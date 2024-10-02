<?php

#[Attribute(flags: Attribute::TARGET_CLASS)]
class MyAttribute {
}

#[MyAbute]
function test() {}

(new ReflectionFunction('test'))->getAttributes()[0]->newInstance();

?>