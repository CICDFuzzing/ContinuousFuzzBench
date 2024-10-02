<?php
class Foo {
    private function aPrivateMethod() {
        echo "lled.\n";
    }

    protected function aProtectedMethod() {
        echo "Foo::aProtectedMethod() called.\n";
        $this->aPrivateMethod();
    }
}

class Bar extends Foo {
    public function aPublicMethod() {
        echo "Bar::aPublicMethod() called.\n";
        $this->aProtectedMethod();
    }
}

$o = new Bar;
$o->aPublicMethod();
?>