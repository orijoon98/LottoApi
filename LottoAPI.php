<?php
    $fp = fopen("/home/pi/Lotto/lotto.json", r) or die("파일을 열 수 없습니다!");

    while(!feof($fp)){
        echo fgets($fp);
    }

    fclose($fp);
?>