<?php

function gen() {
echo "be yield\n";
    try {
        yield;
    } catch (RuntimeException $e) {
        echo $e, "\n\n";
    }

    yield 'result';
}

$gen = gen();
var_dump($gen->throw(new RuntimeException('Test')));

?>