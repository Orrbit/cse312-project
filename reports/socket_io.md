# Phase 2

## Flask-SocketIO (server-side)

**Flask-SocketIO website** - [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)

## Code used by Author Shazmaan, Sam

**Code can be found in socket_handlers.py** - [socket_handlers.py](https://github.com/Shazmaan)

<update this link when merged>

### Flask-SocketIO code

```
@socketio.on('connect') # when socket connects
def <function name>:
    <operations>

@socketio.on('disconnect')
def <function name>:
    <operations>

```
* Why did I use this code?

The code helps establish connection/disconnection of sockets with the already established server. This code also helps communicate 
with those sockets. 

* How does the code do what it does?

Upon executing socketio.run(), the library starts the server and waits for a request from the client to make a websocket connection and 
upon connection, the connect function above is executed and on disconnect the disconnect function is executed.

* Licensing?

No licensing.

### Flask_SocketIO communicate with websocket code

```
@socketio.on('<message_id>')
def handle_message(message):
    <handle message>

```
* Why did I use this code?

The code helps with communicating with the server on how to act when a websocket message is received from the client.

* How does the code do what it does?

The library sees the client and recognizes that the client is a websocket connection and communicates with the corresponding
python function.

* Licensing?

No licensing.

### Flask-SocketIO emit (ing) messages back to client
 
```
emit('<message_id>', message, broadcast = True) # BroadCast message to all clients

```
* Why did I use this code?

The library recognizes this command as websocket "send" command and sends a message to the client with the message_id and the message.
This makes it easier to handle in the client side as the message sent can be recognized by the message_id. Broadcasting messages to 
all clients is also made easier by setting the broadcast variable to True here.

* How does the code do what it does?

This code access the libraries create frame function where it sends to the websocket client a message (as a websocket frame) with it's
respective size and data. Setting broadcast = True here sends the message_id as well as the message to all the websocket clients that
are currently connected.

* Licensing?

No licensing.

## Socket IO (client-side)

**Socket IO website** - [Socket IO](https://socket.io/)

## Code used by Author Shazmaan, Sam

**Code can be found in questions.js** - [questions.js](https://github.com/Shazmaan)
**Code can be found in questions.html** - [questions.html](https://github.com/Shazmaan)

<update this link when merged>

### Socket IO connection

```
const <socket_name> = io.connect('http://localhost:8000');

```
* Why did I use this code?

The code helps establish connection/disconnection of sockets with the already established server. This code also helps communicate 
with those sockets. 

* How does the code do what it does?

This code sends a websocket connection request to the server and initializes the response to <socket_name>

* Licensing?

No licensing.

### Socket IO sending messages to client

```
<socket_name>.emit('<message_id>', message);

```
* Why did I use this code?

This code sends ("emits") the message_id and the message to server to process.

* How does the code do what it does?

This code creates a websocket frame with the given message and the message_id and sends the websocket frame to the server to decode which
the server handles according upon recognizing that the connection is a websocket connection.

* Licensing?

No licensing.

### Socket IO receiving messages from server
 
```
socket.on('<message_id>', function (message) {});

```
* Why did I use this code?

 This code helps make sending messages to server easier. Especially as you can send a sort of "message_id" with it. The server can easily recognize
 the type of functionality of the message by recognizing what this message_id is. This makes the communication between the client and server over a 
 websocket easier.

* How does the code do what it does?

The library recognizes this command as websocket "receive" command and receives a message from the server in frames and first decodes
the received frame into parts, here it is message_id and the message (payload_data) itself. This message can then be passed into a function
where the message can parsed and used by the client as required.

* Licensing?

No licensing.
