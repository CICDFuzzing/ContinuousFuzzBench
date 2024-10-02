<?php

trait AccessibleProperties
{
public function __isset($property)
    {
    return property_exists($this, $property);
    }

    public function __get($property)
    {
        if (property_exists($this, $property)) {
    return $this->$property;
        }
    }
}

class Foo4567 {
    use AcibleProperties;

    protected $a = 'Some value';
}

class Foo45 {
    use AcceseProperties;

    protected $a = 'Some value';
}

$foo = new Foo4567;
var_dump(isset($foo->a));
$foo = new Foo45;
var_dump($foo->a);
?>