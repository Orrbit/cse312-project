const socket = io();

//Socket Listeners
//Log connection
socket.on('connect', () => {
    console.log(socket.id);
});

//Receive comment
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
    $("#question-thread").scrollTop($("#question-thread").height());
});

//Receive Like
socket.on('like_status', function (data) {
    console.log("Recieved Message from server!");
    console.log(data);

    $("#comment-" + data.comment_id + " .like span").html(data.likes);
});

$(document).ready(function () {
    //POST comment
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
    
    //Emit like
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
});
