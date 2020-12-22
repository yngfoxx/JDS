<?php
session_start();
// $allowed_origins = array(
//   "http://localhost:8000"
// );
// header('Access-Control-Allow-Origin: ' . $allowed_origins);
// header('Access-Control-Allow-Credentials: true');
// header('Access-Control-Allow-Headers: Content-Type');

if (isset($_COOKIE['dKEY'])) {
  // PACKAGES ---------------------------
  include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
  include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/auth.php';
  // ------------------------------------


  // OBJECTS [reusable] -----------------
  $std = new stdlib();
  $auth = new auth();
  // ------------------------------------


  $dKEY = $std->db->escape_string($_COOKIE['dKEY']);
  if ($auth->getUserIdByDeviceID($dKEY) != false && !isset($_GET['home'])) {
    $_SESSION['userID'] = $auth->getUserIdByDeviceID($dKEY)['user_id'];
    $_SESSION['logged_in'] = true;
    header("location: ./?home");
  }
}
?>
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <?php require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/header.php'; ?>
  </head>
  <body>
    <div class="_prc_container"></div>
    <div class="web_container">
      <?php
        if (count($_GET) == 0) header("location: ./?login");
        else
        if (isset($_GET['register'])) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/page/register.php';
        else
        if (isset($_GET['login'])) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/page/login.php';
        else
        if (isset($_GET['home'])) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/page/home.php';
        else
        if (isset($_GET['logout'])) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/page/logout.php';
        else
        echo "ERROR 404"; // error page

      ?>
    </div>
    <?php require $_SERVER['DOCUMENT_ROOT'] . '/JDS/section/footer.php'; ?>
  </body>
</html>
