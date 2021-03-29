<?php

include_once $_SERVER['DOCUMENT_ROOT'] . "/JDS/class/standard.php";

/**
 * All server side authentication methods will be in the auth class
 */
class auth extends stdlib
{
  // KEY ENCRYPT ------------------------------------------------------------------------------------->
  function keyCry($key, $hash) { return password_hash(md5($hash."".$key."".$hash), PASSWORD_BCRYPT); }
  // ------------------------------------------------------------------------------------------------->

  // KEY CRYPT CHECK ------------------------------------------------------------------------------------->
  function keyCheck($recieved_pass, $real_hash, $real_key) {
    $keyGiven = md5($real_hash."".$recieved_pass."".$real_hash);
    return password_verify($keyGiven, $real_key);
  }
  // ------------------------------------------------------------------------------------------------------>


  // GET USER BY EMAIL -------------------------------------------------------->
  public function getUserByEmail($email)
  {
    $sql = "SELECT * FROM user WHERE email = '$email'";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }
  // -------------------------------------------------------------------------->


  // GET USER BY USERNAME ----------------------------------------------------->
  public function getUserByUserName($username)
  {
    $sql = "SELECT * FROM user WHERE username = '$username'";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }
  // -------------------------------------------------------------------------->


  // ADD USER TO DATABASE ----------------------------------------------------->
  public function makeUser($arr)
  {
    $sql = "INSERT INTO user(username, email, password, hash) VALUES('".$arr['username']."', '".$arr['email']."', '".$arr['key']."', '".$arr['hash']."')";
    $qry = mysqli_query($this->db, $sql);
    return $qry;
  }
  // -------------------------------------------------------------------------->


  // ASSIGN DEVICE KEY TO USER ------------------------------------------------>
  public function crtDeviceID($arr)
  {
    # Delete any existing device key
    $sql = "DELETE FROM authlogin WHERE user_id = '".$arr['uid']."'";
    $qry = mysqli_query($this->db, $sql);

    # Add new device key for automatic login
    $sql = "INSERT INTO authlogin(user_id, deviceKey) VALUES('".$arr['uid']."', '".$arr['dk']."')";
    $qry = mysqli_query($this->db, $sql);

    return $qry;
  }
  // -------------------------------------------------------------------------->


  // GET USER BY DEVICE ID ---------------------------------------------------->
  public function getUserIdByDeviceID($devID)
  {
    $dID = base64_decode($this->db->escape_string($devID));
    $sql = "
      SELECT user.user_id AS 'id' FROM authlogin
	     INNER JOIN user ON user.user_id = authlogin.user_id
      WHERE authlogin.deviceKey = '$dID';
    ";
    $qry = mysqli_query($this->db, $sql);
    return ((mysqli_num_rows($qry) == 1) ? mysqli_fetch_assoc($qry)['id'] : false);
  }
  // -------------------------------------------------------------------------->


  // Verify user device by cookie --------------------------------------------->
  function verfUser($devID)
  {
    $dID = base64_decode($this->db->escape_string($devID));
    $sql = "
      SELECT user.user_id AS 'id', authlogin.deviceKey AS 'key' FROM authlogin
	     INNER JOIN user ON user.user_id = authlogin.user_id
      WHERE authlogin.deviceKey = '$devID';
    ";
    $qry = mysqli_query($this->db, $sql);
    if (!$qry) return false;
    return true;
  }
  // -------------------------------------------------------------------------->


  // Set users local network ip address variable ------------------------------>
  public function set_lan_addr($uID, $net_addr)
  {
    $uID = $this->db->escape_string($uID);
    $nAddr = $this->db->escape_string($net_addr);
    $sql = "
      UPDATE authlogin SET local_net_addr = '$nAddr'
      WHERE user_id = '$uID';
    ";
    $qry = mysqli_query($this->db, $sql);
    if (!$qry) return false;
    return true;
  }
  // -------------------------------------------------------------------------->


  // Get user local network ip address variable ------------------------------->
  public function get_lan_addr($uID)
  {
    $uID = $this->db->escape_string($uID);
    $sql = "
      SELECT user.user_id AS 'id',
        authlogin.local_net_addr as 'ipv4' FROM authlogin
        INNER JOIN user ON user.user_id = authlogin.user_id
      WHERE authlogin.user_id = '$uID';
    ";
    $qry = mysqli_query($this->db, $sql);
    return ((mysqli_num_rows($qry) == 1) ? mysqli_fetch_assoc($qry)['ipv4'] : 'none');
  }
  // -------------------------------------------------------------------------->
}
 ?>
