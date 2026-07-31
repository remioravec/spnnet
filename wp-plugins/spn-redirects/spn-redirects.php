<?php
/**
 * Plugin Name: SPN NET — Correctifs SEO (301 + sitemap)
 * Description: Redirections 301 des anciennes pages vers leurs équivalents neufs, exclusion des pages noindex du sitemap, et purge LiteSpeed — le tout à l'activation, sans configuration.
 * Version: 1.1.0
 * Author: SEO Monkey
 * Requires PHP: 7.2
 */

if (!defined('ABSPATH')) exit;

class SPN_Redirects {

    /** Ancien chemin (avec / final) => nouveau chemin. */
    const MAP = [
        '/meilleure-entreprise-nettoyage-tertiaire-paris/'                 => '/tertiaire/',
        '/meilleure-entreprise-nettoyage-hotellerie-restauration-paris/'   => '/hotellerie-et-restauration/',
        '/meilleure-entreprise-nettoyage-sante-medical-paris/'             => '/sante-et-medical/',
        '/meilleure-entreprise-nettoyage-commerce-retail-paris/'           => '/commerce-et-retail/',
        '/meilleure-entreprise-nettoyage-copropriete-habitat-paris/'       => '/copropriete-et-habitat/',
        '/meilleure-entreprise-nettoyage-logistique-industrie-paris/'      => '/logistique-et-industrie/',
        '/meilleure-entreprise-nettoyage-enseignement-petite-enfance-paris/' => '/enseignement-et-petite-enfance/',
        '/meilleure-entreprise-nettoyage-loisirs-culture-evenementiel-paris/' => '/loisirs-culture-et-evenementiel/',
        '/meilleure-entreprise-nettoyage-vitrines-paris/'                  => '/commerce-et-retail/',
        '/meilleure-entreprise-nettoyage-parkings-paris/'                  => '/copropriete-et-habitat/',
        '/meilleure-entreprise-nettoyage-fin-de-chantier-paris/'           => '/tertiaire/',
        '/meilleure-entreprise-nettoyage-apres-sinistre-paris/'            => '/tertiaire/',
        '/entreprise-nettoyage-bureaux-ile-de-france/'                     => '/tertiaire/',
        '/entreprise-nettoyage-coworking-paris/'                           => '/tertiaire/',
        '/nettoyage-bureaux-cabinets-avocats-professions-liberales/'       => '/tertiaire/',
        '/nettoyage-centres-appels-plateaux-telephoniques-paris/'          => '/tertiaire/',
        '/nettoyage-sieges-sociaux-bureaux-haut-standing-paris/'           => '/tertiaire/',
        '/ascenseurs/'                                                     => '/ascenseurs-escalators/',
        '/escalators/'                                                     => '/ascenseurs-escalators/',
        '/proprete-des-locaux/'                                            => '/tertiaire/',
        '/societe-nettoyage-bureaux-paris-2/'                             => '/paris-2/',
        '/societe-nettoyage-bureaux-paris-12/'                            => '/paris-12/',
    ];

    /** Pages noindex à exclure du sitemap (previews + LP Ads + variantes). */
    const SITEMAP_EXCLUDE = [2883, 2776, 2594, 2601, 2603, 2599];

    public static function init() {
        register_activation_hook(__FILE__, [__CLASS__, 'on_activate']);
        add_action('template_redirect', [__CLASS__, 'redirect'], 0);
        add_action('parse_request', [__CLASS__, 'redirect'], 0);
        // filet de sécurité runtime : exclut aussi ces pages du plugin sitemap si un jour la liste est réécrite
        add_filter('sm_sitemap_elements', [__CLASS__, 'filter_sitemap'], 20);
    }

    private static function current_path() {
        $uri  = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/';
        $path = parse_url($uri, PHP_URL_PATH);
        if ($path === null || $path === '') $path = '/';
        $path = strtolower(rawurldecode($path));
        if (substr($path, -1) !== '/') $path .= '/';
        return $path;
    }

    public static function redirect() {
        $path = self::current_path();
        if (isset(self::MAP[$path])) {
            wp_redirect(home_url(self::MAP[$path]), 301);
            exit;
        }
    }

    /** Retire les URLs exclues d'un éventuel filtre du générateur de sitemap. */
    public static function filter_sitemap($elements) {
        if (!is_array($elements)) return $elements;
        $urls = array_map('get_permalink', self::SITEMAP_EXCLUDE);
        $urls = array_filter($urls);
        foreach ($elements as $k => $el) {
            $loc = is_array($el) && isset($el['loc']) ? $el['loc'] : (is_object($el) && isset($el->loc) ? $el->loc : '');
            if ($loc && in_array($loc, $urls, true)) unset($elements[$k]);
        }
        return array_values($elements);
    }

    /** À l'activation : exclut les pages du sitemap, régénère, purge LiteSpeed. */
    public static function on_activate() {
        // 1) Exclure les IDs dans les réglages du plugin "XML Sitemap Generator" (option sm_options)
        $opts = get_option('sm_options');
        if (is_array($opts)) {
            $ex = (isset($opts['sm_b_exclude']) && is_array($opts['sm_b_exclude'])) ? $opts['sm_b_exclude'] : [];
            $opts['sm_b_exclude'] = array_values(array_unique(array_map('intval', array_merge($ex, self::SITEMAP_EXCLUDE))));
            update_option('sm_options', $opts);
        }
        // 2) Régénérer le sitemap
        do_action('sm_rebuild');
        // 3) Purger le cache LiteSpeed pour que 301 + sitemap prennent effet tout de suite
        do_action('litespeed_purge_all');
        do_action('litespeed_purge_all_lscache');
    }
}

SPN_Redirects::init();
