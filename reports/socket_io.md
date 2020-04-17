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

both the above functions call the below in flask-socketIO library:
    class SocketIO(object):
    """Create a Flask-SocketIO server.
    ....
    ....
    def on(self, message, namespace=None):
        """Decorator to register a SocketIO event handler.

```
* Why did I use this code?

The code helps establish connection/disconnection of sockets with the already established server. This code also helps communicate 
with those sockets. 

* How does the code do what it does?

Upon executing socketio.run(), the library starts the server and waits for a request from the client to make a websocket connection and 
upon connection, the connect function above is executed and on disconnect the disconnect function is executed.

The code in the library flask-socketIO, checks what the handler is, here in this case, it is 'connect' and 'disconnect' and based on the handler,
it acts a certain way. 'connect' and 'disconnect' are built in commands that execute when a socket connection is made and then disconnected.

* Licensing?

MIT Licensing.

### Flask_SocketIO communicate with websocket code

```
@socketio.on('<message_id>')
def handle_message(message):
    <handle message>

The above functions call the below in flask-socketIO library:
    class SocketIO(object):
    """Create a Flask-SocketIO server.
    ....
    ....
    def on(self, message, namespace=None):
        """Decorator to register a SocketIO event handler.

```
* Why did I use this code?

The code helps with communicating with the server on how to act when a websocket message is received from the client.

* How does the code do what it does?

The library sees the client and recognizes that the client is a websocket connection and communicates with the corresponding
python function.

The code in the library flask-socketIO, checks what the handler is, here in this case, it is '<message_id>'. In the def on function, the library
checks if the message_id is a user_defined string and if it is, it creates handlers for it such that every time this <message_id> is passed, 
the function executes the handler.

* Licensing?

MIT Licensing.

### Flask-SocketIO emit (ing) messages back to client
 
```
emit('<message_id>', message, broadcast = True) # BroadCast message to all clients

The above functions call the below in flask-socketIO library:
    class SocketIO(object):
    """Create a Flask-SocketIO server.
    ....
    ....
    def emit(event, *args, **kwargs):
    """Emit a SocketIO event.

```
* Why did I use this code?

The library recognizes this command as websocket "send" command and sends a message to the client with the message_id and the message.
This makes it easier to handle in the client side as the message sent can be recognized by the message_id. Broadcasting messages to 
all clients is also made easier by setting the broadcast variable to True here.

* How does the code do what it does?

This code access the libraries create frame function where it sends to the websocket client a message (as a websocket frame) with it's
respective size and data. Setting broadcast = True here sends the message_id as well as the message to all the websocket clients that
are currently connected.

The code in the library flask-socketIO, the emit function checks the event, here it is <message_id>, gets the args, here message that needs to be sent to
all clients, and kwargs, which here is broadcast = True. If broadcast = False, then the socket doesn't send the event and message to "all" clients but,
just replies to the sender of the originating event. If broadcast = True (which we have) then the event is sent to all clients connected to a socket.

The emit functions calls a parent "emit" function in the library flask-socketIO, which is the below in namespace.py in the library,

```
def emit(self, event, data=None, room=None, include_self=True,
             namespace=None, callback=None):
        """Emit a custom event to one or more connected clients."""

```

* Licensing?

MIT Licensing

## Socket IO (client-side)

**Socket IO website** - [Socket IO](https://socket.io/)
**Socket IO source code** - [Socket IO source code](https://github.com/socketio)

## Code used by Author Shazmaan, Sam

**Code can be found in questions.js** - [questions.js](https://github.com/Shazmaan)
**Code can be found in questions.html** - [questions.html](https://github.com/Shazmaan)

<update this link when merged>

### Socket IO connection

```
const <socket_name> = io();

```
* Why did I use this code?

The code helps establish connection/disconnection of sockets with the already established server. This code also helps communicate 
with those sockets. 

* How does the code do what it does?

This code sends a websocket connection request to the server and initializes the response to <socket_name>.

In the socket.io library, it also creates a new Manager for the current connected host (default is windows.location). Upon creating a manager, a new Socket instance is given back to <socket_name> and several processes could be initiated after a socket instance is created.

Refer to the [source_code](https://github.com/socketio/socket.io-client/blob/master/docs/API.md#new-managerurl-options) for manager function and details.

* Licensing?

MIT Licensing.

### Socket IO sending messages to client

```
<socket_name>.emit('<message_id>', message);

```
* Why did I use this code?

This code sends ("emits") the message_id and the message to server to process.

* How does the code do what it does?

This code creates a websocket frame with the given message and the message_id and sends the websocket frame to the server to decode which
the server handles according upon recognizing that the connection is a websocket connection.

In the socket.io library, the event is then "emitted" to the socket that is identified by the <socket_name>.

Refer to the [source_code](https://github.com/socketio/socket.io-client/blob/master/docs/API.md#socketemiteventname-args-ack) for emit function and details.

* Licensing?

MIT Licensing.

### Socket IO receiving messages from server
 
```
<socket_name>.on('<message_id>', function (message) {});

```
* Why did I use this code?

 This code helps make sending messages to server easier. Especially as you can send a sort of "message_id" with it. The server can easily recognize
 the type of functionality of the message by recognizing what this message_id is. This makes the communication between the client and server over a 
 websocket easier.

* How does the code do what it does?

The library recognizes this command as websocket "receive" command and receives a message from the server in frames and first decodes
the received frame into parts, here it is message_id and the message (payload_data) itself. This message can then be passed into a function
where the message can parsed and used by the client as required.

In the socket.io library, this calls the parent class Emitter(https://github.com/component/emitter) where the receiving Emitter#on(event,fn) is called.
This function, registers and event handler for the fn. Here, it takes the <message_id> and initializes a handler for it such that it handles what ever we require
the fucntion to complete.

Refer to the [source_code](https://github.com/component/emitter) for Emitter parent class and details.
Refer to the [source_code](https://github.com/socketio/socket.io-client/blob/master/docs/API.md#socketoneventname-callback) for .on function in socket-io,

* Licensing?

MIT Licensing.
