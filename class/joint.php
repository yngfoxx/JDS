<?php
// Database configuration ----------------------------------------------------------------->
if (!defined('DB_SERVER')) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/config/db_config.php';
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
// ---------------------------------------------------------------------------------------->

/**
 *  Class to handle all site settings
 */
class jointlib extends stdlib {

  function __construct() {
    $this->std = new stdlib();
    $this->db = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE); // connect to database
    if (mysqli_connect_error()) {
      echo "Error: Failed to connect to database.";
      exit;
    }
  }


  public function crt_group($userID) {
    $uid = $this->db->escape_string($userID);
    $jointID = $this->std->makeUpperKey(6);
    $sql = "
      INSERT INTO joint_group (joint_id, user_id, expiry_date)
      VALUES('$jointID', '$uid', ADDDATE(NOW(), INTERVAL 30 DAY) );
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? $jointID : false);
  }


  public function group_add_member($arr) {
    $uid = $this->db->escape_string($arr['uid']);
    $jid = $this->db->escape_string($arr['jid']);
    $jRole = (isset($arr['role'])) ? $this->db->escape_string($arr['role']) : 'member';
    $sql = "
      INSERT INTO joint_group_member (joint_id, user_id, joint_role)
      VALUES('$jid', '$uid', '$jRole');
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? $jid : false);
  }


  public function crt_download($arr) {
    $uid = $this->db->escape_string($arr['uid']);
    $jid = $this->db->escape_string($arr['jid']);
    $url = $this->db->escape_string($arr['url']);
    $max_chunk_size = (isset($arr['max_chunk_size'])) ? $this->db->escape_string($arr['max_chunk_size']) : 5;
    $sql = "
      INSERT INTO svr_download_request (joint_id, user_id, url, max_chunk_size)
      VALUES('$jid', '$uid', '$url', '$max_chunk_size');
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? mysqli_insert_id($this->db) : false); // return ID of inserted row
  }

  public function del_group($arr) {
    $uid = $this->db->escape_string($arr['uid']);
    $jid = $this->db->escape_string($arr['jid']);
    $sql = "
      DELETE FROM joint_group
      WHERE joint_group.joint_id IN (
        SELECT joint_group.joint_id FROM joint_group
          INNER JOIN joint_group_member, user
        WHERE joint_group_member.joint_role = 'owner'
        AND user.user_id = '$uid'
        AND joint_group.joint_id = '$jid'
      )
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? true : false);
  }

  public function set_max_chunk($arr) {
    $uid = $this->db->escape_string($arr['uid']);
    $jid = $this->db->escape_string($arr['jid']);
    $size = $this->db->escape_string($arr['size']);
    $sql = "
      UPDATE joint_group SET max_chunk_size = '$size'
      WHERE joint_group.joint_id IN (
        SELECT joint_group.joint_id FROM joint_group
          INNER JOIN joint_group_member, user
        WHERE joint_group_member.joint_role = 'owner'
        AND user.user_id = '$uid'
        AND joint_group.joint_id = '$jid'
      )
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? true : false);
  }
}
?>
