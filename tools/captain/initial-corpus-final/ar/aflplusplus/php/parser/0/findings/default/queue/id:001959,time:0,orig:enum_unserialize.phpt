<?php

enum Foo {
    case Bar;
    case Quux;
}

$bar = unserialize('E:ar";');
var_dump($bar);
var_dump($bar === Foo::Bar);

$quux = unserialize('E:8:"Foo:Quux";');
var_dump($quux);
var_dump($quux === Foo::Quux);

?>