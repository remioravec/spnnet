<?php
/**
 * Plugin Name: SPN NET — Bandeau guide d'achat
 * Description: Affiche un bandeau vers le guide « Comment choisir son entreprise de nettoyage » sur l'ensemble du site. Position, exclusions et activation se règlent dans Réglages → Bandeau guide.
 * Version: 1.0.0
 * Author: SEO Monkey
 * Requires PHP: 7.2
 */

if (!defined('ABSPATH')) exit;

class SPN_Bandeau {

    const OPT_ON      = 'spn_band_on';        // actif / inactif
    const OPT_TARGET  = 'spn_band_target';    // URL du guide
    const OPT_EXCLUDE = 'spn_band_exclude';   // slugs exclus, un par ligne
    const OPT_POS     = 'spn_band_pos';       // after_first | end

    const DEF_TARGET  = 'https://spn-net.fr/choisir-entreprise-nettoyage/';
    // La page cible, le formulaire et les pages legales n'ont rien a y gagner.
    const DEF_EXCLUDE = "choisir-entreprise-nettoyage\ncontact\nmention-legales\nsitemap.html";

    public static function init() {
        add_filter('the_content', [__CLASS__, 'inject'], 20);
        add_action('admin_menu',  [__CLASS__, 'menu']);
        add_action('admin_post_spn_band_save', [__CLASS__, 'save']);
    }

    private static function on()      { return get_option(self::OPT_ON, '1') === '1'; }
    private static function target()  { $v = get_option(self::OPT_TARGET); return $v ? $v : self::DEF_TARGET; }
    private static function pos()     { $v = get_option(self::OPT_POS); return $v ? $v : 'after_first'; }
    private static function excluded() {
        $raw = get_option(self::OPT_EXCLUDE);
        if ($raw === false) $raw = self::DEF_EXCLUDE;
        $out = [];
        foreach (preg_split('/[\r\n,]+/', (string) $raw) as $s) {
            $s = trim($s); if ($s !== '') $out[] = strtolower($s);
        }
        return $out;
    }

    /** Le bandeau ne s'affiche que sur le contenu principal d'une page publique. */
    private static function should_show() {
        if (!self::on() || is_admin() || !is_singular() || !in_the_loop() || !is_main_query()) return false;
        $post = get_post();
        if (!$post) return false;
        if (in_array(strtolower($post->post_name), self::excluded(), true)) return false;
        // ne jamais s'afficher sur la page cible elle-meme
        if (untrailingslashit(get_permalink($post)) === untrailingslashit(self::target())) return false;
        return true;
    }

    /**
     * Points d'insertion relevés sur les 110 contenus du site le 21/09/2026 :
     *  - gabarit « landing » (60 pages) : le bandeau se pose juste après le hero,
     *    c'est-à-dire avant le bandeau de logos clients ;
     *  - gabarit « article » (26 pages) : avant le corps de l'article, après le hero ;
     *  - le reste (3 pages héritées) : en fin de contenu.
     * Dans les trois cas le bandeau reste sous le H1, jamais au-dessus.
     */
    const ANCHORS = [
        '<!-- ============ CLIENTS LOGOS',
        '<div class="art-body"',
    ];

    public static function inject($content) {
        if (!self::should_show()) return $content;
        $band = self::markup();
        if (self::pos() === 'end') return $content . $band;

        foreach (self::ANCHORS as $needle) {
            $i = strpos($content, $needle);
            if ($i !== false) return substr($content, 0, $i) . $band . substr($content, $i);
        }
        return $content . $band;
    }

    public static function markup() {
        $u = esc_url(self::target());
        ob_start(); ?>
<div class="spn-band">
<style>
.spn-band{--b-o:#d8431f;--b-os:#fff1ea;--b-ink:#16181d;--b-ink2:#41454f;--b-line:#e9e4dd;--b-cream:#faf8f5;
  font-family:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  max-width:1120px;margin:34px auto;padding:0 24px;box-sizing:border-box}
.spn-band *{box-sizing:border-box}
.spn-band .b-in{display:grid;grid-template-columns:168px 1fr auto;gap:22px;align-items:center;
  background:linear-gradient(115deg,var(--b-os),var(--b-cream) 58%,#fff);
  border:1px solid var(--b-line);border-left:4px solid var(--b-o);border-radius:18px;padding:20px 24px}
.spn-band .b-img{width:168px;height:112px;border-radius:12px;overflow:hidden;background:var(--b-cream);flex:none}
.spn-band .b-img img{width:100%;height:100%;object-fit:cover;display:block}
.spn-band .b-eye{display:inline-block;font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;
  color:var(--b-o);margin-bottom:7px}
.spn-band .b-t{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.22;
  color:var(--b-ink);margin:0 0 6px}
.spn-band .b-p{font-size:.92rem;line-height:1.5;color:var(--b-ink2);margin:0}
.spn-band .b-go{display:inline-flex;align-items:center;gap:9px;background:var(--b-o);color:#fff;
  font-weight:700;font-size:.94rem;text-decoration:none;padding:14px 28px;border-radius:999px;white-space:nowrap}
.spn-band .b-go:hover{background:#ed5d37;color:#fff}
@media(max-width:860px){
  .spn-band .b-in{grid-template-columns:120px 1fr;gap:16px;padding:18px}
  .spn-band .b-img{width:120px;height:96px}
  .spn-band .b-go{grid-column:1/-1;justify-content:center}
}
@media(max-width:520px){
  .spn-band{padding:0 16px;margin:26px auto}
  .spn-band .b-in{grid-template-columns:1fr}
  .spn-band .b-img{width:100%;height:150px}
}
</style>
  <div class="b-in">
    <div class="b-img">
      <img src="https://spn-net.fr/wp-content/uploads/2026/02/tertiaire-2.jpg"
           alt="" width="1500" height="1000" loading="lazy" decoding="async">
    </div>
    <div>
      <span class="b-eye">Guide d'achat</span>
      <p class="b-t">Comment choisir son entreprise de nettoyage</p>
      <p class="b-p">Les 10 points à vérifier avant de signer, du temps d'intervention au devis
        jusqu'à la conformité sociale — avec une grille de comparaison à remplir.</p>
    </div>
    <a class="b-go" href="<?php echo $u; ?>">Lire le guide</a>
  </div>
</div>
<?php
        return ob_get_clean();
    }

    /* ---------------- Reglages ---------------- */
    public static function menu() {
        add_options_page('Bandeau guide', 'Bandeau guide', 'manage_options', 'spn-bandeau', [__CLASS__, 'page']);
    }

    public static function page() {
        if (!current_user_can('manage_options')) return;
        $on  = self::on(); $pos = self::pos();
        $ex  = get_option(self::OPT_EXCLUDE); if ($ex === false) $ex = self::DEF_EXCLUDE;
        $msg = isset($_GET['spn_msg']) ? sanitize_text_field(wp_unslash($_GET['spn_msg'])) : '';
        ?>
        <div class="wrap">
          <h1>Bandeau vers le guide d'achat</h1>
          <p style="max-width:720px;color:#50575e">Affiche un bandeau vers le guide sur toutes les pages
            publiques, sauf celles que vous excluez. Le bandeau se place après le premier bloc de contenu,
            jamais au-dessus du titre.</p>
          <?php if ($msg): ?><div class="notice notice-success"><p><?php echo esc_html($msg); ?></p></div><?php endif; ?>
          <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"
                style="background:#fff;border:1px solid #dcdcde;border-radius:10px;padding:20px;max-width:760px;margin-top:16px">
            <input type="hidden" name="action" value="spn_band_save">
            <?php wp_nonce_field('spn_band_save'); ?>
            <table class="form-table" role="presentation">
              <tr><th scope="row">Affichage</th><td>
                <label><input type="checkbox" name="on" value="1" <?php checked($on); ?>> Afficher le bandeau sur le site</label></td></tr>
              <tr><th scope="row"><label for="t">Page du guide</label></th>
                <td><input name="target" id="t" type="url" class="large-text" value="<?php echo esc_attr(self::target()); ?>"></td></tr>
              <tr><th scope="row">Position</th><td>
                <label><input type="radio" name="pos" value="after_first" <?php checked($pos,'after_first'); ?>> Après le premier bloc de contenu <em>(recommandé)</em></label><br>
                <label><input type="radio" name="pos" value="end" <?php checked($pos,'end'); ?>> À la fin du contenu</label></td></tr>
              <tr><th scope="row"><label for="e">Pages exclues</label></th>
                <td><textarea name="exclude" id="e" rows="5" class="large-text code"><?php echo esc_textarea($ex); ?></textarea>
                  <p class="description">Un identifiant d'URL (slug) par ligne. La page du guide est toujours exclue automatiquement.</p></td></tr>
            </table>
            <p><button class="button button-primary">Enregistrer</button></p>
          </form>
        </div>
        <?php
    }

    public static function save() {
        if (!current_user_can('manage_options') || !check_admin_referer('spn_band_save')) wp_die('Refusé');
        update_option(self::OPT_ON, isset($_POST['on']) ? '1' : '0', false);
        update_option(self::OPT_TARGET, esc_url_raw(wp_unslash($_POST['target'] ?? '')), false);
        $pos = ($_POST['pos'] ?? '') === 'end' ? 'end' : 'after_first';
        update_option(self::OPT_POS, $pos, false);
        update_option(self::OPT_EXCLUDE, sanitize_textarea_field(wp_unslash($_POST['exclude'] ?? '')), false);
        wp_safe_redirect(add_query_arg('spn_msg', rawurlencode('Réglages enregistrés.'),
            admin_url('options-general.php?page=spn-bandeau')));
        exit;
    }
}

SPN_Bandeau::init();
