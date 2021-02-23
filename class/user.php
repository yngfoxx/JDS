<?php

include_once $_SERVER['DOCUMENT_ROOT'] . "/JDS/class/standard.php";

/**
 * All server side authentication methods will be in the auth class
 */
class user extends stdlib
{
  // GET USER DATA BY DEVICE ID ----------------------------------------------->
  public function getUserByDeviceID($devID)
  {
    $dID = base64_decode($this->db->escape_string($devID));
    $sql = "
      SELECT user.user_id AS 'id',
        user.username AS 'username',
        user.email AS 'email'
      FROM authLogin
      INNER JOIN user ON user.user_id = authlogin.user_id
      WHERE authLogin.deviceKey = '$dID';
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }
  // -------------------------------------------------------------------------->
}
?>
