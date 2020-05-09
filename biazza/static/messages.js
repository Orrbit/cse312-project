let current_conversation_id = -1;

$(document).ready(function(){
  $("a.conversation-start-user").on("click", function(){
      let guest_user = $(this).attr("user_id")
      $.post( "/conversation", {guest_user:guest_user}, function() {
          alert( "Conversation created, ready to emit the conversation" );
        })
          .fail(function() {
            alert( "There was an error starting a new conversation" );
          });
  })

  $(document).on("click", ".conversation-block", function(){
    let conversation_id = $(this).attr("conversation_id")
    $.get( "/conversation?conversation_id="+conversation_id, function(response) {
      current_conversation_id  = conversation_id
      alert( response );
      })
      .fail(function() {
        alert( "There was an error starting a new conversation" );
      });
  })

  $(document).on("click", "#message-send", function(){
    let text = $("#message-content").val();

    $.post( "/message", {text: text, conversation_id: current_conversation_id}, function(response) {
        alert( response );
      })
      .fail(function() {
        alert( "There was an error starting a new conversation" );
      });
  })
});