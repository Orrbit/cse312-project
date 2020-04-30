$(document).ready(function(){
    $("a.conversation-start-user").on("click", function(){
        let guest_user = $(this).attr("user_id")
        $.post( "/home/conversation", {guest_user:guest_user}, function() {
            alert( "Conversation created, ready to emit the conversation" );
          })
            .fail(function() {
              alert( "There was an error starting a new conversation" );
            });
    })
});