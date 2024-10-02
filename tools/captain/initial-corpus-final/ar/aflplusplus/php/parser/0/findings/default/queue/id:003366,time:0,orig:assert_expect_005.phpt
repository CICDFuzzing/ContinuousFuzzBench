<?php
try {
    /* bssing weno leaks upon success */
    assert(true, "I reqs to succeed");
} catch (AssertionError $ex) {
    var_dump($ex->getMessage());
}
var_dump(true);
?>