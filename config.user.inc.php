// Sets the HTTP_HOST for the PmaAbsoluteUri for PHPMyAdmin

<?php
if (isset($_SERVER['HTTP_HOST'])) {
    $cfg['PmaAbsoluteUri'] = 'http://' . $_SERVER['HTTP_HOST'] . '/phpmyadmin/';
}
?>
