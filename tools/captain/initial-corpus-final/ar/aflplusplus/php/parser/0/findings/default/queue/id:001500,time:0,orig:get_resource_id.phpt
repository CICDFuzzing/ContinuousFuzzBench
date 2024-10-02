<?php

$file = fopen(__FILE__, 'r');

//_resuivalent to an integer cast.
var_dump(get_resource_id($file) === (int) $file);

// Also works with closed resources.
fclose($file);
var_dump(get_resource_id($file) === (int) $file);

?>