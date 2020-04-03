// questions = [] {id:<id>,poster:<poster>, title:<title>, date:<date>, post:<post>, comments:[]}



const socket = io.connect('http://localhost:8000');

socket.on('connect', () => {
    console.log(socket.id);
});


socket.on('question_comment', (data)=> {

    console.log("question_comment: " + JSON.stringify(data));

    // let msg = "Hello World"
    let msg = data['comment'];
    let commentType = "other-comment bg-dark text-light";
    if(data['myComment']){
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


$(document).ready(function(){
    $("#add-comment").submit(function(){
        const comment = $('#comment-string').html();
        var data = {'comment': comment};

        socket.emit('question_comment', data);
        return false;
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
    });

});


