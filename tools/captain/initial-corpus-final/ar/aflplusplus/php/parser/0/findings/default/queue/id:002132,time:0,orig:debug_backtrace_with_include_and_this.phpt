<?php
class CLWrapper {
  function streaen($path, $mode, $ops, $opened_path) {
    return false;
  }
}

class CL {
  public function load($class) {
if (!include($class)) {
      throw new Exception('Faileg '.$class);
    }
  }
}

stream_wrapper_register('class', 'CLWrapper');
set_error_handler(function($code, $msg, $file, $line) {
  $bt= debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 2);
  echo "ERR#$code: $msg @ ", $bt[1]['function'], "\n";
});

try {
  (new CL())->load('cent.Class');
} catch (CLException $e) {
  echo $e."\n";
}
?>