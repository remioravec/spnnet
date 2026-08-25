<?php
/**
 * Plugin Name: SPN NET — CRM des demandes (leads)
 * Description: CRM léger : capture toutes les demandes (Elementor + endpoint REST), qualifie bon/mauvais lead, filtre, source précise + canal, e-mail de secours, export CSV. Design moderne 2026.
 * Version: 1.3.0
 * Author: SEO Monkey
 * Requires PHP: 7.2
 */

if (!defined('ABSPATH')) exit;

class SPN_Leads {

    const TABLE = 'spn_leads';
    const OPT_EMAIL = 'spn_leads_notify_email';

    public static function init() {
        register_activation_hook(__FILE__, [__CLASS__, 'activate']);
        add_action('elementor_pro/forms/new_record', [__CLASS__, 'capture'], 10, 2);
        add_action('rest_api_init', [__CLASS__, 'rest']);
        add_action('admin_menu', [__CLASS__, 'menu']);
        add_action('admin_post_spn_leads_export', [__CLASS__, 'export_csv']);
        add_action('admin_post_spn_leads_save_settings', [__CLASS__, 'save_settings']);
        add_action('admin_post_spn_leads_quality', [__CLASS__, 'set_quality']);
        add_action('admin_post_spn_leads_delete', [__CLASS__, 'delete_row']);
        add_action('admin_post_spn_leads_purge_tests', [__CLASS__, 'purge_tests']);
    }

    /* ---------- Table ---------- */
    public static function activate() {
        global $wpdb;
        $t = $wpdb->prefix . self::TABLE;
        $charset = $wpdb->get_charset_collate();
        $sql = "CREATE TABLE $t (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            created_at DATETIME NOT NULL,
            name VARCHAR(255) NULL,
            email VARCHAR(255) NULL,
            phone VARCHAR(100) NULL,
            company VARCHAR(255) NULL,
            message TEXT NULL,
            source VARCHAR(255) NULL,
            form VARCHAR(150) NULL,
            channel VARCHAR(30) NULL,
            ip VARCHAR(64) NULL,
            quality VARCHAR(12) NULL DEFAULT '',
            PRIMARY KEY (id),
            KEY created_at (created_at),
            KEY quality (quality)
        ) $charset;";
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta($sql);
        if (get_option(self::OPT_EMAIL) === false) update_option(self::OPT_EMAIL, get_option('admin_email'));
    }

    /* ---------- Helpers ---------- */
    private static $FREEMAIL = ['gmail.com','googlemail.com','yahoo.com','yahoo.fr','ymail.com','hotmail.com','hotmail.fr','outlook.com','outlook.fr','live.com','live.fr','msn.com','aol.com','icloud.com','me.com','free.fr','orange.fr','wanadoo.fr','sfr.fr','neuf.fr','laposte.net','bbox.fr','gmx.com','gmx.fr','protonmail.com','proton.me','yopmail.com','mail.com'];

    private static function is_pro_email($email) {
        if (!$email || strpos($email, '@') === false) return false;
        $d = strtolower(substr(strrchr($email, '@'), 1));
        return !in_array($d, self::$FREEMAIL, true);
    }

    private static function client_ip() {
        foreach (['HTTP_CF_CONNECTING_IP','HTTP_X_FORWARDED_FOR','REMOTE_ADDR'] as $k) {
            if (!empty($_SERVER[$k])) return substr(trim(explode(',', $_SERVER[$k])[0]), 0, 64);
        }
        return '';
    }

    private static function is_test_row($r) {
        $email = strtolower($r['email'] ?? ''); $name = strtoupper(trim($r['name'] ?? ''));
        return (substr($email, -12) === '@example.com')
            || (strpos($name, 'ZZ TEST') === 0)
            || in_array($email, ['test-sidebar@spn-net.fr','test-endpoint@spn-net.fr','hook-a@spn-net.fr','hook-b@spn-net.fr','autre-email@spn-net.fr','apres-fix@example.com'], true);
    }

    /* ---------- Insertion + e-mail de secours ---------- */
    private static function store($d, $channel) {
        global $wpdb; $t = $wpdb->prefix . self::TABLE;
        if (!empty($d['email']) || !empty($d['phone'])) {
            $since = get_date_from_gmt(gmdate('Y-m-d H:i:s', time() - 180));
            $dupe = $wpdb->get_var($wpdb->prepare(
                "SELECT id FROM $t WHERE created_at >= %s AND ((email <> '' AND email = %s) OR (phone <> '' AND phone = %s)) LIMIT 1",
                $since, (string)$d['email'], (string)$d['phone']));
            if ($dupe) return (int)$dupe;
        }
        $wpdb->insert($t, [
            'created_at' => current_time('mysql'),
            'name' => $d['name'], 'email' => $d['email'], 'phone' => $d['phone'],
            'company' => $d['company'], 'message' => $d['message'],
            'source' => $d['source'], 'form' => $d['form'],
            'channel' => $channel, 'ip' => $d['ip'], 'quality' => '',
        ]);
        $id = (int)$wpdb->insert_id;
        $to = get_option(self::OPT_EMAIL);
        if ($to) {
            $body  = "Nouvelle demande via le site.\n\nNom : {$d['name']}\nE-mail : {$d['email']}\nTéléphone : {$d['phone']}\nEntreprise : {$d['company']}\n\nMessage :\n{$d['message']}\n\nPage : {$d['source']}\nCanal : $channel\nDate : " . current_time('mysql') . "\n";
            $h = []; if ($d['email'] && is_email($d['email'])) $h[] = 'Reply-To: ' . $d['email'];
            wp_mail($to, '🧹 Nouvelle demande — ' . ($d['name'] ?: $d['email'] ?: 'Sans nom'), $body, $h);
        }
        return $id;
    }

    /* ---------- Endpoint REST public ---------- */
    public static function rest() {
        register_rest_route('spn/v1', '/lead', ['methods'=>'POST','permission_callback'=>'__return_true','callback'=>[__CLASS__,'rest_lead']]);
        // Export sécurisé (admin only) : backfill complet des submissions Elementor puis dump JSON.
        register_rest_route('spn/v1', '/export', [
            'methods'  => 'GET',
            'permission_callback' => function () { return current_user_can('manage_options'); },
            'callback' => [__CLASS__, 'rest_export'],
        ]);
    }

    /** Renvoie toutes les demandes (historique inclus), tests signalés. Auth : App Password admin. */
    public static function rest_export($req) {
        self::backfill(); // récupère l'historique Elementor manquant dans la table
        global $wpdb; $t = $wpdb->prefix . self::TABLE;
        $rows = $wpdb->get_results("SELECT * FROM $t ORDER BY created_at ASC", ARRAY_A) ?: [];
        $include_tests = (string)$req->get_param('tests') === '1';
        $out = [];
        foreach ($rows as $r) {
            $r['is_test'] = self::is_test_row($r) ? 1 : 0;
            if (!$include_tests && $r['is_test']) continue;
            $out[] = $r;
        }
        return new WP_REST_Response([
            'ok' => true,
            'count' => count($out),
            'generated_at' => current_time('mysql'),
            'rows' => $out,
        ], 200);
    }
    public static function rest_lead($req) {
        if ((string)$req->get_param('website') !== '') return new WP_REST_Response(['ok'=>true], 200);
        $c = function($k,$l=255) use ($req){ return mb_substr(sanitize_text_field((string)$req->get_param($k)),0,$l); };
        $email = sanitize_email((string)$req->get_param('email'));
        $d = ['name'=>$c('name'),'email'=>$email,'phone'=>$c('phone',100),'company'=>$c('company'),
              'message'=>mb_substr(wp_strip_all_tags((string)$req->get_param('message')),0,4000),
              'source'=>esc_url_raw((string)$req->get_param('source')),'form'=>$c('form',150),'ip'=>self::client_ip()];
        if (!$d['email'] && !$d['phone']) return new WP_REST_Response(['ok'=>false,'error'=>'contact manquant'],400);
        return new WP_REST_Response(['ok'=>true,'id'=>self::store($d,'rest')],200);
    }

    /* ---------- Capture Elementor ---------- */
    public static function capture($record, $handler) {
        try {
            $fields = $record->get('fields');
            $name=$email=$phone=$company=$message='';
            foreach ($fields as $id => $f) {
                $type=$f['type']??''; $val=$f['value']??''; if ($val==='') continue;
                if ($type==='email' && !$email){$email=$val;continue;}
                if ($type==='tel' && !$phone){$phone=$val;continue;}
                if ($type==='textarea' && !$message){$message=$val;continue;}
                if ((stripos($id,'name')!==false||stripos($id,'nom')!==false)&&!$name){$name=$val;continue;}
                if ((stripos($id,'entreprise')!==false||stripos($id,'company')!==false||$id==='field_e9cc337')&&!$company){$company=$val;continue;}
                if ($id==='message'&&!$message)$message=$val;
                if ($id==='name'&&!$name)$name=$val;
            }
            $source = isset($_POST['referer']) ? esc_url_raw($_POST['referer']) : '';
            if (!$source){$m=$record->get('meta'); if(isset($m['page_url']['value']))$source=$m['page_url']['value'];}
            $form = method_exists($record,'get_form_settings')?(string)$record->get_form_settings('form_name'):'';
            self::store(['name'=>$name,'email'=>$email,'phone'=>$phone,'company'=>$company,'message'=>$message,'source'=>$source,'form'=>$form,'ip'=>self::client_ip()],'elementor');
        } catch (\Throwable $e) {}
    }

    /* ---------- Backfill historique Elementor -> table (dédup) ---------- */
    private static function backfill() {
        global $wpdb;
        $sub=$wpdb->prefix.'e_submissions'; $val=$wpdb->prefix.'e_submissions_values'; $t=$wpdb->prefix.self::TABLE;
        if ($wpdb->get_var($wpdb->prepare("SHOW TABLES LIKE %s",$sub))!==$sub) return;
        $rows=$wpdb->get_results("SELECT id, form_name, referer, created_at FROM $sub ORDER BY created_at DESC LIMIT 5000");
        if (!$rows) return;
        foreach ($rows as $r) {
            $vals=$wpdb->get_results($wpdb->prepare("SELECT `key`,`value` FROM $val WHERE submission_id=%d",$r->id));
            $map=[]; foreach($vals as $v)$map[strtolower($v->key)]=$v->value;
            $pick=function($keys)use($map){foreach($keys as $k)foreach($map as $mk=>$mv){if(strpos($mk,$k)!==false&&$mv!=='')return $mv;}return '';};
            $email=$pick(['email','mail']); $phone=$pick(['tel','phone','1696542','2dc1dda']);
            if (!$email && !$phone) continue;
            $exists=$wpdb->get_var($wpdb->prepare(
                "SELECT id FROM $t WHERE created_at=%s AND (email=%s OR phone=%s) LIMIT 1",$r->created_at,$email,$phone));
            if ($exists) continue;
            $wpdb->insert($t,['created_at'=>$r->created_at,'name'=>$pick(['name','nom']),'email'=>$email,
                'phone'=>$phone,'company'=>$pick(['entreprise','company','e9cc337']),'message'=>$pick(['message']),
                'source'=>$r->referer,'form'=>$r->form_name,'channel'=>'elementor','ip'=>'','quality'=>'']);
        }
    }

    /* ---------- Admin ---------- */
    public static function menu() {
        add_menu_page('CRM Demandes','Demandes','manage_options','spn-leads',[__CLASS__,'page'],'dashicons-groups',26);
    }

    private static function post_url($action, $args=[]) {
        $args=array_merge(['action'=>$action],$args);
        return wp_nonce_url(add_query_arg($args,admin_url('admin-post.php')),$action);
    }

    public static function page() {
        if (!current_user_can('manage_options')) return;
        self::backfill();
        global $wpdb; $t=$wpdb->prefix.self::TABLE;
        $filter = isset($_GET['q']) ? sanitize_key($_GET['q']) : 'all';
        $where = '1=1';
        if ($filter==='good') $where="quality='good'";
        elseif ($filter==='bad') $where="quality='bad'";
        elseif ($filter==='none') $where="(quality='' OR quality IS NULL)";
        $rows=$wpdb->get_results("SELECT * FROM $t WHERE $where ORDER BY created_at DESC",ARRAY_A) ?: [];
        // exclure les tests de l'affichage
        $rows=array_values(array_filter($rows,function($r){return !self::is_test_row($r);}));
        $stats=[
            'all'=>(int)$wpdb->get_var("SELECT COUNT(*) FROM $t"),
            'good'=>(int)$wpdb->get_var("SELECT COUNT(*) FROM $t WHERE quality='good'"),
            'bad'=>(int)$wpdb->get_var("SELECT COUNT(*) FROM $t WHERE quality='bad'"),
            'none'=>(int)$wpdb->get_var("SELECT COUNT(*) FROM $t WHERE quality='' OR quality IS NULL"),
        ];
        $ntest=(int)$wpdb->get_var("SELECT COUNT(*) FROM $t WHERE email LIKE '%@example.com' OR name LIKE 'ZZ TEST%'");
        $notify=esc_attr(get_option(self::OPT_EMAIL));
        $export=wp_nonce_url(admin_url('admin-post.php?action=spn_leads_export'),'spn_leads_export');
        self::css();
        echo '<div class="wrap spncrm"><div class="spn-top"><div><h1>Demandes <span class="spn-count">'.count($rows).'</span></h1>'
            .'<p class="spn-sub">CRM des leads — capture Elementor + endpoint, qualification & suivi.</p></div>'
            .'<div class="spn-actions"><a class="spn-btn ghost" href="'.esc_url($export).'">⬇ Export CSV</a></div></div>';

        // stat cards
        echo '<div class="spn-cards">';
        $card=function($k,$lbl,$cls,$active)use($stats){
            $u=esc_url(add_query_arg('q',$k,admin_url('admin.php?page=spn-leads')));
            echo '<a href="'.$u.'" class="spn-card '.$cls.($active?' on':'').'"><div class="n">'.$stats[$k].'</div><div class="l">'.$lbl.'</div></a>';
        };
        $card('all','Toutes','c-all',$filter==='all');
        $card('good','🟢 Bons leads','c-good',$filter==='good');
        $card('bad','🔴 Mauvais / spam','c-bad',$filter==='bad');
        $card('none','⚪ À qualifier','c-none',$filter==='none');
        echo '</div>';

        if ($ntest>0) {
            echo '<div class="spn-notice">🧪 '.$ntest.' entrée(s) de test détectée(s). '
                .'<a class="spn-btn danger sm" href="'.esc_url(self::post_url('spn_leads_purge_tests')).'" onclick="return confirm(\'Supprimer définitivement les entrées de test ?\')">Purger les tests</a></div>';
        }

        // table
        echo '<div class="spn-table"><table><thead><tr>'
            .'<th>Date</th><th>Contact</th><th>Source & canal</th><th>Message</th><th>Qualité</th><th></th></tr></thead><tbody>';
        if (!$rows) echo '<tr><td colspan="6" class="spn-empty">Aucune demande pour ce filtre.</td></tr>';
        foreach ($rows as $r) {
            $pro=self::is_pro_email($r['email']);
            $q=$r['quality'];
            $when=self::human_date($r['created_at']);
            $src=$r['source']; $srclabel=$src?parse_url($src,PHP_URL_PATH):'—';
            $chan=$r['channel']?:'—';
            echo '<tr class="q-'.esc_attr($q?:'none').'">';
            echo '<td class="spn-date"><b>'.esc_html($when['d']).'</b><span>'.esc_html($when['t']).'</span></td>';
            // contact
            echo '<td class="spn-contact"><div class="nm">'.esc_html($r['name']?:'—').'</div>';
            if ($r['email']) echo '<div class="em"><a href="mailto:'.esc_attr($r['email']).'">'.esc_html($r['email']).'</a> <span class="tag '.($pro?'pro':'perso').'">'.($pro?'pro':'perso').'</span></div>';
            if ($r['phone']) echo '<div class="ph"><a href="tel:'.esc_attr($r['phone']).'">'.esc_html($r['phone']).'</a></div>';
            if ($r['company']) echo '<div class="co">'.esc_html($r['company']).'</div>';
            echo '</td>';
            // source & canal
            echo '<td class="spn-src"><span class="chan chan-'.esc_attr($chan).'">'.esc_html($chan).'</span>';
            if ($src) echo '<a class="pg" href="'.esc_url($src).'" target="_blank" title="'.esc_attr($src).'">'.esc_html($srclabel).'</a>';
            if ($r['ip']) echo '<span class="ip">'.esc_html($r['ip']).'</span>';
            echo '</td>';
            // message
            echo '<td class="spn-msg">'.esc_html(mb_strimwidth((string)$r['message'],0,150,'…')).'</td>';
            // quality toggle
            $gu=self::post_url('spn_leads_quality',['id'=>$r['id'],'v'=>'good','q'=>$filter]);
            $bu=self::post_url('spn_leads_quality',['id'=>$r['id'],'v'=>'bad','q'=>$filter]);
            echo '<td class="spn-q"><a class="qbtn good'.($q==='good'?' on':'').'" href="'.esc_url($gu).'" title="Bon lead">Bon</a>'
                .'<a class="qbtn bad'.($q==='bad'?' on':'').'" href="'.esc_url($bu).'" title="Mauvais / spam">Spam</a></td>';
            // delete
            $du=self::post_url('spn_leads_delete',['id'=>$r['id'],'q'=>$filter]);
            echo '<td class="spn-del"><a href="'.esc_url($du).'" onclick="return confirm(\'Supprimer cette demande ?\')" title="Supprimer">✕</a></td>';
            echo '</tr>';
        }
        echo '</tbody></table></div>';

        // settings
        echo '<form class="spn-settings" method="post" action="'.esc_url(admin_url('admin-post.php')).'">'
            .'<input type="hidden" name="action" value="spn_leads_save_settings">';
        wp_nonce_field('spn_leads_settings');
        echo '<label>E-mails de notification <input type="text" name="notify" value="'.$notify.'" placeholder="a@b.fr, c@d.fr"></label>'
            .'<button class="spn-btn">Enregistrer</button></form>';
        echo '</div>';
    }

    private static function human_date($mysql) {
        $ts=strtotime($mysql);
        return ['d'=>date_i18n('j M Y',$ts),'t'=>date_i18n('H:i',$ts)];
    }

    /* ---------- Actions ---------- */
    public static function set_quality() {
        if (!current_user_can('manage_options')||!wp_verify_nonce($_GET['_wpnonce']??'','spn_leads_quality')) wp_die('Refusé');
        global $wpdb; $id=(int)($_GET['id']??0); $v=in_array($_GET['v']??'',['good','bad'],true)?$_GET['v']:'';
        // clic sur un état déjà actif = on l'enlève
        $cur=$wpdb->get_var($wpdb->prepare("SELECT quality FROM ".$wpdb->prefix.self::TABLE." WHERE id=%d",$id));
        if ($cur===$v) $v='';
        $wpdb->update($wpdb->prefix.self::TABLE,['quality'=>$v],['id'=>$id]);
        self::back();
    }
    public static function delete_row() {
        if (!current_user_can('manage_options')||!wp_verify_nonce($_GET['_wpnonce']??'','spn_leads_delete')) wp_die('Refusé');
        global $wpdb; $wpdb->delete($wpdb->prefix.self::TABLE,['id'=>(int)($_GET['id']??0)]);
        self::back();
    }
    public static function purge_tests() {
        if (!current_user_can('manage_options')||!wp_verify_nonce($_GET['_wpnonce']??'','spn_leads_purge_tests')) wp_die('Refusé');
        global $wpdb; $t=$wpdb->prefix.self::TABLE;
        $wpdb->query("DELETE FROM $t WHERE email LIKE '%@example.com' OR name LIKE 'ZZ TEST%' OR email IN ('test-sidebar@spn-net.fr','test-endpoint@spn-net.fr','hook-a@spn-net.fr','hook-b@spn-net.fr','autre-email@spn-net.fr')");
        self::back();
    }
    private static function back() {
        $q=isset($_GET['q'])?'&q='.sanitize_key($_GET['q']):'';
        wp_redirect(admin_url('admin.php?page=spn-leads'.$q)); exit;
    }

    public static function save_settings() {
        if (!current_user_can('manage_options')||!check_admin_referer('spn_leads_settings')) wp_die('Refusé');
        $emails=array_filter(array_map('sanitize_email',array_map('trim',explode(',', (string)($_POST['notify']??'')))));
        update_option(self::OPT_EMAIL, implode(', ',$emails));
        wp_redirect(admin_url('admin.php?page=spn-leads')); exit;
    }

    public static function export_csv() {
        if (!current_user_can('manage_options')||!check_admin_referer('spn_leads_export')) wp_die('Refusé');
        global $wpdb; $rows=$wpdb->get_results("SELECT * FROM ".$wpdb->prefix.self::TABLE." ORDER BY created_at DESC",ARRAY_A)?:[];
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename=demandes-spn-'.date('Y-m-d').'.csv');
        $out=fopen('php://output','w'); fprintf($out,"\xEF\xBB\xBF");
        fputcsv($out,['Date','Nom','Email','Telephone','Entreprise','Message','Source','Canal','IP','Qualite'],';');
        foreach ($rows as $r) if(!self::is_test_row($r)) fputcsv($out,[$r['created_at'],$r['name'],$r['email'],$r['phone'],$r['company'],$r['message'],$r['source'],$r['channel'],$r['ip'],$r['quality']],';');
        fclose($out); exit;
    }

    /* ---------- Style CRM 2026 ---------- */
    private static function css() { ?>
<style>
.spncrm{--ink:#0f172a;--mut:#64748b;--line:#e6e9ef;--bg:#f6f8fb;--card:#fff;--brand:#4f46e5;--green:#16a34a;--green-s:#dcfce7;--red:#dc2626;--red-s:#fee2e2;--amber:#d97706;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,sans-serif;color:var(--ink);max-width:1220px}
.spncrm h1{font-size:26px;font-weight:750;letter-spacing:-.02em;margin:0;display:flex;align-items:center;gap:12px}
.spncrm .spn-count{background:var(--brand);color:#fff;font-size:14px;font-weight:700;padding:3px 12px;border-radius:100px}
.spncrm .spn-sub{color:var(--mut);margin:6px 0 0;font-size:14px}
.spncrm .spn-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin:12px 0 22px;flex-wrap:wrap}
.spncrm .spn-btn{display:inline-flex;align-items:center;gap:7px;background:var(--brand);color:#fff;border:none;border-radius:10px;padding:9px 16px;font-weight:600;font-size:13.5px;cursor:pointer;text-decoration:none;transition:.15s}
.spncrm .spn-btn:hover{filter:brightness(1.08);color:#fff}
.spncrm .spn-btn.ghost{background:#fff;color:var(--ink);border:1px solid var(--line)}
.spncrm .spn-btn.danger{background:var(--red)}.spncrm .spn-btn.sm{padding:5px 12px;font-size:12.5px}
.spncrm .spn-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
@media(max-width:900px){.spncrm .spn-cards{grid-template-columns:repeat(2,1fr)}}
.spncrm .spn-card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;text-decoration:none;color:var(--ink);transition:.15s;box-shadow:0 1px 2px rgba(15,23,42,.04)}
.spncrm .spn-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(15,23,42,.09)}
.spncrm .spn-card .n{font-size:30px;font-weight:750;line-height:1}
.spncrm .spn-card .l{color:var(--mut);font-size:13px;margin-top:6px;font-weight:600}
.spncrm .spn-card.on{border-color:var(--brand);box-shadow:0 0 0 3px rgba(79,70,229,.12)}
.spncrm .spn-card.c-good.on{border-color:var(--green);box-shadow:0 0 0 3px var(--green-s)}
.spncrm .spn-card.c-bad.on{border-color:var(--red);box-shadow:0 0 0 3px var(--red-s)}
.spncrm .spn-notice{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;padding:11px 16px;border-radius:12px;margin-bottom:16px;font-size:13.5px;display:flex;align-items:center;gap:12px}
.spncrm .spn-table{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 1px 3px rgba(15,23,42,.05)}
.spncrm table{width:100%;border-collapse:collapse;font-size:13.5px}
.spncrm thead th{background:var(--bg);text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);font-weight:700;padding:13px 16px;border-bottom:1px solid var(--line)}
.spncrm tbody td{padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top}
.spncrm tbody tr:last-child td{border-bottom:none}
.spncrm tbody tr{transition:background .12s}.spncrm tbody tr:hover{background:#fafbfd}
.spncrm tr.q-good{box-shadow:inset 3px 0 0 var(--green)}
.spncrm tr.q-bad{box-shadow:inset 3px 0 0 var(--red);opacity:.72}
.spncrm .spn-date b{display:block;font-weight:650}.spncrm .spn-date span{color:var(--mut);font-size:12px}
.spncrm .spn-contact .nm{font-weight:650}
.spncrm .spn-contact .em a,.spncrm .spn-contact .ph a{color:var(--brand);text-decoration:none}
.spncrm .spn-contact .co{color:var(--mut);font-size:12.5px;margin-top:2px}
.spncrm .tag{font-size:10px;font-weight:700;text-transform:uppercase;padding:2px 7px;border-radius:100px;vertical-align:middle}
.spncrm .tag.pro{background:var(--green-s);color:var(--green)}.spncrm .tag.perso{background:#f1f5f9;color:var(--mut)}
.spncrm .chan{display:inline-block;font-size:11px;font-weight:700;padding:3px 9px;border-radius:6px;background:#eef2ff;color:var(--brand);text-transform:capitalize}
.spncrm .chan-rest{background:#ecfeff;color:#0891b2}.spncrm .chan-historique{background:#f8fafc;color:var(--mut)}
.spncrm .spn-src .pg{display:block;color:var(--ink);font-size:12px;margin-top:5px;text-decoration:none;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.spncrm .spn-src .pg:hover{color:var(--brand)}
.spncrm .spn-src .ip{display:block;color:#94a3b8;font-size:11px;margin-top:3px;font-variant-numeric:tabular-nums}
.spncrm .spn-msg{color:var(--mut);max-width:260px;font-size:12.5px}
.spncrm .spn-q{white-space:nowrap}
.spncrm .qbtn{display:inline-block;font-size:12px;font-weight:650;padding:5px 11px;border-radius:8px;text-decoration:none;border:1px solid var(--line);color:var(--mut);margin-right:5px}
.spncrm .qbtn.good:hover,.spncrm .qbtn.good.on{background:var(--green);color:#fff;border-color:var(--green)}
.spncrm .qbtn.bad:hover,.spncrm .qbtn.bad.on{background:var(--red);color:#fff;border-color:var(--red)}
.spncrm .spn-del a{color:#cbd5e1;text-decoration:none;font-size:15px;font-weight:700}.spncrm .spn-del a:hover{color:var(--red)}
.spncrm .spn-empty{text-align:center;color:var(--mut);padding:40px}
.spncrm .spn-settings{margin-top:22px;display:flex;gap:12px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px}
.spncrm .spn-settings label{font-weight:600;font-size:13.5px;display:flex;gap:10px;align-items:center;flex:1}
.spncrm .spn-settings input{flex:1;max-width:420px;padding:8px 12px;border:1px solid var(--line);border-radius:9px;font-size:13.5px}
</style>
<?php }
}

SPN_Leads::init();
