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
    $channel = $this->std->makeNumericKey(6);
    $sql = "
      INSERT INTO joint_group (joint_id, user_id, py_channel, expiry_date)
      VALUES('$jointID', '$uid', '$channel', ADDDATE(NOW(), INTERVAL 30 DAY) );
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
    $uid = $this->db->escape_string($arr['uid']); # User ID
    $jid = $this->db->escape_string($arr['jid']); # Joint ID
    $url = $this->db->escape_string($arr['url']); # File requested
    $ext = $this->db->escape_string($arr['ext']); # File extension
    $size = $this->db->escape_string($arr['size']); # File size
    $max_chunk_size = (isset($arr['max_chunk_size'])) ? $this->db->escape_string($arr['max_chunk_size']) : 5;
    $sql = "
      INSERT INTO svr_download_request (joint_id, user_id, url, ext, size, max_chunk_size)
      VALUES('$jid', '$uid', '$url', '$ext', '$size', '$max_chunk_size');
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
    $svrID = $this->db->escape_string($arr['svrID']);
    $size = $this->db->escape_string($arr['size']);
    $sql = "
      UPDATE svr_download_request
      SET svr_download_request.max_chunk_size = '$size'
      WHERE svr_download_request.request_id = '$svrID'
      AND svr_download_request.request_id IN (
        SELECT svr_download_request.request_id
        FROM svr_download_request
          INNER JOIN joint_group_member, user
        WHERE joint_group_member.joint_role = 'owner'
        AND user.user_id = '$uid'
      );
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? $svrID : false);
  }


  public function getUserJointList($uid)
  {
    $uid = $this->db->escape_string($uid);
    $sql = "
      SELECT joint_group_member.joint_id AS 'jid',
        joint_group_member.joint_role AS 'role',
        user.user_id AS 'uid'
      FROM joint_group_member
      INNER JOIN user ON user.user_id = joint_group_member.user_id
      INNER JOIN joint_group ON joint_group.joint_id = joint_group_member.joint_id
      WHERE user.user_id = '$uid'
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 0 || !$qry) return 0;
    $arr = array();
    while ($jData = mysqli_fetch_assoc($qry)) array_push($arr, $jData);
    return $arr;
  }


  public function getJointDownloadList($jid)
  {
    $jid = $this->db->escape_string($jid);
    $sql = "
    SELECT
      svr_download_request.request_id AS 'rid',
      joint_group.joint_id AS 'jid',
      svr_download_request.url AS 'url',
      svr_download_request.max_chunk_size AS 'chunk_size',
      user.user_id AS 'uid',
      svr_download_request.ext AS 'ext',
      svr_download_request.size AS 'size',
      svr_download_request.init AS 'status'
    FROM svr_download_request
    INNER JOIN joint_group ON joint_group.joint_id = svr_download_request.joint_id
    INNER JOIN user ON user.user_id = svr_download_request.user_id
    WHERE svr_download_request.joint_id = '$jid'
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 0 || !$qry) return 0;
    $arr = array();
    while ($jData = mysqli_fetch_assoc($qry)) array_push($arr, $jData); // store sql result in array
    return $arr;
  }


  public function getJointInfo($jid)
  {
    $jid = $this->db->escape_string($jid);
    $sql = "
    SELECT
      joint_group.joint_id AS 'jid',
      joint_group.user_id AS 'uid',
      joint_group.py_channel AS 'channel',
      joint_group.access_limit AS 'capacity',
      joint_group.date_created AS 'creationDate'
     FROM joint_group
     WHERE joint_group.joint_id = '$jid'";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }


  public function getJointMembers($jid)
  {
    $jid = $this->db->escape_string($jid);
    $sql = "
    SELECT
      user.user_id AS 'uid',
      user.username AS 'username',
      joint_group.joint_id AS 'jid',
      joint_group_member.joint_role AS 'role',
      joint_group_member.date_added AS 'joined',
      COUNT(svr_download_request.request_id) AS 'requests'
    FROM joint_group_member
    INNER JOIN user ON user.user_id = joint_group_member.user_id
    INNER JOIN joint_group ON joint_group.joint_id = joint_group_member.joint_id
    INNER JOIN svr_download_request ON svr_download_request.joint_id = joint_group.joint_id AND svr_download_request.user_id = joint_group_member.user_id
    WHERE joint_group_member.joint_id = '$jid'
    GROUP BY joint_group_member.id
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 0 || !$qry) return 0;
    $arr = array();
    while ($jData = mysqli_fetch_assoc($qry)) array_push($arr, $jData);
    return $arr;
  }


  public function getRequestInfo($rid)
  {
    $rid = $this->db->escape_string($rid);
    $sql = "
    SELECT
      svr_download_request.request_id AS 'rid',
      joint_group.joint_id AS 'jid',
      svr_download_request.url AS 'url',
      svr_download_request.max_chunk_size AS 'chunk_size',
      user.user_id AS 'uid',
      svr_download_request.ext AS 'ext',
      svr_download_request.init AS 'status'
    FROM svr_download_request
    INNER JOIN joint_group ON joint_group.joint_id = svr_download_request.joint_id
    INNER JOIN user ON user.user_id = svr_download_request.user_id
    WHERE svr_download_request.request_id = '$rid'
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }


  public function crt_file($arr)
  {
    $jid = $this->db->escape_string($arr['jid']);
    $rid = $this->db->escape_string($arr['rid']);
    $channel = $this->db->escape_string($arr['py_channel']);
    $size = $this->db->escape_string($arr['size']);
    $serverPath = $this->db->escape_string($arr['server_path']);
    $sql = "
      INSERT INTO file(request_id, joint_id, py_channel, server_path, size) VALUES ('$rid', '$jid', '$channel', '$serverPath', '$size');
      UPDATE svr_download_request SET init = '1' WHERE request_id = '$rid' AND joint_id = '$jid';
    ";
    $qry = mysqli_multi_query($this->db, $sql);
    return (($qry) ? true : false);
  }


  public function updateDownloadData($arr)
  {
    $jid = $arr['jid'];
    $rid = $arr['rid'];
    $progress = $arr['progress'];

    if (!empty($arr['md5_hash'])) {
      // Update file complete data
      $md5 = $arr['md5_hash'];
      $sha1 = $arr['sha1_hash'];
      $sha256 = $arr['sha256_hash'];
      $sql = "
        UPDATE svr_download_request SET init = '2' WHERE request_id = '$rid' AND joint_id = '$jid';
        UPDATE file SET md5_hash = '$md5', sha1_hash = '$sha1', sha256_hash = '$sha256' WHERE request_id = '$rid' AND joint_id = '$jid';
      ";
      $qry = mysqli_multi_query($this->db, $sql);
      return (($qry) ? true : $this->db->error);
    } else {
      // Update file download progress
      $sql = "UPDATE file SET progress = '$progress' WHERE joint_id = '$jid' AND request_id = '$rid'";
      $qry = mysqli_query($this->db, $sql);
      return (($qry) ? true : $this->db->error);
    }
  }
}
?>
