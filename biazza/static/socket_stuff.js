// Socket stuff
var socket = io.connect('http://localhost:8000');

var updateBtn = document.getElementById('updateCount');
var count = document.getElementById('count');

// Emit Events
updateBtn.addEventListener('click', function(){
    console.log('Button Pressed!');
});

// Socket functions
socket.on('connect', function(){
    socket.emit('connect', 'Hello Server! I am Socket!');
});