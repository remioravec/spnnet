<?php
/**
 * Plugin Name: SPN NET — Envoi des e-mails via Google Workspace
 * Description: Route les e-mails de WordPress (notifications de demandes, formulaires) par le SMTP authentifié de Google Workspace, au lieu de la fonction mail() du serveur. Le mot de passe d'application se définit dans wp-config.php, jamais dans ce fichier.
 * Version: 1.0.0
 * Author: SEO Monkey
 * Requires PHP: 7.2
 */

if (!defined('ABSPATH')) exit;

class SPN_SMTP {

    const HOST   = 'smtp.gmail.com';
    const PORT   = 587;      // STARTTLS
    const SECURE = 'tls';
    const USER   = 'remi-oravec@seo-monkey.fr';

    public static function init() {
        add_action('phpmailer_init',   [__CLASS__, 'configure']);
        add_filter('wp_mail_from',     [__CLASS__, 'from'],      99);
        add_filter('wp_mail_from_name',[__CLASS__, 'from_name'], 99);
        add_action('rest_api_init',    [__CLASS__, 'rest']);
        add_action('admin_notices',    [__CLASS__, 'notice']);
    }

    /** Mot de passe d'application Google — défini dans wp-config.php uniquement. */
    private static function pass() {
        return defined('SPN_SMTP_PASS') ? trim((string) SPN_SMTP_PASS) : '';
    }

    private static function ready() {
        return self::pass() !== '';
    }

    /** Nom affiché de l'expéditeur (surchargeable par constante). */
    public static function from_name($name = '') {
        if (defined('SPN_SMTP_FROM_NAME')) return SPN_SMTP_FROM_NAME;
        return 'SPN NET';
    }

    /**
     * Google n'autorise à envoyer que depuis le compte authentifié (ou un de ses
     * alias vérifiés). On aligne donc l'expéditeur, sinon Gmail le réécrit ou rejette.
     */
    public static function from($email = '') {
        if (!self::ready()) return $email;          // pas configuré : on ne touche à rien
        if (defined('SPN_SMTP_FROM')) return SPN_SMTP_FROM;
        return self::USER;
    }

    public static function configure($phpmailer) {
        if (!self::ready()) return;                  // sans mot de passe, WordPress garde mail()
        try {
            $phpmailer->isSMTP();
            $phpmailer->Host       = self::HOST;
            $phpmailer->Port       = self::PORT;
            $phpmailer->SMTPAuth   = true;
            $phpmailer->SMTPSecure = self::SECURE;
            $phpmailer->Username   = self::USER;
            $phpmailer->Password   = self::pass();
            $phpmailer->CharSet    = 'UTF-8';
            $phpmailer->Encoding   = 'base64';
            $phpmailer->Timeout    = 20;

            // Expéditeur aligné sur le compte authentifié (exigence Google).
            $from = self::from('');
            $phpmailer->setFrom($from, self::from_name(''), false);
            $phpmailer->Sender = $from;              // Return-Path : ce qui fait passer SPF

            // On NE touche PAS au Reply-To : le plugin de demandes y met déjà
            // l'adresse du prospect, ce qui permet de répondre directement.
        } catch (\Throwable $e) {
            // Ne jamais casser l'envoi : en cas d'erreur on laisse WordPress faire.
        }
    }

    /* ---------- Test à distance (admin only) ---------- */
    public static function rest() {
        register_rest_route('spn/v1', '/smtp-test', [
            'methods'  => 'POST',
            'permission_callback' => function () { return current_user_can('manage_options'); },
            'callback' => [__CLASS__, 'rest_test'],
        ]);
        register_rest_route('spn/v1', '/smtp-status', [
            'methods'  => 'GET',
            'permission_callback' => function () { return current_user_can('manage_options'); },
            'callback' => [__CLASS__, 'rest_status'],
        ]);
    }

    public static function rest_status() {
        return new WP_REST_Response([
            'ok'            => true,
            'configured'    => self::ready(),
            'host'          => self::HOST,
            'port'          => self::PORT,
            'user'          => self::USER,
            'from'          => self::from(''),
            'from_name'     => self::from_name(''),
            'password_set'  => self::ready(),   // jamais la valeur, seulement l'état
        ], 200);
    }

    public static function rest_test($req) {
        $to = sanitize_email((string) $req->get_param('to'));
        if (!$to) $to = self::USER;
        if (!self::ready()) {
            return new WP_REST_Response([
                'ok' => false,
                'error' => "SPN_SMTP_PASS n'est pas défini dans wp-config.php — l'envoi passe encore par le serveur.",
            ], 200);
        }
        $errors = [];
        $catch = function ($wp_error) use (&$errors) {
            $errors[] = $wp_error->get_error_message();
        };
        add_action('wp_mail_failed', $catch);

        $sent = wp_mail(
            $to,
            'Test SMTP — spn-net.fr',
            "Ceci est un test d'envoi depuis spn-net.fr via Google Workspace.\n\n"
            . 'Date : ' . current_time('mysql') . "\n"
            . 'Expéditeur : ' . self::from('') . "\n",
            ['Content-Type: text/plain; charset=UTF-8']
        );

        remove_action('wp_mail_failed', $catch);

        return new WP_REST_Response([
            'ok'      => (bool) $sent,
            'to'      => $to,
            'from'    => self::from(''),
            'errors'  => $errors,
        ], 200);
    }

    /* ---------- Rappel discret en admin si non configuré ---------- */
    public static function notice() {
        if (self::ready() || !current_user_can('manage_options')) return;
        echo '<div class="notice notice-warning"><p><b>SPN NET — envoi des e-mails :</b> '
           . 'le mot de passe d\'application Google n\'est pas encore renseigné. '
           . 'Ajoutez la ligne <code>define(\'SPN_SMTP_PASS\', \'votre-mot-de-passe-application\');</code> '
           . 'dans <code>wp-config.php</code>. En attendant, les e-mails continuent de partir par le serveur.</p></div>';
    }
}

SPN_SMTP::init();
