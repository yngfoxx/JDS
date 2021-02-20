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
      // ----------------------------------------------------------------------<

      // Add user to group as owner -------------------------------------------<
      $arrGRP = array('jid' => $jointID, 'uid' => $userID, 'role' => 'owner');
      if ($jds->group_add_member($arrGRP)) {
        // Add requested file to server download request
        # Create new download request from URL recieved -----------------------\/
        $arrSVR = array(
          'jid' => $jointID,
          'uid' => $userID,
          'url' => $data,
          'ext' => $result['extension'],
          'size' => $result['size'],
          'max_chunk_size' => 'auto' // put default at first
        );
        $crt = $jds->crt_download($arrSVR);
        if ($crt != false) {
          $result['svrID'] = $crt;
          echo json_encode($result); // end of process
        } else {
          $result = array('server_error' => "Unrecoverable error v2!");
          echo json_encode($result);
        }
        # ---------------------------------------------------------------------/\
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
      // Not an HTTP URL [CHECK IF group code exists]
      $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
      if ($jds->validateGroup($data)) {
        // check if user is a member of the group
        $members = $jds->getJointMembers($data);
        $isMember = false;
        for ($i=0; $i < sizeof($members); $i++) {
          if ($members[$i]['uid'] == $userID) {
            $isMember = true;
            break;
          }
        }
        if (!$isMember) {
          $arrGRP = array('jid' => $data, 'uid' => $userID, 'role' => 'member');
          if ($jds->group_add_member($arrGRP)) {
            echo json_encode(array('isMember' => true, 'jid' => $data, 'type' => 'code', 'isNew' => true)); exit();
          }
          echo json_encode(array('isMember' => false, 'jid' => $data, 'type' => 'code')); exit();
        }
        // User is a member of the group
        echo json_encode(array('isMember' => true, 'jid' => $data, 'type' => 'code')); exit();

      } else {
        echo "group code does not exist";
        exit();
      }
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

    $GROUPDATA['UID'] = $userID;

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
  if (isset($_POST['jdsInit'])) {
    if (!$_POST['jdsInit']) exit();
    // TODO: Initialize joint download
    /*
    #-> File authenticity check
    #
    #-> Create socket channel ID
    #
    #-> Store necessary file data
    */
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

    // Necessary variables
    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
    $requestID = $std->db->escape_string($_POST['rid']);
    $jointID = $std->db->escape_string($_POST['jid']);

    // Authenticating request from client -------------------------------------<
    $requestData = $jds->getRequestInfo($requestID);
    $jointData = $jds->getJointInfo($jointID);

    if (!$requestData || !$jointData) {
      $result = array('server_error' => "Not found!", 'code' => '404'); // request id or joint group id not found
      echo json_encode($result);
      exit();
    }

    if ($requestData['jid'] != $jointID) {
      $result = array('server_error' => "ID match not found!", 'code' => '500'); // request id does not belong to the joint group
      echo json_encode($result);
      exit();
    }
    // ------------------------------------------------------------------------<


    // FILE AUTHENTICITY CHECK ------------------------------------------------>
    $file_url = $requestData['url'];
    if (!$std->scanURL($file_url)) {
      $result = array('server_error' => "File at URL not found!", 'code' => '404'); // request id or joint group id not found
      echo json_encode($result);
      exit();
    }

    // database fields : rid, jid, file_path, size, MD5, SHA1, SHA256, progress
    $fileName = pathinfo($file_url, PATHINFO_FILENAME); # source file name
    $fileExtension = pathinfo($file_url, PATHINFO_EXTENSION); # source file name
    // $socketChannel = $std->makeNumericKey(6); // Get joint group socket channel
    $socketChannel = $jointData['channel']; // Get joint group socket channel
    // $serverPath = "C:/xampp/htdocs/JDS/storage/$jointID/$requestID/";

    // Make directory to store files per request
    $serverPath = "C:/xampp/htdocs/JDS/storage/$jointID/$requestID/";
    mkdir($serverPath, 0777, true); chmod($serverPath, 0777);

    $fileData = array(
      'jid'         => $jointID,
      'rid'         => $requestID,
      'py_channel'  => $socketChannel,
      'size'        => $std->formatUnit($std->getURLFileSize($file_url)),
      'server_path' => $serverPath
    );
    $response = $jds->crt_file($fileData); // create file data in database
    if ($response) {
      // INITIALIZE PYTHON SCRIPT [Initial failed attempt]
        // $script_path = $_SERVER['DOCUMENT_ROOT'] . '/JDS/req/script.sh';
        //
        // $python_path = 'C:/Users/YoungFox/AppData/Local/Programs/Python/Python39/python.exe';
        //
        // $script_path = $_SERVER['DOCUMENT_ROOT'] . '/JDS/api/grab.py';
        //
        // $code = "$python_path $script_path -u '$file_url' -r '$requestID' -nsp '$socketChannel' -d '$serverPath'";
        //
        // // $result_last_line = Shell_Exec($code.' 2>&1 &');
        //
        // exec("$code 2>&1", $out, $status);
        // if (0 === $status) {
        //     var_dump($out);
        // } else {
        //     echo "Command failed with status: $status";
        // }
        // exit();
        // if ($result_last_line) {
        //   echo "Script is running..";
        // } else {
        //   echo "Script failed to init...";
        // }

      // EXECUTE SCRIPT WITH PYTHON FLASK API (fetch.py) [THIS WORKS BETTER]
      # 127.0.0.1:5000/?url=https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe&rid=12&jid=13RWS2&nsp=1234531&dest=C:\JDS\storage
      $arr = array(
        'url'   => $file_url, // File URL
        'jid'   => $jointID, // File Joint Group ID
        'rid'   => $requestID, // File Request ID
        'nsp'   => $socketChannel, // File Joint Group socket namespace
        'dest'  => $serverPath // File download destination
      );
      $apiResponse = $std->cUrlRequest('http://127.0.0.1:5000/', $arr, 'GET'); // Target Flask API server
      echo $apiResponse; // result is already json encoded
      exit();
    } else {
      $result = array('server_error' => "Unexpected error", 'code' => '500'); // Something unexpected has happened
      echo json_encode($result);
      exit();
    }

    // ------------------------------------------------------------------------>

  }


  # Update MySQL from python flask API
  if (isset($_POST['jdsUpd'])) {
    if ($_POST['jdsUpd'] != 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs') {
      $result = array('server_error' => "Unexpected origin of request", 'code' => '500'); // invalid request origin
      echo json_encode($result);
      exit();
    }
    /* payload = {
        'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
        'data': {
            'joint_id': JOINT_ID,
            'request_id': REQUEST_ID,
            'progress': 100,
            'status': 'Completed',
            'download_path': obj.get_dest(),
            'download_time_length': obj.get_dl_time(human=True),
            'MD5': obj.get_data_hash('md5'),
            'SHA1': obj.get_data_hash('sha1'),
            'SHA256': obj.get_data_hash('sha256')
        }
    } */
    $arr = array();
    $arr['jid'] = $std->db->escape_string($_POST['joint_id']);
    $arr['rid'] = $std->db->escape_string($_POST['request_id']);
    $arr['progress'] = $std->db->escape_string($_POST['progress']);
    $arr['status'] = $std->db->escape_string($_POST['status']);
    $arr['md5_hash'] = (isset($_POST['md5_hash'])) ? $std->db->escape_string($_POST['md5_hash']) : '';
    $arr['sha1_hash'] = (isset($_POST['sha1_hash'])) ? $std->db->escape_string($_POST['sha1_hash']) : '';
    $arr['sha256_hash'] = (isset($_POST['sha256_hash'])) ? $std->db->escape_string($_POST['sha256_hash']) : '';

    $response = $jds->updateDownloadData($arr);
    echo $response;


    // Update MySQL with new data
  }

  if (isset($_POST['crtDownload'])) {
    // Add requested file to server download request
    $jointID = $std->db->escape_string($_POST['jointID']);
    $userID = $auth->getUserIdByDeviceID($_COOKIE['dKEY']);
    $url = $std->db->escape_string($_POST['url']);

    // EXIT CODE IF URL IS NOT VALID
    if (!filter_var($url, FILTER_VALIDATE_URL)) exit();

    $ext = $std->db->escape_string($_POST['ext']);
    $realSize = $std->db->escape_string($_POST['realSize']);
    $formattedSize = $std->formatUnit($realSize);
    $fileOrigin = $_POST['origin']; // object contains url broken into scheme, host and path

    # Create new download request from URL recieved -----------------------\/
    $arrSVR = array(
      'jid' => $jointID,
      'uid' => $userID,
      'url' => $url,
      'ext' => $ext,
      'size' => $formattedSize,
      'max_chunk_size' => 'auto' // put default at first
    );
    $crt = $jds->crt_download($arrSVR);
    if ($crt != false) {
      $result['svrID'] = $crt;
      echo json_encode($result); // end of process
    } else {
      $result = array('server_error' => "Unrecoverable error v2!");
      echo json_encode($result);
    }
    # ---------------------------------------------------------------------/\
  }
  //////////////////////////////////////////////////////////////////////////////
} else if ($_SERVER['REQUEST_METHOD'] == "GET") {
  if (isset($_GET['groupCheck'])) {
    if (empty($_GET['groupCheck'])) exit();
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
    $jID = $std->db->escape_string($_GET['groupCheck']);

    $res = ($jds->validateGroup($jID) == true) ? true : false;
    $result = array('response' => $res, 'jid' => $jID);
    echo json_encode($result);
    exit();
  }
}
?>
