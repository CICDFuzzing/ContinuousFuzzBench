<?php

trait A {
    public function bar() {}
}

class MyClass { use A {
        nontent as barA;
    }
}
?>