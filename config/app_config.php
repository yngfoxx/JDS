<?php
/**
* Stephen's comment terminologies
* (inRel -> var) means in relation to a variable
**/

// fetch required files
require_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/config/db_config.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
/**
 *  Class to handle all site settings
 */
class app extends stdlib {

  public $app_ID; // recieve app id from parenthesis

  function __construct($app_ID)
  {
    $this->db = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE); // connect to database

    if (mysqli_connect_error()) {
      echo "Error: Failed to connect to database.";
        exit;
    } else {
      // verify app ID in parenthesis
      $sql = mysqli_query($this->db, "SELECT * FROM applications WHERE app_ID = '$app_ID'");
      if (mysqli_num_rows($sql) == 1) { // app id is valid
        // store app variables in class driven variables
        $this->app_ID = $app_ID;
        $this->app_data = mysqli_fetch_assoc($sql); // stores the database data of the app
      } else { // app id is invalid or unautorized
        echo "Error: Unautorized application or invalid application identity.";
          exit;
      }
    }
  }

  /////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////// METHODS //////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////

  //////// APP NAME ////////
  function get_name()
  {
    $app_data = $this->app_data;
    return $app_data["app_name"];
  }

  function set_name($new_name)
  {
    $sql = mysqli_query($this->db, "UPDATE applications SET app_name = '$new_name' WHERE app_ID = '$app_ID'");
    return (($sql) ? 1 : 0); // return true or false inRel -> $sql
  }

  //////// APP DESC ////////
  function get_desc()
  {
    $app_data = $this->app_data;
    return $app_data["app_desc"];
  }

  function set_desc($new_desc)
  {
    $sql = mysqli_query($this->db, "UPDATE applications SET app_desc = '$new_desc' WHERE app_ID = '$app_ID'");
    return (($sql) ? 1 : 0); // return true or false inRel -> $sql
  }
}
?>
