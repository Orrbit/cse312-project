let currentPage = "";

function setNotification(count) {
    let notification = $('#messagesNotification');

    notification.html(count);

    if(count == 0){
        notification.removeClass('visible');
        notification.addClass('invisible');
    } else {
        notification.addClass('visible');
        notification.removeClass('invisible');
    }
}


function changeIFrame(newSource){
    $("#mainContent").attr("src", newSource);
    currentPage = newSource;
    if(currentPage == "/home/messages"){
        unreadMessageCount = 0;
        setNotification(0);
    }
}

const socket = io();
let unreadMessageCount = 0;

socket.on('connect', () => {
    console.log(socket.id);
});
socket.on('room_response', () => {
    console.log("I have entered a room");
});

socket.on('message_receive', (data) => {
    if(currentPage != '/home/messages'){
        unreadMessageCount += 1;
        setNotification(unreadMessageCount);
    }

});



function joinAllConversationRooms() {
    console.log("I am joining rooms...")
    socket.emit('enter_rooms')
}

setTimeout(joinAllConversationRooms, 5000);

