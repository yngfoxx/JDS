<?php
// PACKAGES ---------------------------
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/auth.php';
// ------------------------------------


// OBJECTS [reusable] -----------------
$std = new stdlib();
$auth = new auth();
// ------------------------------------


// SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
if (isset($_COOKIE['dKEY'])) {
  if ($auth->verfUser($_COOKIE['dKEY']) == false) {
    $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
    // echo json_encode($result);
    header("location: ./?logout");
  }
} else {
  $_SESSION['error'] = "Unauthorized access";
  header("location: ./?logout");
}
?>

<div class="_tnvbr">
  <a class="icon-wrench-3 _tb_menu_btn"></a>
  <h3 class="_tblgo" title="Joint Download Software">JDS</h3>
  <ul class="_mnuli">
    <li title="Logout">
      <a class="icon-logout"></a>
    </li>
  </ul>
</div>
<div class="_bdyMain">
  <div class="_bdysec1">

    <form class="_bibf" method="POST">
      <div class="_bibf_div">
        <input class="_bibftxt" name="path_code" placeholder="Enter URL or JDS code" type="text" required>
        <button type="submit" class="_bibfbtn icon-plus" title="New J0INT"></button>
      </div>
      <div class="floating_info">Don't have JDS extension? download from <a href="#">here</a></div>
    </form>

    <!-- Configuration menu -->
    <div class="_bibf_div_c_cont">
      <form class="_bibf_dc_div">
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_title">Download configuration</div>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_text">Manual configuration</div>
          <label class="switch"><input type="checkbox" name="auto_config"><span class="slider round"></span></label>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_text v_row">
            <label>Maximum chunk size</label>
            <select style="background: #EEE;" name="max_chunk" disabled class="_bibfdcds_select">
              <option value="5" selected>5 MB</option>
              <option value="10">10 MB</option>
              <option value="50">50 MB</option>
              <option value="100">100 MB</option>
              <option value="200">200 MB</option>
              <option value="s">Specify</option>
            </select>
            <input type="text" style="display: none;" name="chunk_max_size" class="chunkInput" placeholder="Specify chunk size (MB)">
          </div>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_btn" data-button="cls_config">Save</div>
        </div>
      </form>
    </div>

  </div>

  <div class="_bdysec2">
    <div class="float_center_msg" data-jds-body>Enter a URL or a Group code to begin</div>
    <div class="_bs2_div_contr hide">
      <div class="_bs2dc_pane _pane_l"></div>
      <div class="_bs2dc_pane _pane_r"></div>
    </div>
  </div>
</div>
