function populateMessagesContainer(message_data){
  htmlForMainContent = ""
  message_data.forEach(message =>{
    htmlForMainContent = htmlForMainContent + createMessageCard(message)
  });
  $("#messages-holder").html(htmlForMainContent);
  $('#messages-holder').scrollTop($("#messages-holder").height());
}

function createMessageCard(singleMessageData){
  divType = "";
    if(singleMessageData.is_me){
      divType= `<div class="d-flex justify-content-end align-items-center">
            <div class="message bg-primary border rounded-top rounded-left mb-3 mr-3 p-3 text-light">`
    } else {
      divType = `<div class="d-flex justify-content-begin align-items-center">
      <div class="message bg-light border border-dark rounded-top rounded-right mb-3 ml-3 p-3">`
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

function createConversationHtml(conversation){
  let htmlForBar = `<div conversation_id="${conversation.id}" id="conversation-block-${conversation.id}" class="row conversation-block border border-dark py-3 " >
            <div user_id="${conversation.other_id}" class="col-12">
                <h5>${ conversation.other_name }</h5>
            </div>
            <div class="col-12">
                <p class="conversation-text">
                    <b>${ conversation.text }</b>
                </p>
            </div>
            <div class="col-8">
                <small class="conversation-time">
                  ${ conversation.time }
                </small>
            </div>
            <div class="col-4">
                <span class="badge badge-warning"><i class="fas fa-star"></i></span>
            </div>
        </div>`
  return htmlForBar
}

$(document).ready(function(){
  $("a.conversation-start-user").on("click", function(){
      let guest_user = $(this).attr("user_id")
      let name = $(this).text()
      $.post( "/conversation", {guest_user:guest_user}, function(data) {
        conversationHtml = createConversationHtml({
          id: data.id,
          other_user: guest_user,
          other_name: name,
          text: "Start a new conversation now!",
          time: (new Date(Date.now())).toISOString()
        })
        $(".message-container").append(conversationHtml)
        $('#conversation-start-modal').modal('hide')
      })
          .fail(function() {
            alert( "There was an error starting a new conversation" );
          });
  })

  $(document).on("click", ".conversation-block", function(){
    let conversation_id = $(this).attr("conversation_id")
    $(this).find(".badge").hide()
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
        alert( "There was an error sending a message" );
      });
  })
});