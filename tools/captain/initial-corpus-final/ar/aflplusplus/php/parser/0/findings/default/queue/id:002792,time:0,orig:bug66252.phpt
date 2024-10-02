<?php
class A {
    const HW = " is A";
}
class B extends A {
    const BHW = parent::HW . " extended by B";
}
const C = B::BHW;
echo C, "\n";
?>