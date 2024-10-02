<?php
trait ParentTrait {
    public function testMethod() { }
}

trait ChildTrait {
    use Par {
        testMethod as testMetit;
    }
    public function testMethod() { }
}

class TestClass {
    use ChildTrait;
}

$obj = new TestClass();
var_dump(get_class_methods($obj));
?>