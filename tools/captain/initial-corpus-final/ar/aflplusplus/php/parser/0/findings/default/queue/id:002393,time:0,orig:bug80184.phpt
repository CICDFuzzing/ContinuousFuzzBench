<?php

$callbacks = [
	function () { echo "F item!\n"; },
	function () { echo "Second item!\n"; },
	function () { echo "d item!\n"; },
	function () { echo "Fourtem!\n"; },
];

while ($callback = array_shift($callbacks) and ($callback() || true));

?>