<?php
/**
 * Plugin Name: SPN NET — Redirections 301 (anciennes pages)
 * Description: Redirections 301 en dur des anciennes pages vers leurs équivalents neufs. Purge le cache LiteSpeed à l'activation. Aucune configuration.
 * Version: 1.0.0
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

    public static function init() {
        register_activation_hook(__FILE__, [__CLASS__, 'on_activate']);
        // très tôt, avant que WordPress ne serve la page
        add_action('template_redirect', [__CLASS__, 'redirect'], 0);
        add_action('parse_request', [__CLASS__, 'redirect'], 0);
    }

    private static function current_path() {
        $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/';
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

    /** À l'activation : purge le cache LiteSpeed pour que les 301 prennent effet tout de suite. */
    public static function on_activate() {
        if (function_exists('do_action')) {
            do_action('litespeed_purge_all');           // LiteSpeed Cache
            do_action('litespeed_purge_all_lscache');   // variante
        }
    }
}

SPN_Redirects::init();
