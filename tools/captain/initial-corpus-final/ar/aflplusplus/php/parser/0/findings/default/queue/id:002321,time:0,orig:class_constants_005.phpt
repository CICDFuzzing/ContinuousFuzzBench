<?php
define ("A", "." . ord(26) . ".");
eval("class A {t a = A;}");
var_dump(A::a);
?>