<?php
/**
 * Plugin Name: SPN NET — Envoi des e-mails (Google Workspace)
 * Description: Route les e-mails de WordPress par le SMTP authentifié de Google Workspace, au lieu de la fonction mail() du serveur. Tout se règle depuis Réglages → Envoi e-mails : aucun fichier à modifier.
 * Version: 1.2.0
 * Author: SEO Monkey
 * Requires PHP: 7.2
 */

if (!defined('ABSPATH')) exit;

class SPN_SMTP {

    const HOST = 'smtp.gmail.com';
    const PORT = 587;               // STARTTLS
    const SECURE = 'tls';

    const OPT_USER = 'spn_smtp_user';
    const OPT_PASS = 'spn_smtp_pass';
    const OPT_FROM = 'spn_smtp_from';
    const OPT_NAME = 'spn_smtp_from_name';

    const DEFAULT_USER = 'remi-oravec@seo-monkey.fr';

    public static function init() {
        add_action('phpmailer_init',    [__CLASS__, 'configure']);
        add_filter('wp_mail_from',      [__CLASS__, 'from'], 99);
        add_filter('wp_mail_from_name', [__CLASS__, 'from_name'], 99);
        add_action('admin_menu',        [__CLASS__, 'menu']);
        add_action('admin_post_spn_smtp_save', [__CLASS__, 'save']);
        add_action('admin_post_spn_smtp_test', [__CLASS__, 'send_test']);
        add_action('rest_api_init',     [__CLASS__, 'rest']);
        add_action('admin_notices',     [__CLASS__, 'notice']);
    }

    /* ---------- Valeurs ---------- */
    public static function user() {
        $v = get_option(self::OPT_USER);
        return $v ? $v : self::DEFAULT_USER;
    }
    /** La constante de wp-config reste prioritaire si elle existe. */
    private static function pass() {
        if (defined('SPN_SMTP_PASS') && trim((string) SPN_SMTP_PASS) !== '') return trim((string) SPN_SMTP_PASS);
        return (string) get_option(self::OPT_PASS, '');
    }
    private static function ready() { return self::pass() !== ''; }

    public static function from_name($name = '') {
        $v = get_option(self::OPT_NAME);
        return $v ? $v : 'SPN NET';
    }
    /** Google n'accepte que le compte authentifié ou un de ses alias vérifiés. */
    public static function from($email = '') {
        if (!self::ready()) return $email;
        $v = get_option(self::OPT_FROM);
        return $v ? $v : self::user();
    }

    /* ---------- Branchement SMTP ---------- */
    public static function configure($phpmailer) {
        if (!self::ready()) return;   // rien de configuré : WordPress garde son envoi habituel
        try {
            $phpmailer->isSMTP();
            $phpmailer->Host       = self::HOST;
            $phpmailer->Port       = self::PORT;
            $phpmailer->SMTPAuth   = true;
            $phpmailer->SMTPSecure = self::SECURE;
            $phpmailer->Username   = self::user();
            $phpmailer->Password   = str_replace(' ', '', self::pass()); // Google affiche le mdp par blocs de 4
            $phpmailer->CharSet    = 'UTF-8';
            $phpmailer->Timeout    = 20;
            $from = self::from('');
            $phpmailer->setFrom($from, self::from_name(''), false);
            $phpmailer->Sender = $from;   // Return-Path (SPF)
            // Le Reply-To n'est pas touché : il porte l'adresse du prospect.
        } catch (\Throwable $e) { /* on ne casse jamais l'envoi */ }
    }

    /* ---------- Écran de réglages ---------- */
    public static function menu() {
        add_options_page('Envoi e-mails', 'Envoi e-mails', 'manage_options', 'spn-smtp', [__CLASS__, 'page']);
    }

    public static function page() {
        if (!current_user_can('manage_options')) return;
        $ok   = self::ready();
        $user = esc_attr(self::user());
        $from = esc_attr(get_option(self::OPT_FROM, ''));
        $name = esc_attr(get_option(self::OPT_NAME, 'SPN NET'));
        $const = defined('SPN_SMTP_PASS') && trim((string) SPN_SMTP_PASS) !== '';
        $msg = isset($_GET['spn_msg']) ? sanitize_text_field(wp_unslash($_GET['spn_msg'])) : '';
        ?>
        <div class="wrap">
          <h1>Envoi des e-mails</h1>
          <p style="max-width:720px;color:#50575e">
            Les e-mails du site (notifications de demandes, formulaires) partent par défaut via le serveur,
            ce qui finit souvent en indésirables. Ce réglage les fait partir par votre compte Google Workspace.
          </p>

          <?php if ($msg): ?>
            <div class="notice notice-<?php echo strpos($msg, 'Erreur') === 0 ? 'error' : 'success'; ?>"><p><?php echo esc_html($msg); ?></p></div>
          <?php endif; ?>

          <div style="background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:8px 20px;max-width:720px;margin-top:16px">
            <p style="font-size:15px">
              État :
              <?php if ($ok): ?>
                <b style="color:#1e8e3e">✓ configuré</b> — les e-mails partent via Google.
              <?php else: ?>
                <b style="color:#b06000">non configuré</b> — les e-mails partent encore via le serveur.
              <?php endif; ?>
            </p>
          </div>

          <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"
                style="background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:20px;max-width:720px;margin-top:16px">
            <input type="hidden" name="action" value="spn_smtp_save">
            <?php wp_nonce_field('spn_smtp_save'); ?>
            <table class="form-table" role="presentation">
              <tr>
                <th scope="row"><label for="u">Adresse Google</label></th>
                <td><input name="user" id="u" type="email" class="regular-text" value="<?php echo $user; ?>" required>
                  <p class="description">Le compte Workspace qui enverra les messages.</p></td>
              </tr>
              <tr>
                <th scope="row"><label for="p">Mot de passe d'application</label></th>
                <td>
                  <?php if ($const): ?>
                    <p><em>Défini dans wp-config.php — ce champ est ignoré.</em></p>
                  <?php else: ?>
                    <input name="pass" id="p" type="password" class="regular-text" autocomplete="new-password"
                           placeholder="<?php echo $ok ? '•••••••• (déjà enregistré)' : 'xxxx xxxx xxxx xxxx'; ?>">
                    <p class="description">
                      16 caractères générés sur
                      <a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noopener">myaccount.google.com/apppasswords</a>.
                      Les espaces sont acceptés. Laissez vide pour conserver celui déjà enregistré.
                    </p>
                  <?php endif; ?>
                </td>
              </tr>
              <tr>
                <th scope="row"><label for="f">Expéditeur affiché</label></th>
                <td><input name="from" id="f" type="email" class="regular-text" value="<?php echo $from; ?>" placeholder="<?php echo $user; ?>">
                  <p class="description">
                    Laissez vide pour utiliser l'adresse Google ci-dessus. Pour afficher une autre adresse
                    (ex. contact@spn-net.fr), elle doit d'abord être ajoutée comme alias vérifié dans Gmail
                    (Paramètres → Comptes → « Envoyer des e-mails en tant que »), sinon Google la remplacera.
                  </p></td>
              </tr>
              <tr>
                <th scope="row"><label for="n">Nom affiché</label></th>
                <td><input name="from_name" id="n" type="text" class="regular-text" value="<?php echo $name; ?>"></td>
              </tr>
            </table>
            <p><button class="button button-primary">Enregistrer</button></p>
          </form>

          <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"
                style="background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:20px;max-width:720px;margin-top:16px">
            <input type="hidden" name="action" value="spn_smtp_test">
            <?php wp_nonce_field('spn_smtp_test'); ?>
            <h2 style="margin-top:0;font-size:16px">Envoyer un test</h2>
            <p>
              <input name="to" type="email" class="regular-text" value="<?php echo esc_attr(get_option('admin_email')); ?>" required>
              <button class="button">Envoyer</button>
            </p>
            <p class="description">Un message de contrôle est envoyé à cette adresse. En cas d'échec, l'erreur exacte de Google s'affiche.</p>
          </form>
        </div>
        <?php
    }

    public static function save() {
        if (!current_user_can('manage_options') || !check_admin_referer('spn_smtp_save')) wp_die('Refusé');
        update_option(self::OPT_USER, sanitize_email(wp_unslash($_POST['user'] ?? '')), false);
        update_option(self::OPT_FROM, sanitize_email(wp_unslash($_POST['from'] ?? '')), false);
        update_option(self::OPT_NAME, sanitize_text_field(wp_unslash($_POST['from_name'] ?? '')), false);
        $p = trim((string) wp_unslash($_POST['pass'] ?? ''));
        if ($p !== '') update_option(self::OPT_PASS, $p, false);   // vide = on garde l'existant
        self::back('Réglages enregistrés.');
    }

    public static function send_test() {
        if (!current_user_can('manage_options') || !check_admin_referer('spn_smtp_test')) wp_die('Refusé');
        $to = sanitize_email(wp_unslash($_POST['to'] ?? ''));
        if (!$to) self::back('Erreur : adresse de test invalide.');
        $res = self::do_test($to);
        self::back($res['ok']
            ? 'Message de test envoyé à ' . $to . ' (expéditeur : ' . $res['from'] . '). Vérifiez la réception.'
            : 'Erreur : ' . ($res['errors'] ? implode(' / ', $res['errors']) : 'envoi refusé')
              . ($res['dialog'] ? '  —  Réponse de Google : ' . $res['dialog'] : ''));
    }

    private static function do_test($to) {
        if (!self::ready()) return ['ok' => false, 'from' => '', 'errors' => ["aucun mot de passe d'application enregistré"], 'dialog' => ''];
        $errors = []; $dialog = '';

        // On capture le dialogue SMTP pour remonter le motif exact de Google.
        // Seules les réponses du SERVEUR sont conservées : les lignes du client
        // contiennent l'authentification encodée, elles ne sont jamais gardées.
        $sniff = function ($m) use (&$dialog) {
            $m->SMTPDebug   = 2;
            $m->Debugoutput = function ($str, $level) use (&$dialog) {
                if (strpos($str, 'SERVER -> CLIENT') !== false) {
                    $dialog .= trim($str) . "\n";
                }
            };
        };
        add_action('phpmailer_init', $sniff, 99);

        $catch = function ($e) use (&$errors) { $errors[] = $e->get_error_message(); };
        add_action('wp_mail_failed', $catch);

        $sent = wp_mail($to, 'Test d\'envoi — spn-net.fr',
            "Test d'envoi depuis spn-net.fr via Google Workspace.\n\nDate : " . current_time('mysql')
            . "\nExpéditeur : " . self::from('') . "\n",
            ['Content-Type: text/plain; charset=UTF-8']);

        remove_action('wp_mail_failed', $catch);
        remove_action('phpmailer_init', $sniff, 99);

        // On ne garde que les réponses parlantes (codes d'erreur SMTP).
        $keep = [];
        foreach (explode("\n", $dialog) as $line) {
            if (preg_match('/\b(5\d\d|4\d\d)[ -]/', $line)) $keep[] = preg_replace('/^.*SERVER -> CLIENT:?\s*/', '', $line);
        }
        return ['ok' => (bool) $sent, 'from' => self::from(''), 'errors' => $errors,
                'dialog' => trim(implode(' | ', array_slice($keep, -6)))];
    }

    private static function back($msg) {
        wp_safe_redirect(add_query_arg('spn_msg', rawurlencode($msg), admin_url('options-general.php?page=spn-smtp')));
        exit;
    }

    /* ---------- Contrôle à distance (admin only) ---------- */
    public static function rest() {
        $perm = function () { return current_user_can('manage_options'); };
        register_rest_route('spn/v1', '/smtp-status', ['methods' => 'GET', 'permission_callback' => $perm,
            'callback' => function () {
                return new WP_REST_Response([
                    'ok' => true, 'configured' => self::ready(), 'host' => self::HOST, 'port' => self::PORT,
                    'user' => self::user(), 'from' => self::from(''), 'from_name' => self::from_name(''),
                ], 200);
            }]);
        register_rest_route('spn/v1', '/smtp-test', ['methods' => 'POST', 'permission_callback' => $perm,
            'callback' => function ($req) {
                $to = sanitize_email((string) $req->get_param('to'));
                if (!$to) $to = get_option('admin_email');
                return new WP_REST_Response(self::do_test($to) + ['to' => $to], 200);
            }]);
    }

    public static function notice() {
        if (self::ready() || !current_user_can('manage_options')) return;
        $s = get_current_screen();
        if ($s && $s->id === 'settings_page_spn-smtp') return;
        echo '<div class="notice notice-warning"><p><b>SPN NET — envoi des e-mails :</b> pas encore configuré. '
           . '<a href="' . esc_url(admin_url('options-general.php?page=spn-smtp')) . '">Renseigner le mot de passe d\'application</a>.</p></div>';
    }
}

SPN_SMTP::init();
