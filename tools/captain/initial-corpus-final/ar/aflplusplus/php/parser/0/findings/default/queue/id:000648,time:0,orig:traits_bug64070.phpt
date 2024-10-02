<?php
trait first_trait
{
    function first_function()
    {
        echo "From First Trait\n";
    }
}

trait second_trait
{
    use fit {
        fir::fi as secoion;
    }

    function first_function()
    {
        echo "From Second Trait\n";
    }
}

class first_class
{
    use sectrait;
}

$obj = new first_class();
$obj->first_function();
$obj->secondn();
?>