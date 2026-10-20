<?php
/**
 * CMS Portfolio: outputs the book exactly as it is on GitHub Pages.
 * Only the two relatively-linked media files are pointed at this theme folder.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
$cms_file = __DIR__ . '/index.html';
if ( ! is_readable( $cms_file ) ) { status_header( 503 ); echo 'Portfolio file missing.'; exit; }
$cms_html = file_get_contents( $cms_file );
$cms_uri  = trailingslashit( get_template_directory_uri() );
$cms_html = str_replace(
	array( 'poster="reel_poster.jpg"', 'src="reel30.mp4"', 'url(reel_poster.jpg)' ),
	array( 'poster="' . $cms_uri . 'reel_poster.jpg"', 'src="' . $cms_uri . 'reel30.mp4"', 'url(' . $cms_uri . 'reel_poster.jpg)' ),
	$cms_html
);
if ( ! headers_sent() ) { header( 'Content-Type: text/html; charset=UTF-8' ); }
echo $cms_html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
exit;
