
$(document).ready(function (events, handler) {

    function handleUnfollow() {
        let id = $(this).parent().parent().attr('id');
        id = id.split('-')[0];

        $.ajax({
            method: 'POST',
            url: '/unfollow',
            processData: false,
            data: JSON.stringify({'id': id}),
            contentType: 'application/json',
            success: function (data) {
                console.log('Unfollow was a success');

                $(`#${id}-following`).remove();
                let button = $(`#${id}`).find('button');
                button.removeClass('btn-danger following');
                button.addClass('btn-success not-following');
                button.html('Follow');
                button.off('click').on('click', handleFollow);
            },
            error: jqXHR => {
                console.log('Unfollow failed');
            }
        });
    }

    function handleFollow(){
        let $button = $(this);
        let id = $button.parent().parent().attr('id');
        id = id.split('-')[0];
        console.log(id);

        $.ajax({
            method: 'POST',
            url: '/follow',
            processData: false,
            data: JSON.stringify({'id': id}),
            contentType: 'application/json',
            success: function (data) {
                console.log('Follow was a success');

                $button.removeClass('btn-success not-following');
                $button.addClass('btn-danger following');
                $button.html('Unfollow');
                $button.off('click').on('click', handleUnfollow);

                let user = data['user'];

                let html = `
                    <div id="${id}-following" data-lastname="${user['last_name']}" class="row bg-light m-3 border">
                        <div class="col-8">
                            <h6>${user['first_name']} ${user['last_name']}</h6>
                            <a href="mailto:{{ leader.email }}">${user['email']}</a>
                        </div>
                        <div class="col d-flex flex-row-reverse">
                            <button class="btn btn-danger my-auto following">Unfollow</button>
                        </div>
                    </div>
                `;

                let htmlSelector = $(html);
                htmlSelector.find('button').on('click', handleUnfollow);

                let followingContainer = $('#followContainer');
                let followingList = followingContainer.children();

                let inserted = false;
                followingList.each(function (i) {
                    if(user['last_name'] < $(this)[i].getAttribute('data-lastname')) {
                        htmlSelector.insertBefore($(this)[i]);
                        inserted = true;
                        return false;
                    }
                });


                if(!inserted){
                    followingContainer.append(htmlSelector);
                }
            },
            error: jqXHR => {
                console.log('Follow failed');
            }
        });
    }


    $('.following').on("click", handleUnfollow);

    $('.not-following').on("click", handleFollow);

})
