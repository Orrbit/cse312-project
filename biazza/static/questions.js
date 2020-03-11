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
});