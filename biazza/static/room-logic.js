const socket = io();

socket.on('connect', () => {
    console.log(socket.id);
});
socket.on('room_response', () => {
    console.log("I have entered a room");
});

socket.on('message_receive', (data) => {
    if(current_conversation_id == data.conversation_id){
        showMessageInContainer(data)
    } else {
        showMessageInBar(data)
    }
});

function showMessageInContainer(data){
    my_id = $("#user-area").attr("user_id")
    data.is_me = data.sender_id == myUserID // myUserID defined globally when templating messages.html
    htmlForCard = createMessageCard(data) // defined in messages.js
    $("#messages-holder").append(createMessageCard(data))
}

function showMessageInBar(data){
    barBlockElement = $("#conversation-block-" + data.conversation_id)
    barBlockElement.find(".badge").show()
    barBlockElement.find(".conversation-text").text(data.text)
    barBlockElement.find(".conversation-time").show(data.time)
}

function joinAllConversationRooms() {
    console.log("I am joining rooms...")
    socket.emit('enter_rooms')
}

setInterval(joinAllConversationRooms, 5000);

