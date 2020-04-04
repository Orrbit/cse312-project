var socket = io.connect('http://localhost:8000');


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

    $(".updateCount").click(function(){
        console.log('Button Clicked!');

        let count = $(".updateCount span").text();

        socket.emit('message', {
            id_name: "<enter idenitifier>",
            number: parseInt(count) + 1
        });
        console.log("Messag Sent with count : " + count);
    });
});

var currCount = 0;

socket.on('updateCount', function(data){

    console.log("Recieved Message from server!");

    var count = $(".updateCount span").html(data.number);

    currCount = data.number;

    console.log(currCount);
});

socket.on('initialUpdate', function(data){

    console.log("Initial Update of \"all count\"");

    var count = $(".updateCount span").html(data.number);

    currCount = data.number;
});