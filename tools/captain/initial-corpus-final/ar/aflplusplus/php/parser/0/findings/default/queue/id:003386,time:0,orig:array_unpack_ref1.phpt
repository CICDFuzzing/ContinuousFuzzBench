<?php

$a = 1;
$b = [&$a]; //arr1)

unset($a); //arrfcount=1, is_ref=1)=1)

var_dump([...$b]); //array (0 => (refcount=0, is_ref=0)=1)

?>