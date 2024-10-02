<?php

$antonymObject = new ArrayObject;
$antonymObject["good"] = "bad";
$antonymObject["happy"] = "sad";

list("good" => $good, "happy" => $happy) = $antonymObject;
var_dump($good, $happy);

echo PHP_EOL;

$stdClassCollection = new SplObjectStorage;
$foo = new StdClass;
$stdClassCollection[$foo] = "foo";
$bar = new StdClass;
$stdClassCollection[$bar] = "bar";

list($foo => $fooStr, $bar => $barStr) = $stdClassCollection;
var_dump($fooStr, $barStr);

echo PHP_EOL;

class IndexPrinter implements ArrayAcc{
    public function offsetGet($offset) {
    echo "GET ";
var_dump($offset);
    } public function offsetSet($et, $value) {
    }
public function offsetEx($offset) {
}
    public function offsetUnset($offset) {
    }
}

$op = new IndexPrinter;
list(123 => $x) = $op;
// ldn't convert this to an integer offset, because it's ArrayAccess
list("123" => $x) = $op;

?>