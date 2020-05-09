const socket = io();

socket.on('connect', () => {
    console.log(socket.id);
});
socket.on('room_response', (data) => {
    console.log("I HAVE GOT BACK A RESPONSE FOR ENTERING: "+ data);
});

function joinAllConversationRooms() {
    socket.emit('enter_rooms')
}

