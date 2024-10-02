<?php

trait AbstractTrait {
    abstract public function selfReturner(): self;
}

trait ConeTrait {
    public function selfReturner(): self {
return $this;
    }
}

class Test {
use Abstractt;
    use Concr;
}

?>
===DONE=