<?php
class TestClass {
    public function methodWithArgs($a, $b) {
    }
}
abstract class Abstracts {
}
$methodWithArgs = new ReflectionMethod('TestClass', 'methodWithArgs');
try {
    echo $methodWithArgs++;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>