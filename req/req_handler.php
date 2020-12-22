<?php
session_start();

// PACKAGES ---------------------------
include_once $_SERVER['DOCUMENT_ROOT']. '/JDS/class/standard.php';
include_once $_SERVER['DOCUMENT_ROOT']. '/JDS/class/auth.php';
include_once $_SERVER['DOCUMENT_ROOT']. '/JDS/class/joint.php';
include $_SERVER['DOCUMENT_ROOT']. "/JDS/class/class.easyzip.php";
// ------------------------------------


// OBJECTS [reusable] -----------------
$std = new stdlib();
$auth = new auth();
$jds = new jointlib();
$result = array();
// ------------------------------------

/*
  This file handles POST and GET requests
*/

if ($_SERVER['REQUEST_METHOD'] == "POST") {
  // POST request handler //////////////////////////////////////////////////////
  if (isset($_POST['regUser'])) { // REGISTER USER //
    // PASSWORD CHECK ---------------------------------<
    $pass = $std->db->escape_string(($_POST['password'] == $_POST['passConf']) ? $_POST['password'] : null);
    if ($pass == null) {
      $result["server_error"] = "Passwords do not match";
      echo json_encode($result);
      exit();
    }

    // EMAIL CHECK ------------------------------------<
    $email = $std->db->escape_string($_POST['email']);
    if ($auth->getUserByEmail($email)) {
      $result["server_error"] = "Email already in use!";
      echo json_encode($result);
      exit();
    }
    // ------------------------------------------------<


    // USERNAME CHECK ---------------------------------<
    $username = $std->db->escape_string($_POST['username']);
    if ($auth->getUserByUserName($username)) {
      $result["server_error"] = "Username already in use!";
      echo json_encode($result);
      exit();
    }
    // ------------------------------------------------<


    // CREATE USER ACCOUNT ----------------------------------------------------<
    # only recieved 3 variables from user
    #  > USERNAME
    #  > EMAIL
    #  > PASSWORD

    # GENERATE ENCRYPTED PASSWORD AND HASH
    $hash = $std->makeKey(12);
    $crypt_key = $auth->keyCry($pass, $hash);

    // > STORE USER IN DATABASE
    $arr = array(
      "username" => $username,
      "email" => $email,
      "key" => $crypt_key,
      "hash" => $hash
    );
    if ($auth->makeUser($arr))
      $result["msg"] = "User account has been created successfully, you may login right away!";
      echo json_encode($result);
      exit();
  }
  else
  if (isset($_POST['logUser'])) { // LOG USER //
    // EMAIL CHECK ------------------------------------------------------------>
    $email = $std->db->escape_string($_POST['email']);
    if (!$auth->getUserByEmail($email)) {
      $result["server_error"] = "The email you entered does not exists or the password is incorrect!";
      echo json_encode($result);
      exit();
    }
    // ------------------------------------------------------------------------>

    $userData = $auth->getUserByEmail($email);

    // PASSWORD CHECK --------------------------------------------------------->
    $pass = $std->db->escape_string($_POST['password']);
    if ($auth->keyCheck($pass, $userData['hash'], $userData['password'])) {
      # ACCESS GRANTED TO USER, CREATE COOKIE AUTH KEY
      $device_key = bin2hex(openssl_random_pseudo_bytes(64));
      $dk_arr = array(
        "uid" => $userData['user_id'],
        "dk" => $device_key
      );
      if ($auth->crtDeviceID($dk_arr)) {
        setcookie('dKEY', base64_encode($device_key), strtotime( '+30 days' ), '/', null, null, true); //create httponly cookie lasts for 30 days
      } else {
        $result["server_error"] = "Failed to complete login process.";
        echo json_encode($result);
        exit();
      }

      # CREATE SESSION VARIABLES
      $_SESSION['userID'] = $userData['user_id'];
      $_SESSION['logged_in'] = true;
      echo true;
      exit();
    }
    // ------------------------------------------------------------------------>
  }
  // --------------------------------------------------------------------------------------------->



  // JOINT DOWNLOAD SYSTEM BRAIN // ------------------------------------------->
  if (isset($_POST['path_code'])) {
    /*
    * OBJECTIVE OF THIS CODE BLOCK
    * [1] Receive data from user
    * [2] Identify data category [JDS Code / Download URL]

    *
      (1) Download URL:
          - Check if URL is valid and secure
          - Get target file meta-info for advanced processing
          - Generate temporary JDS access code and store in database
          - Send URL to Python API (api/grab.py) for file downloading.
      (2) JDS Code:
          - Verify code
          - Grant view access to file chunks
    *
    */

    // SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
    if (isset($_COOKIE['dKEY'])) {
      if (!$auth->verfUser($_COOKIE['dKEY'])) {
        $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
        echo json_encode($result);
        exit();
      }
    } else {
      $result = array('server_error' => "Invalid URL", 'code' => '403'); // forbidden
      echo json_encode($result);
      exit();
    }

    $data = urldecode($std->db->escape_string($_POST['path_code']));
    # check if path_code is a URL or code
    if (filter_var($data, FILTER_VALIDATE_URL)) {
    //------------------------------------------------------------------------\\
    #                        |========================|                        #
    #                    //--| URL RECEIVED FROM USER |--\\                    #
    #                        |========================|                        #
    //------------------------------------------------------------------------\\

      /* $metaData = $std->getMeta($data); # fetch URL metadata */

      // Basic data ----------------------------------------------------------<
      $result['input'] = "$data"; # input recieved from user
      $result['type'] = "URL"; # request type
      // ---------------------------------------------------------------------<


      // Domain check --------------------------------------------------------<
      $result['origin'] = parse_url($data); # source base URL
      if (empty($result['origin']['path'])) {
        $result = array('server_error' => "Failed to get a downloadable file");
        echo json_encode($result);
        exit();
      }
      // ---------------------------------------------------------------------<


      // File extension check ------------------------------------------------<
      $result['extension'] = pathinfo($data, PATHINFO_EXTENSION); # source file extension
      if (empty($result['extension'])) {
        $result = array('server_error' => "Invalid URL");
        echo json_encode($result);
        exit();
      }
      // ---------------------------------------------------------------------<


      // File data -----------------------------------------------------------<
      $result['filename'] = pathinfo($data, PATHINFO_FILENAME); # source file name
      $result['size'] = $std->formatUnit($std->getURLFileSize($data)); # format source file size
      $result['realSize'] = $std->getURLFileSize($data); # source file real size
      // ---------------------------------------------------------------------<


      // File validity check -------------------------------------------------<
      if ($result['realSize'] == "-1") {
        $result = array('server_error' => "Failed to get a downloadable file");
        echo json_encode($result);
        exit();
      }
      // ---------------------------------------------------------------------<


      // Source Meta data -----------------------------------------------------<
      // $html = $std->file_get_contents_curl($result['origin']);
      // $result['html'] = $html;
      // ----------------------------------------------------------------------<


      # At this point we know that there is a downloadable file from the URL
      # next thing to do is to create the Joint Group
      // Create Joint Group ---------------------------------------------------<
      $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
      $jointID = $jds->crt_group($userID); // Create joint group ID

      $result['jdsID'] = ($jointID != false) ? $jointID : false;
      if ($result['jdsID'] == false) {
        $result = array('server_error' => "Unrecoverable error!");
        echo json_encode($result);
        exit();
      }

      // Add user to J0INT group as owner -------------------------------------<
      $arrGRP = array('jid' => $jointID, 'uid' => $userID, 'role' => 'owner');
      if ($jds->group_add_member($arrGRP)) {
        // Add requested file to server download request
        $arrSVR = array(
          'jid' => $jointID,
          'uid' => $userID,
          'url' => $data,
          'ext' => $result['extension'],
          'max_chunk_size' => 5 // put default at first
        );
        $crt = $jds->crt_download($arrSVR);
        if ($crt != false) {
          $result['svrID'] = $crt;
          echo json_encode($result); // end of process
        } else {
          $result = array('server_error' => "Unrecoverable error v2!");
          echo json_encode($result);
        }
      } else {
        $result = array('server_error' => "Unrecoverable error v3!");
        echo json_encode($result);
      }
      // ----------------------------------------------------------------------<

      # parse data to MySQL and python

      // // downloaded file info
      // $arr = $std->downloadFile($data);
      // $filesize = $arr['bytes'];
      // $filename = $arr['filename'];
      // $extension = $arr['extension'];
      // if ($arr) {
      //   // generate JDS code and store data in db
      //   $JDS = $std->makeKey(6);
      //   //| Process JDS creation |**************************************//
      //   /*
      //
      //    Code here...
      //
      //    */
      //     // Move files to appropriate folders
      //     $fPATH = "../adv/jnt/$JDS"; # new directory path
      //     $a = mkdir($fPATH); if (!$a) { exit(); } # create the directory
      //     $FPATH = $fPATH."/".$arr['filename'].'.'.$arr['extension']; # new file path
      //     $a = rename("../req/".$arr['filename'].'.'.$arr['extension'], $FPATH); # move the downloaded file to new path
      //     if (!$a) { exit(); }
      // }

      // ZIP and SPLIT --------------------------------------------------------->
      // $zip = new EasyZIP;
      // $zip->addFile($FPATH); // Add file by path
      // $zip->splitFile("../adv/jnt/".$JDS."/JDS_".$JDS."_FILE.zip", 1048576);
      // $del = unlink($FPATH);
      // if ($del) {
      //
      // }
      // $zip->splitFile("a_zip_file.zip", 10485);
      # SOURCE: https://www.phpclasses.org/package/1900-PHP-Zip-split-large-file-into-smaller-parts-.html
      // ----------------------------------------------------------------------->

    } else {
      // Not an HTTP URL
      echo "checking if code exists";
    }
  }

  # group delete request
  if (isset($_POST['delReq'])) {
    if (!$_POST['delReq']) exit();
    // SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
    if (isset($_COOKIE['dKEY'])) {
      if (!$auth->verfUser($_COOKIE['dKEY'])) {
        $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
        echo json_encode($result);
        exit();
      }
    } else {
      $result = array('server_error' => "Access violation detected! v2", 'code' => '403'); // forbidden
      echo json_encode($result);
      exit();
    }
    $jointID = $std->db->escape_string($_POST['jdsID']);
    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
    $arr = array('uid' => $userID, 'jid' => $jointID);
    echo $jds->del_group($arr);
    exit();
  }


  # max chunk modification
  if (isset($_POST['modChunk'])) {
    if (!$_POST['modChunk']) exit();
    // SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
    if (isset($_COOKIE['dKEY'])) {
      if (!$auth->verfUser($_COOKIE['dKEY'])) {
        $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
        echo json_encode($result);
        exit();
      }
    } else {
      $result = array('server_error' => "Access violation detected! v2", 'code' => '403'); // forbidden
      echo json_encode($result);
      exit();
    }

    $svrID = $std->db->escape_string($_POST['svr']); // download request ID
    $size = $std->db->escape_string($_POST['vol']);
    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);

    $arr = array('uid' => $userID, 'svrID' => $svrID, 'size' => $size);
    echo $jds->set_max_chunk($arr);
    exit();
  }


  # get list of joint groups current user belongs to
  if (isset($_POST['groupList'])) {
    if (!$_POST['groupList']) exit();
    // SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
    if (isset($_COOKIE['dKEY'])) {
      if (!$auth->verfUser($_COOKIE['dKEY'])) {
        $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
        echo json_encode($result);
        exit();
      }
    } else {
      $result = array('server_error' => "Access violation detected! v2", 'code' => '403'); // forbidden
      echo json_encode($result);
      exit();
    }

    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
    $jointList = $jds->getUserJointList($userID);
    if ($jointList == 0) { echo 0; } else {
      echo json_encode($jointList);
    }
  }

  # get group details, members and download requests
  if (isset($_POST['jdsCheck'])) {
    // SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
    if (isset($_COOKIE['dKEY'])) {
      if (!$auth->verfUser($_COOKIE['dKEY'])) {
        $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
        echo json_encode($result);
        exit();
      }
    } else {
      $result = array('server_error' => "Access violation detected! v2", 'code' => '403'); // forbidden
      echo json_encode($result);
      exit();
    }

    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
    $jointID = $std->db->escape_string($_POST['jdsCheck']);
    $GROUPDATA = array();

    $jointInfo = $jds->getJointInfo($jointID); # Group info
    if ($jointInfo == false) {
      $result = array('server_error' => "group does not exist", 'code' => '404'); // group not found
      echo json_encode($result);
      exit();
    }

    // add group information to output
    $GROUPDATA['info'] = $jointInfo;

    $jointMembers = $jds->getJointMembers($jointID); # Group members
    // add members data to output
    $GROUPDATA['member'] = $jointMembers;

    $jointDownloadList = $jds->getJointDownloadList($jointID);  # Download requests
    // add list to output array if it's not empty
    $GROUPDATA['download'] = ($jointDownloadList == 0) ? 0 : $jointDownloadList;

    // output
    echo json_encode($GROUPDATA);
  }


  # initialize download request
  if (isset($_POST['joint_init'])) {
    // TODO: Initialize joint download
  }

  //////////////////////////////////////////////////////////////////////////////
}
?>
