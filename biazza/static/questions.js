
// questions = [] {id:<id>,poster:<poster>, title:<title>, date:<date>, post:<post>, comments:[]}



const socket = io.connect('http://localhost:8000');

socket.on('connect', () => {
    console.log(socket.id);
});


socket.on('question_comment', (data) => {

    console.log("question_comment: " + JSON.stringify(data));

    // let msg = "Hello World"
    let msg = data['comment'];
    let commentType = "other-comment bg-dark text-light";
    if (data['myComment']) {
        commentType = 'my-comment bg-light text-dark';
    }


    let html = `<div class='${commentType}'>
    <h4>Brian</h4>
    <div class='comment-content'>
        ${msg}
    </div>
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


    $(".updateCount").click(function () {
        console.log('Button Clicked!');

        let count = $(this).find("span").text();  // get span count

        let parentId = $(this).parent().parent().attr("id");

        console.log("Parent : " + parentId);

        socket.emit('message', {
            id_name: parentId,
            number: parseInt(count) + 1
        });
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

socket.on('updateCount', function (data) {

    console.log("Recieved Message from server!");

    var count = $("#" + data.id_name + " .updateCount span").html(data.number);

    currCount = data.number;

    console.log(data);
});

socket.on('initialUpdate', function (data) {

    console.log("Initial Update of \"all count\"" + " id : " + data.id_name);

    var count = $("#" + data.id_name + " .updateCount span").html(data.number);

    console.log("Initial Count : " + data.number);

    currCount = data.number;
});