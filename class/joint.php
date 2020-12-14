<?php
// Database configuration ----------------------------------------------------------------->
if (!defined('DB_SERVER')) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/config/db_config.php';
// ---------------------------------------------------------------------------------------->

/**
 *  Class to handle all site settings
 */
class jointlib extends stdlib {

  function __construct() {
    $this->db = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE); // connect to database
    if (mysqli_connect_error()) {
      echo "Error: Failed to connect to database.";
      exit;
    }
  }

  public function crt_group($userID) {
    include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
    $std = new stdlib();
    $uid = $this->db->escape_string($userID);
    $jointID = $std->makeUpperKey(6);
    $sql = "
      INSERT INTO joint_group (joint_id, user_id, expiry_date)
      VALUES('$jointID', '$uid', ADDDATE(NOW(), INTERVAL 30 DAY) );
    ";
    $qry = mysqli_query($this->db, $sql);
    return ($qry) ? $jointID : false;
  }
}
?>
