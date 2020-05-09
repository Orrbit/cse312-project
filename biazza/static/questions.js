const socket = io();

let queryParams = new URLSearchParams(window.location.search);
let filter = 'all';
if(queryParams.has('filter')){
    let f_param = queryParams.get('filter');
    if(f_param === 'me'){
        filter = 'me';
    } else if(f_param === 'following'){
        filter = 'following';
    }
}

//Socket Listeners
//Log connection
socket.on('connect', () => {
    console.log(socket.id);
});


// Receive question
socket.on('question_emit', (data) => {

    console.log("question: " + JSON.stringify(data));

    let q_id = data['id'];
    let title = data['title'];


    title = title.replace(">", "&gt;"); title = title.replace("<", "&lt;"); title = title.replace("&", "&amp;");

    let html = '<a class="list-group-item list-group-item-action" data-toggle="list" role="tab" id="' + q_id + '">' + title + '</a>'

    if(filter === 'all'){
        $('#questionsPane').prepend(html);
    } else {
        $.ajax({
            method: 'GET',
            url: '/home/questions/' + q_id + '/' + filter,
            success: function (data) {
                if (data === true){
                    $('#questionsPane').prepend(html);
                }
            }
        });
    }


});

//Receive comment
socket.on('comment_emit', (data) => {

    console.log("comment: " + JSON.stringify(data));


    if ($('.active').attr('id') == data['qid']) {
        let msg = data['text'];
        msg = msg.replace(">", "&gt;"); msg = msg.replace("<", "&lt;"); msg = msg.replace("&", "&amp;");

        console.log("MSG : " + msg);

        let likes = data['likes'];
        let id = data['id'];
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
        <h4>${data['name']}</h4>
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
    }


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

        console.log("User Input : " + userInput);

        var q_id = $('.active').attr('id');

        $.ajax({
            type: "POST",
            url: "/home/questions/" + q_id + "/comments",
            processData: false,
            contentType: false,
            cache: false,
            data: userInput,
            success: function (data) {
                console.log("success");
                form.reset();
                // Clear the form
            },
            error: function (err) {
                console.log("error with post");
            }
        });


        return false;
    });


    $('#postQuestion').submit(function () {
        var form = $('#postQuestion')[0];
        var userInput = new FormData(form);

        $.ajax({
            type: 'POST',
            url: "/home/questions",
            processData: false,
            contentType: false,
            cache: false,
            data: userInput,
            success: function (data) {
                $("#newQuestionModal").modal('hide');
            },
            error: function (e) {
                $("#questions-msg").text("Don't leave title or question body blank.");
                $("#questions-msg").css('color', 'red');
            }
        });

        return false;
    });


    // Handler for opening a question from the menu
    $(document).on("click", ".list-group-item", function (event) {
        // event.stopPropagation();
        // event.stopImmediatePropagation();

        var qid = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: '/home/questions/' + qid,
            cache: true,
            success: function (data) {
                console.log('Question: ' + data);

                var html = `
                <div class="jumbotron jumbotron-fluid  p-3" id="${data['id']}">
                    <h1 class="display-4">${data['title']}</h1>
                    <p class="lead">Submitted by ${data['name']}</p>
                    <p class="lead">Date: 3/9/2020</p>
                    <hr class="">
                    <p>${data['content']}</p>
                </div>`;

                for (var comment of data['comments']) {
                    html += `
                    <div class='my-comment bg-light text-dark' id="comment-${comment['c_id']}">
                        <h4>${comment['name']}</h4>
                        <p class='comment-content'>
                            ${comment['c_text']}
                        </p>
                        <div>
                    `;
                    for (var attachment of comment['attachments']) {
                        html += `
                        <a href='${attachment['path']}' target='_blank'>
                            ${attachment['name']}
                        </a>
                        `;
                    }

                    html += `
                    </div>
                        <div class='comment-footer'>
                            <button class='btn btn-primary float-right mx-2 like'>
                                <!-- added updateCount as a class and count as a class -->
                                <i class='fa fa-thumbs-up'></i>
                                <span class='badge badge-light'>${comment['c_likes']}</span>
                            </button>
                        </div>
                    </div>
                    `;
                }

                $('#question-thread').html(html);
                $('#comment-form').show();
                console.log(html);
            },
            error: function (e) {
                console.log(e);
            }

        });

    });


    //Emit like
    $(document).on("click", "button.like", function () {
        let count = $(this).find("span").text();
        let parentId = $(this).parent().parent().attr("id");
        let commentId = parentId.replace("comment-", "");
        if($(this).hasClass('liked')){
            //We are handling the case that they are revoking a upvote
            socket.emit('like_click', {
                comment_id: commentId,
                is_like: false
            });
            $(this).removeClass('liked')
        } else {
            socket.emit('like_click', {
                comment_id: commentId,
                is_like: true
            });
            $(this).addClass('liked')
        }
        console.log("Parent : " + parentId);
        console.log("Messag Sent with count : " + count);
    });


    if($('#questionsPane').children().length == 0){
        console.log()
        $('#comment-form').hide();
    }

});
