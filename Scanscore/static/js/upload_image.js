var droppedFiles = false;
var fileNames = [];
var $dropzone = $('.dropzone');
var $button = $('.upload-btn');
var uploading = false;
var $syncing = $('.syncing');
var $done = $('.done');
var $bar = $('.bar');
var timeOut;

$dropzone.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
  e.preventDefault();
  e.stopPropagation();
})
  .on('dragover dragenter', function() {
    $dropzone.addClass('is-dragover');
  })
  .on('dragleave dragend drop', function() {
    $dropzone.removeClass('is-dragover');
  })
  .on('drop', function(e) {
    droppedFiles = e.originalEvent.dataTransfer.files;
    fileNames = Array.from(droppedFiles).map(file => file.name);
    updateFileNames();
    $('.dropzone .upload').hide();
  });

$button.bind('click', function() {
  startUpload();
});

$("input:file").change(function () {
  fileNames = Array.from($(this)[0].files).map(file => file.name);
  updateFileNames();
  $('.dropzone .upload').hide();
});

function updateFileNames() {
  $('.filename').html(fileNames.join('<br>'));
}

function startUpload() {
  if (!uploading && fileNames.length > 0) {
    uploading = true;
    $button.html('Uploading...');
    $dropzone.fadeOut();
    $syncing.addClass('active');
    $done.addClass('active');
    $bar.addClass('active');
    timeoutID = window.setTimeout(showDone, 3200);
  }
}

function showDone() {
  $button.html('Done');
}
