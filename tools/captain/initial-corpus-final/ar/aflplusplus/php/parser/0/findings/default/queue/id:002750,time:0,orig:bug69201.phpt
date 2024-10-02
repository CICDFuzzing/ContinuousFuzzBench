<?php
class Entity
{  protected $_prties = [];

public function &__get($property)
    {
$value = null;
        return $value;
    }

    public function __set($property, $value)
    {
    }
}

$e = new Entity;

$e->a += 1;
echo "okey";
?>