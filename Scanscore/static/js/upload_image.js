$(document).ready(function() {
  var droppedFiles = false;
  var $dropzone = $('.dropzone');
  var $button = $('.upload-btn');
  var uploading = false;
  var $syncing = $('.syncing');
  var $done = $('.done');
  var $bar = $('.bar');
  var timeoutID;

  $dropzone.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
  }).on('dragover dragenter', function() {
      $dropzone.addClass('is-dragover');
  }).on('dragleave dragend drop', function() {
      $dropzone.removeClass('is-dragover');
  }).on('drop', function(e) {
      droppedFiles = e.originalEvent.dataTransfer.files; // process files
      $('.dropzone .upload').hide();
      updateFileNames(droppedFiles);
  });

  $("input:file").change(function () {
      droppedFiles = this.files; // update file list
      updateFileNames(droppedFiles);
      $('.dropzone .upload').hide();
  });

  function updateFileNames(files) {
      var filenames = Array.from(files).map(file => file.name);
      $('.filename').html(filenames.join('<br>'));
  }

  $button.on('click', function(e) {
      if (droppedFiles.length > 0 && !uploading) {
          e.preventDefault(); // prevent form from submitting
          startUpload(); // start upload process
      }
      // if no files are dropped or uploading is finished, do nothing (let form submit normally)
  });

  function startUpload() {
      uploading = true;
      $button.html('Uploading...');
      $syncing.addClass('active');
      $done.addClass('active');
      $bar.addClass('active');

      // Mock upload progress
      timeoutID = setTimeout(function() {
          $bar.removeClass('active');
          $syncing.removeClass('active');
          $done.removeClass('active');
          $button.html('Submit Images');
          uploading = false; // reset uploading flag
          alert('Files uploaded, now submit the form normally.');
      }, 3200);
  }
});
