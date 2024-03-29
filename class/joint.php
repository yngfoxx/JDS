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


  public function validateGroup($jID) {
    $sql = "SELECT joint_id FROM joint_group WHERE joint_id = '$jID'";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return true;
    return false;
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
    $bytes = $this->db->escape_string($arr['bytes']); # File size
    $max_chunk_size = (isset($arr['max_chunk_size'])) ? $this->db->escape_string($arr['max_chunk_size']) : 5;
    $sql = "
      INSERT INTO svr_download_request (joint_id, user_id, url, ext, size, bytes, max_chunk_size)
      VALUES('$jid', '$uid', '$url', '$ext', '$size', '$bytes', '$max_chunk_size');
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? $this->db->insert_id : false); // return ID of inserted row
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


  /*
   Get users' joint group list
  */
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


  /*
   Get all downloads in joint group
  */
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
    ORDER BY request_datetime DESC
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
      joint_group_member.date_added AS 'joined'
    FROM joint_group_member
    INNER JOIN user ON user.user_id = joint_group_member.user_id
    INNER JOIN joint_group ON joint_group.joint_id = joint_group_member.joint_id
    WHERE joint_group_member.joint_id = '$jid'
    GROUP BY joint_group_member.id
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 0 || !$qry) return 0;
    $arr = array();
    while ($jData = mysqli_fetch_assoc($qry)) array_push($arr, $jData);
    return $arr;
  }


  public function getRequestInfo($rid, $jid)
  {
    $rid = $this->db->escape_string($rid);
    $jid = $this->db->escape_string($jid);
    $sql = "
    SELECT
      svr_download_request.request_id AS 'rid',
      joint_group.joint_id AS 'jid',
      svr_download_request.url AS 'url',
      svr_download_request.max_chunk_size AS 'chunk_size',
      svr_download_request.bytes AS 'bytes',
      user.user_id AS 'uid',
      svr_download_request.ext AS 'ext',
      svr_download_request.init AS 'status'
    FROM svr_download_request
    INNER JOIN joint_group ON joint_group.joint_id = svr_download_request.joint_id
    INNER JOIN user ON user.user_id = svr_download_request.user_id
    WHERE svr_download_request.request_id = '$rid'
    AND joint_group.joint_id = '$jid'
    ";
    $qry = mysqli_query($this->db, $sql);
    if (mysqli_num_rows($qry) == 1) return mysqli_fetch_assoc($qry);
    return false;
  }


  /*
   Store file basic info in database
  */
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


  /*
   Update the data of the in progress download from python script
  */
  public function updateFileData($arr)
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


  /*
   Update state of server downloaded data from python scripts
  */
  public function updateDownloadData($arr)
  {
    $jid = $arr['jid'];
    $rid = $arr['rid'];
    $status_txt = $arr['stat'];
    $status = ($status_txt == 'compressing') ? 3 : ( ($status_txt == 'splitting') ? 4 : ( ($status_txt == 'chunkified') ? 5 : null ) );
    if ($status == null) return false;
    $sql = "UPDATE svr_download_request SET init = '$status' WHERE joint_id = '$jid' AND request_id = '$rid'";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? true : $this->db->error);
  }


  /*
   Split the bytes into percentile portions
  */
  public function splitBytesByPercentile($bytes, $percentile)
  {
    $percentile_chunk = ($bytes * $percentile) / 100;
    $percentIntrator = 0;
    $chunks = [];
    while ($percentIntrator < $bytes) {
      $percentIntrator += $percentile_chunk;
      $chunks[] = $percentIntrator;
    }
    return $chunks;
  }


  /*
   Split file into chunks of
   bytes with this method
  */
  public function crt_chunks($chunk)
  {
    $chnkID = $chunk['chunk_order'];
    $chnkJID = $chunk['joint_id'];
    $chnkRID = $chunk['request_id'];
    $chnkBSTART = $chunk['byte_start'];
    $chnkBEND = $chunk['byte_end'];
    $error = array();
    $sql = "
      INSERT INTO chunk(chunk_order, joint_id, request_id, byte_start, byte_end)
      VALUES ('$chnkID', '$chnkJID', '$chnkRID', '$chnkBSTART', '$chnkBEND')
    ";
    $qry = mysqli_query($this->db, $sql);
    $ch_chnkID = $this->db->insert_id;
    if ($qry) {
      $chnkCHILDREN = $chunk['children'];
      foreach ($chnkCHILDREN as $key => $chnk) {
        $ch_chnkORDER = $chnk['ch_chunk_order'];
        $ch_chnkBSTART = $chnk['ch_chunk_start'];
        $ch_chnkBEND = $chnk['ch_chunk_end'];
        $ch_chnkUID = $chnk['uID'];
        $sql = "
          INSERT INTO chunk_child(chunk_id, chunk_order, byte_start, byte_end, user_id)
          VALUES ('$ch_chnkID', '$ch_chnkORDER', '$ch_chnkBSTART', '$ch_chnkBEND', '$ch_chnkUID')
        ";
        $qry = mysqli_query($this->db, $sql);
        if (!$qry) array_push($error, array('server_error' => $this->db->error));
      }
    }
    return (count($error) == 0);
  }


  /*
   Get all parent chunks of a
   splitted file in database
  */
  public function getChunks($arr)
  {
    $chnkJID = $arr['joint_id'];
    $chnkRID = $arr['request_id'];
    $sql = "
      SELECT
        chunk.id AS 'chunk_id',
        chunk.chunk_order AS 'order_name',
        joint_group.joint_id AS 'jid',
        svr_download_request.request_id AS 'rid',
        chunk.byte_start AS 'byte_start',
        chunk.byte_end AS 'byte_end'
      FROM chunk
      INNER JOIN joint_group ON joint_group.joint_id = chunk.joint_id
      INNER JOIN svr_download_request ON svr_download_request.request_id = chunk.request_id
      WHERE chunk.request_id = '$chnkRID'
      AND joint_group.joint_id = '$chnkJID'
    ";
    $qry = mysqli_query($this->db, $sql);
    if ($qry && mysqli_num_rows($qry) > 0) {
      $response = array();

      // Merge all downloaded chunk size
      while ($arr = mysqli_fetch_assoc($qry)) {
        $tempArray = $arr;
        $chnkChildren = $this->getChunkChildrenByChunkId($arr['chunk_id']);
        if ($chnkChildren != false) {
          $chnkChildSize = 0;
          for ($i=0; $i < count($chnkChildren); $i++) {
            if ($chnkChildren[$i]['downloaded']) $chnkChildSize = $chnkChildSize + $chnkChildren[$i]['downloaded'];
          }
          $tempArray['downloaded'] = $chnkChildSize;
        }
        $response[] = $tempArray;
      }

      return $response;
    }
    return false;
  }


  /*
   Get children chunk of a
   bigger chunk by chunk ID
  */
  public function getChunkChildrenByChunkId($chnkID)
  {
    $sql = "
      SELECT
        chunk_child.chunk_order AS 'order',
        chunk_child.byte_start AS 'byte_start',
        chunk_child.byte_end AS 'byte_end',
        chunk_child.progress AS 'download_progress',
        chunk_child.size AS 'downloaded',
        chunk_child.user_id AS 'uid'
      FROM chunk_child
      WHERE chunk_child.chunk_id = '$chnkID'
    ";
    $qry = mysqli_query($this->db, $sql);
    if ($qry && mysqli_num_rows($qry) > 0) {
      $response = array();
      while ($arr = mysqli_fetch_assoc($qry)) $response[] = $arr;
      return $response;
    }
    return false;
  }


  /*
   Get all server downloaded files that
   have been split into chunks in database
  */
  public function getChunkedFiles($chData)
  {
    $chnkJID = $chData['joint_id'];
    $chnkRID = $chData['request_id'];
    $sql = "
      SELECT *
      FROM svr_download_request
      WHERE request_id = '$chnkRID' AND joint_id = '$chnkJID' AND (init = 4 OR init = 5)
    ";
    $qry = mysqli_query($this->db, $sql);
    if ($qry && mysqli_num_rows($qry) > 0) return mysqli_fetch_assoc($qry);
    return false;
  }


  /*
    Update child chunk data
  */
  public function updateChildChunk($arr)
  {
    $chunkID = $arr['chunkCID'];
    $chunkOrder = $arr['chunkOID'];
    $chunkSize = $arr['chunkSIZE'];
    $chunkProgress = $arr['chunkPROGRESS'];
    $sql = "
      UPDATE chunk_child
      SET progress = '$chunkProgress', size = '$chunkSize'
      WHERE chunk_id = '$chunkID' AND chunk_order = '$chunkOrder'
    ";
    $qry = mysqli_query($this->db, $sql);
    return (($qry) ? true : $this->db->error);
  }
}
?>
