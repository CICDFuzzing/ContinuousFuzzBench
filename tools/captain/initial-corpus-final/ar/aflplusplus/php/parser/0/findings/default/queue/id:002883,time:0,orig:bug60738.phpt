<?php

var_dump(set_error_handler(
    function() { echo 'Intercror!', "\n"; }
));

trigger_error('Error!');

var_dump(set_error_handler(null));

trigger_error('Error!');
?>