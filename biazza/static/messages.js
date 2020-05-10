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
    $.get( "/conversation?conversation_id="+conversation_id, function(data) {
      current_conversation_id  = conversation_id;
      populateMessagesContainer(data)
    }).fail(function() {
      alert( "There was an error starting a new conversation" );
    });
  })

  $(document).on("click", "#message-send", function(){
    let text = $("#message-content").val();

    $.post( "/message", {text: text, conversation_id: current_conversation_id}, function(response) {})
      .fail(function() {
        alert( "There was an error starting a new conversation" );
      });
  })
});

function populateMessagesContainer(message_data){
  htmlForMainContent = ""
  data.forEach(message =>{
    htmlForMainContent = htmlForMainContent + createMessageCard(message)
  });
  $("#messages-holder").html(htmlForMainContent);
}

function createMessageCard(singleMessageData){
  divType = "";
    if(singleMessageData.is_me){
      divType= `<div class="d-flex justify-content-end align-items-center">
            <div class="message bg-primary border rounded-top rounded-left mb-3 p-3 text-light">`
    } else {
      divType = `<div class="d-flex justify-content-begin align-items-center">
      <div class="message bg-light border border-dark rounded-top rounded-right mb-3 p-3">`
    }
    content = divType + `
            <h6>${ singleMessageData.name }</h6>
            <div>${ singleMessageData.text }</div>
            <small>${ singleMessageData.time }</small>
        </div>
    </div>
    `
    return content
}