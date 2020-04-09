
// questions = [] {id:<id>,poster:<poster>, title:<title>, date:<date>, post:<post>, comments:[]}



const socket = io.connect('http://localhost:8000');

socket.on('connect', () => {
    console.log(socket.id);
});

socket.on('comment_emit', (data) => {

    console.log("comment: " + JSON.stringify(data));

    let msg = data['text'];
    let likes = data['likes']
    let id = data['id']
    let commentType = "other-comment bg-dark text-light";
    // We will need this conditional to be responsive in phase 3
    if (true) {
        commentType = 'my-comment bg-light text-dark';
    }
    let attachmentString = ""
    data['attachments'].forEach(attachment => 
        attachmentString = attachmentString + `
        <a href='${attachment.path}' target='_blank'>
            ${attachment.name}
        </a>
        `
    );


    let html = `<div class='${commentType}' id='comment-${id}'>
    <h4>Me</h4>
    <div class='comment-content'>
        ${msg}
    </div>
    <div>
        ${attachmentString}
    </div>
    <div class='comment-footer'>
        <button class='btn btn-primary float-right mx-2 like'>
            <i class='fa fa-thumbs-up'></i>
            <span class='badge badge-light'>${likes}</span>
        </button>
    </div>
    </div>`
    $("#question-thread").append(html);
});


$(document).ready(function () {
    $("#add-comment").submit(function () {
        var form = $('#add-comment')[0];
        var userInput = new FormData(form);

        $.ajax({
            type: "POST",
            url: "/home/questions/comments",
            processData: false,
            contentType: false,
            cache: false,
            data: userInput,
            success: function(data){
                console.log("success");
                // Clear the form
            },
            error: function(err){
                console.log("error with post");
                // Provide some indication that there was an error
            }
        });


        return false;
    });


    $(document).on("click", "button.like", function () {
        let count = $(this).find("span").text();
        let parentId = $(this).parent().parent().attr("id");
        let commentId = parentId.replace("comment-", "");
        if($(this).is(':disabled')){
            //We are handling the case that they are revoking a upvote
            socket.emit('like_click', {
                comment_id: commentId,
                is_like: false
            });
            $(this).attr('disabled', false);
        } else {
            socket.emit('like_click', {
                comment_id: commentId,
                is_like: true
            });
            $(this).attr('disabled', true);
        }
        console.log("Parent : " + parentId);
        console.log("Messag Sent with count : " + count);
    });

    $("#fileUploadButton").click(function () {
        let files = document.getElementById("fileInp").files;

        if (files.length == 0) {
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
                success: function (data) {
                    console.log("UPLOAD SUCCESS: ", data);
                    $('#fileUploadModal').modal('toggle');
                    $("#fileUploadMessage").html("");

                    let link = '<a href="' + data['href'] + '" target="_blank">' + data['filename'] + '</a>';

                    $('#comment-string').html($('#comment-string').html() + link);
                },
                error: function (err) {
                    console.log("ERROR: ", err);
                }
            })
        }
    });

});


var currCount = 0;

socket.on('like_status', function (data) {
    console.log("Recieved Message from server!");
    console.log(data);

    $("#comment-" + data.comment_id + " .like span").html(data.likes);
});

socket.on('initialUpdate', function (data) {

    console.log("Initial Update of \"all count\"" + " id : " + data.id_name);

    var count = $("#" + data.id_name + " .updateCount span").html(data.number);

    console.log("Initial Count : " + data.number);

    currCount = data.number;
});