<?php
    $message_base64 = $_POST['message'];
    $message_binary = base64_decode($message_base64);

    $ip = $_SERVER['REMOTE_ADDR'];

    $fp = fopen('/var/www/t/ip.txt', 'w');
    fwrite($fp, $ip . "\n");
    fclose($fp);

    $fp = fopen('/var/www/t/message.txt', 'wb');
    fwrite($fp, $message_binary);
    fclose($fp);
?>
