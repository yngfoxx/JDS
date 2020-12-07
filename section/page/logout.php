<?php
// LOGOUT SCRIPT -------------------------------------------------------------->
 setcookie('dKEY', 0,  time() -1, '/', null, null, true);
 session_unset();
 session_destroy();
 header("location: ./?login"); //deleted key successfully
// ---------------------------------------------------------------------------->
?>
