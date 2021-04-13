<?php
  echo "<div><h1>Chunk splitting</h1>";
  $bytes = 309721;
  $max_chunk_size = 20; // Percent
  $percentile_chunk = ($bytes * $max_chunk_size) / 100;
  $percentIntrator = 0;

  while ($percentIntrator < $bytes) {
    $percentIntrator += $percentile_chunk;
    echo "$percentIntrator <br>";
  }
  echo "</div>";
?>
