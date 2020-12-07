<?php
if ((!isset($_SESSION['logged_in']) && !isset($_SESSION['userID'])) || !$_SESSION['logged_in'] || !isset($_COOKIE['dKEY'])) {
  $_SESSION['error'] = "Unauthorized access";
  header("location: ./?login");
}
 ?>

<div class="_tnvbr">
  <a class="icon-menu _tb_menu_btn"></a>
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
        <button type="submit" class="_bibfbtn icon-link-5" title="Start JDS"></button>
        <button type="button" class="_bibfbtn icon-cog-6" data-button="config" title="configuration"></button>
      </div>
      <div class="floating_info">Don't have JDS extension? download from <a href="#">here</a></div>
    </form>

    <!-- Configuration menu -->
    <div class="_bibf_div_c_cont">
      <div class="_bibf_dc_div">
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_title">Configuration</div>
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
          <div class="_bibfdcds_btn" data-button="cls_config">Close</div>
        </div>
      </div>
    </div>

  </div>

  <div class="_bdysec2">
    <div class="float_center_msg" data-jds-body>Enter a URL or a Group code to begin</div>
  </div>
</div>
