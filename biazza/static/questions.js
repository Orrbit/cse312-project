$(document).ready(function(){
    $("#add-comment").submit(function(){
        let msg = $(this).find('textarea').val()
        let html = `<div class='my-comment bg-light text-dark'>
        <h4>Brian</h4>
        <p class='comment-content'>
            ${msg}
        </p>
        <div class='comment-footer'>
            <button class='btn btn-primary float-right mx-2'>
                <i class='fa fa-thumbs-up'></i>
                <span class='badge badge-light'>0</span>
            </button>
            <button class='btn btn-primary float-right mx-2'>
                <i class='fa fa-star'></i>
                <span class='badge badge-light'>0</span>
            </button>
        </div>
        </div>`
        $("#question-thread").append(html);
    });

    $("#fileUploadButton").click(function(){
        let files = document.getElementById("fileInp").files;

        if(files.length == 0){
            $("#fileUploadMessage").html("No files were selected for upload.");
            $("#fileUploadMessage").css('color', 'red');
        } else {
            let uploadData = new FormData();
            uploadData.append('file', files[0]);

            $.ajax({
                type: "POST",
                mimeType: "multipart/form-data",
                url: "/home/questions/files",
                data: uploadData,
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log("UPLOAD SUCCESS: ", data);
                    $('#fileUploadModal').modal('toggle');
                    $("#fileUploadMessage").html("");

                    let link = '<a href="' + data['href'] + '" target="_blank">' + data['filename'] + '</a>';

                    $('#comment-string').html($('#comment-string').html() + link);
                },
                error: function(err) {
                    console.log("ERROR: ", err);
                }
            })
        }
    })
});