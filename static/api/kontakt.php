<?php
// Formularz kontaktowy spondylus.pl: wiadomość na doktor@spondylus.pl. Odpowiedź JSON dla main.js.
// Ochrona przed spamem: ukryte pole „www” i limit 5 wiadomości na godzinę z jednego IP.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

const ODBIORCA = 'doktor@spondylus.pl';
const NADAWCA = 'formularz@spondylus.pl';
const LIMIT_NA_GODZINE = 5;

function odpowiedz($ok, $blad = '', $kod = 200) {
    http_response_code($kod);
    echo json_encode(['ok' => $ok, 'blad' => $blad], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') odpowiedz(false, 'Niedozwolona metoda', 405);
if (!empty($_POST['www'])) odpowiedz(true); // bot wypełnił ukryte pole: udajemy sukces, nic nie wysyłamy

$pole = function ($k, $max) {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
};
$imie = $pole('imie', 120);
$tel = $pole('tel', 40);
$email = $pole('email', 160);
$placowka = $pole('placowka', 80);
$temat = $pole('temat', 80);
$wiadomosc = $pole('wiadomosc', 5000);

if ($imie === '' || $tel === '' || $wiadomosc === '') odpowiedz(false, 'Uzupełnij imię, telefon i wiadomość.', 422);
if (($_POST['zgoda'] ?? '') !== 'tak') odpowiedz(false, 'Potrzebna zgoda na przetwarzanie danych.', 422);
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) odpowiedz(false, 'Nieprawidłowy adres e-mail.', 422);
foreach ([$imie, $tel, $placowka, $temat] as $v) {
    if (preg_match('/[\n]/', $v)) odpowiedz(false, 'Nieprawidłowe dane.', 422); // bez wstrzykiwania nagłówków
}

// limit wiadomości z jednego adresu IP
$katalog = sys_get_temp_dir() . '/spondylus-kontakt';
@mkdir($katalog, 0700, true);
$plik = $katalog . '/' . hash('sha256', $_SERVER['REMOTE_ADDR'] ?? '');
$teraz = time();
$czasy = array_filter(array_map('intval', @file($plik, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > $teraz - 3600);
if (count($czasy) >= LIMIT_NA_GODZINE) odpowiedz(false, 'Za dużo wiadomości. Zadzwoń: 665 035 035.', 429);
$czasy[] = $teraz;
@file_put_contents($plik, implode("\n", $czasy), LOCK_EX);

$tresc = "Wiadomość z formularza kontaktowego spondylus.pl\n\n"
    . "Imię i nazwisko: $imie\nTelefon: $tel\nE-mail: " . ($email ?: '(nie podano)') . "\n"
    . "Placówka: $placowka\nTemat: $temat\n\n$wiadomosc\n";
$naglowki = [
    'From: Spondylus formularz <' . NADAWCA . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];
if ($email !== '') $naglowki[] = 'Reply-To: ' . $email;
$tytul = '=?UTF-8?B?' . base64_encode("Formularz: $temat ($placowka)") . '?=';

if (!mail(ODBIORCA, $tytul, $tresc, implode("\r\n", $naglowki), '-f' . NADAWCA)) {
    odpowiedz(false, 'Serwer nie wysłał wiadomości.', 500);
}
odpowiedz(true);
