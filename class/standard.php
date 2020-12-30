<?php
// Database configuration ----------------------------------------------------------------->
if (!defined('DB_SERVER')) require $_SERVER['DOCUMENT_ROOT'] . '/JDS/config/db_config.php';
// ---------------------------------------------------------------------------------------->

/**
 *  Class to handle all site settings
 */
class stdlib {

  function __construct() {
    $this->db = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE); // connect to database
    if (mysqli_connect_error()) {
      echo "Error: Failed to connect to database.";
      exit;
    }
  }



  public function getIP()
  {
    // IP USAGE METHODS ---------------------------------------------------------
      #\> ASSIGN API OBJECT
        #-> $ipdat = @json_decode(file_get_contents("http://www.geoplugin.net/json.gp?ip=" . $THE_VARIABLE_THAT_STORES_THE_IP));
            # echo 'Country Name: ' . $ipdat->geoplugin_countryName . "<br>";
            # echo 'City Name: ' . $ipdat->geoplugin_city . "<br>";
            # echo 'Continent Name: ' . $ipdat->geoplugin_continentName . "<br>";
            # echo 'Latitude: ' . $ipdat->geoplugin_latitude . "<br>";
            # echo 'Longitude: ' . $ipdat->geoplugin_longitude . "<br>";
            # echo 'Currency Symbol: ' . $ipdat->geoplugin_currencySymbol . "<br>";
            # echo 'Currency Code: ' . $ipdat->geoplugin_currencyCode . "<br>";
            # echo 'Timezone: ' . $ipdat->geoplugin_timezone;
    // --------------------------------------------------------------------------
    $ip = (!empty($_SERVER['HTTP_CLIENT_IP'])) ? $_SERVER['HTTP_CLIENT_IP'] : ((!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) ? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR']);
    return $ip;
  }



  public function makeKey($length) {
    // MAKE KEY -----------------------------------------------------------------
      # Generates random strings with given length
    // --------------------------------------------------------------------------
    $str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    return substr(str_shuffle($str), 0, $length);
  }


  public function makeNumericKey($length) {
    // MAKE KEY -----------------------------------------------------------------
      # Generates random integers with given string length
    // --------------------------------------------------------------------------
    $str = '0123456789';
    return substr(str_shuffle($str), 0, $length);
  }


  public function makeUpperKey($length) {
    // MAKE KEY -----------------------------------------------------------------
      # Generates random strings with given length
    // --------------------------------------------------------------------------
    $str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    return substr(str_shuffle($str), 0, $length);
  }


  public function isImage($imagePath)
  {
    // VALIDATE IMAGE -----------------------------------------------------------
      # Check if file in path is an image
    // --------------------------------------------------------------------------
    $a = getimagesize($imagePath);
    $image_type = $a[2]; // gets the image type
    return in_array($image_type , array(IMAGETYPE_GIF , IMAGETYPE_JPEG ,IMAGETYPE_PNG , IMAGETYPE_BMP));
  }



  public function isVideo($fileType)
  {
    // VALIDATE VIDEO -----------------------------------------------------------
      # Check if file is a video by type
    // --------------------------------------------------------------------------
    $arr = array(
      "video/mp4",
      "video/wav",
      "video/webM",
    );
    return in_array($fileType, $arr);
  }



  public function compressImage($source, $destination, $quality) {
    // IMAGE COMPRESSION --------------------------------------------------------
      # Compress image and store image in destination path
    // --------------------------------------------------------------------------
    $info = getimagesize($source);

    if ($info['mime'] == 'image/jpeg') {
      $image = imagecreatefromjpeg($source);
    } else
    if ($info['mime'] == 'image/gif') {
      $image = imagecreatefromgif($source);
    } else
    if ($info['mime'] == 'image/png') {
      $image = imagecreatefrompng($source);
    }
    return imagejpeg($image, $destination, $quality);
  }


  public function sendHeaders($file, $type, $name=NULL)
  // SEND HEADERS -------------------------------------------------------------
    # Send headers for proper request
    # source: https://zinoui.com/blog/download-large-files-with-php
  // --------------------------------------------------------------------------
  {
    if (empty($name))
    {
        $name = basename($file);
    }
    header('Pragma: public');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Cache-Control: private', false);
    header('Content-Transfer-Encoding: binary');
    header('Content-Disposition: attachment; filename="'.$name.'";');
    header('Content-Type: ' . $type);
    header('Content-Length: ' . filesize($file));
  }


  public function downloadFile($path,$retbytes=true) {
  // DOWNLOAD FILE CHUNKS ----------------------------------------------------
    # Read and save file in chunks
    # source: https://www.tutorialspoint.com/how-to-download-large-files-through-php-script
  // --------------------------------------------------------------------------
   $chunksize = 1*(1024*1024); // how many bytes per chunk the user wishes to read
   $buffer = '';
   $cnt = 0;
   $handle = fopen($path, 'rb'); // get file from url

   $result = array();

   if ($handle === false) return false;

   // GET FILE DETAILS
   $ext = pathinfo($path, PATHINFO_EXTENSION); // file extension
   $filename = pathinfo($path, PATHINFO_FILENAME); // file name
   $newf = fopen ($filename.".".$ext, 'wb'); // create file destination on server
   $filePath = $_SERVER['DOCUMENT_ROOT'] . '/JDS/req/'.$filename.'.'.$ext;

   while (!feof($handle)) {
      $buffer = fread($handle, $chunksize); // chunks
      fwrite($newf, $buffer); // write chunks to file on server
      // echo $buffer; // display chunk output
      if ($retbytes) {
         $cnt += strlen($buffer);
      }
   }
   $status = fclose($handle);
   if ($newf) fclose($newf);
   if ($retbytes && $status) {
     // successful
     $result['bytes'] = $cnt; // return number of bytes delivered like readfile() does.
     $result['filename'] = $filename;
     $result['extension'] = $ext;
     return $result;
   }

   // something happened
   return $status;
  }


  function scanURL($url) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_NOBODY, true);
    curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $status = ($code == 200) ? true : false;
    curl_close($ch);
    return $status;
  }

  public function getURLFileSize($URL)
  {
    $ch = curl_init($URL);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_HEADER, TRUE);
    curl_setopt($ch, CURLOPT_NOBODY, TRUE);

    $data = curl_exec($ch);
    $size = curl_getinfo($ch, CURLINFO_CONTENT_LENGTH_DOWNLOAD);
    $fileIp = curl_getinfo($ch, CURLINFO_PRIMARY_IP);

    curl_close($ch);
    return $size;
  }


  public function formatUnit($bytes)
  {
    if ($bytes >= 1073741824)
    {$bytes = number_format($bytes / 1073741824, 2) . ' GB';}
    elseif ($bytes >= 1048576)
    {$bytes = number_format($bytes / 1048576, 2) . ' MB';}
    elseif ($bytes >= 1024)
    {$bytes = number_format($bytes / 1024, 2) . ' KB';}
    elseif ($bytes > 1)
    {$bytes = $bytes . ' bytes';}
    elseif ($bytes == 1)
    {$bytes = $bytes . ' byte';}
    else
    {$bytes = '0 bytes';}
    return $bytes;
  }


  public function startsWith ($string, $startString) {
    $len = strlen($startString);
    return (substr($string, 0, $len) === $startString);
  }

  public function endsWith($string, $endString) {
    $len = strlen($endString);
    if ($len == 0) {
      return true;
    }
    return (substr($string, -$len) === $endString);
  }

  public function file_get_contents_curl($url) {
      $ch = curl_init();

      curl_setopt($ch, CURLOPT_HEADER, 0);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
      curl_setopt($ch, CURLOPT_URL, $url);
      curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);

      $data = curl_exec($ch);
      curl_close($ch);

      return $data;
  }

  public function getMeta($url)
  {
    // metadata object
    $metaData = array();

    // Clean URL
    $domain = parse_url($url)['host'];
    $html = $this->file_get_contents_curl($url);

    // fetch HTML contents
    $doc = new DOMDocument();
    @$doc->loadHTML($html);
    $nodes = $doc->getElementsByTagName('title');

    // LINK TAGS -------------------------------------------------------------->
    $links = $doc->getElementsByTagName('link');
    for ($x = 0; $x < $links->length; $x++)
    {
      $link = $links->item($x);
      if ($link->getAttribute('rel') == 'icon') {
        $metaData['icon'] = $link->getAttribute('href');
      }
    }
    // ------------------------------------------------------------------------>


    // META TAGS -------------------------------------------------------------->
    $metas = $doc->getElementsByTagName('meta');
    $metaData['title'] = $nodes->item(0)->nodeValue;
    for ($i = 0; $i < $metas->length; $i++)
    {
      $meta = $metas->item($i);
      if ($meta->getAttribute('property') == 'og:image') {
        $metaData['image'] = $meta->getAttribute('content');
        if (!$this->startsWith($metaData['image'], 'http')){
          $metaData['image'] = "https://".$domain."/".$meta->getAttribute('content');
        }
      } else if ($meta->getAttribute('itemprop') == 'image') {
        $metaData['image'] = $meta->getAttribute('content');
        if (!$this->startsWith($metaData['image'], 'http')){
          $metaData['image'] = "https://".$domain."/".$meta->getAttribute('content');
        }
      }

      if ($meta->getAttribute('name') == 'description') {
        $metaData['description'] = $meta->getAttribute('content');
      }

      if ($meta->getAttribute('name') == 'keywords') {
        $metaData['keywords'] = $meta->getAttribute('content');
      }
    }
    // ------------------------------------------------------------------------>

    return $metaData;
  }


  // PHP CURL REQUEST -------------------------------------------------------->
  function cUrlRequest($url, $arr, $method) {
    if ($method == 'GET') {
      // GET request
      $cURLConnection = curl_init();
      $serial = $url.'?';
      $arrCount = count($arr);
      $count = 0;
      foreach ($arr as $key => $value) {
        $serial = $serial.''.$key.'='.$value;
        if($count != $arrCount) $count += 1;
        if($count < $arrCount) $serial = $serial.'&';
      }
      curl_setopt($cURLConnection, CURLOPT_URL, $serial);
      curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
    } else if ($method == 'POST') {
      // POST request
      $cURLConnection = curl_init($url);
      curl_setopt($cURLConnection, CURLOPT_POSTFIELDS, $postRequest);
      curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
    }

    $response = curl_exec($cURLConnection);
    curl_close($cURLConnection);

    return $response;
  }
  // ------------------------------------------------------------------------>
}

?>
