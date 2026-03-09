# Simple TCP Chat Application

## Overview

This project implements a **multi-client chat application** using **TCP socket programming**.
The system follows a **client–server architecture** where a central server manages communication between multiple connected clients.

Each client connects to the server using an IP address and port number. Users can send messages that are broadcast to all other connected clients in real time.

The application demonstrates important networking concepts such as:

* TCP socket programming
* Client–server architecture
* Multi-client communication
* Thread-based concurrency
* Application-layer protocol design
* Reliable communication over TCP

---

# System Architecture

The chat application uses a **centralized client–server model**.

Clients do not communicate directly with each other. Instead, all communication passes through the server.

Architecture flow:

Client → Server → Broadcast → Clients

### Components

**Server**

* Accepts incoming client connections
* Maintains a list of connected users
* Receives messages from clients
* Broadcasts messages to other clients
* Handles user join and leave notifications
* Handles unexpected disconnections

**Client**

* Connects to the server
* Sends messages typed by the user
* Receives messages from other users
* Displays messages in real time
* Allows clean exit using `/quit`

---

# Communication Protocol

The application uses a **simple text-based protocol** between the client and server.

### Commands

JOIN <username>
Used when a client joins the chat.

MSG <message>
Used when a client sends a message.

USERS
Requests the list of currently connected users.

QUIT
Disconnects the client from the server.

### Example

JOIN Rijwith
MSG Hello everyone
USERS
QUIT

---

# Features

### Core Features

* Multi-client chat server
* TCP socket communication
* Real-time message broadcasting
* Username system
* Join/leave notifications
* Graceful client disconnection
* Server runs continuously
* Supports **10+ concurrent clients**

### Extra Credit Features

**1. Message Timestamps**

Every message includes the time when it was sent.

Example:

[14:02:10] Rijwith: Hello everyone

---

**2. User List Command**

Users can view currently connected users.

Command:

/users

Example output:

[SERVER] Connected users: Rijwith, yash, anshul

---

# Concurrency Model

The server uses a **thread-per-client concurrency model**.

When a new client connects:

1. The server accepts the connection.
2. A new thread is created.
3. That thread handles communication with that client.

Advantages of this approach:

* Multiple clients can chat simultaneously
* No client blocks another
* Simple and efficient implementation

Python’s **threading module** is used to implement concurrency.

---

# Installation Requirements

Python 3.x

No external libraries are required.

Only the standard Python libraries are used:

* socket
* threading
* datetime
* sys

---

# Running the Application

## Step 1 — Start the Server

Navigate to the server folder:

cd server

Run:

python chat_server.py

Server output example:

Chat server running on port 5000

---

## Step 2 — Start the Client

Open a new terminal.

Navigate to the client folder:

cd client

Run:

python chat_client.py

Enter the server IP address:

Enter server IP: 127.0.0.1

Enter username:

Enter username: Rijwith

---

# Example Chat Session

User Rijwith joins:

[22:45:00] [SERVER] rijwith joined the chat

User anshul joins:

[22:46:07] [SERVER] anshul joined the chat

Rijwith sends message:

Hello anshul

Output:

[23:01:25] rijwith: hello anshul

anshul checks connected users:

/users

Output:

[SERVER] Connected users: rijwith, anshul

rijwith exits:

/quit

Output:

[23:03:11] [SERVER] rijwith left the chat

---

# Testing

Several tests were performed to ensure reliability.

### Multiple Client Connections

Multiple clients connected simultaneously to ensure the server supports concurrent connections.

### Simultaneous Messaging

Several clients sent messages at the same time to verify proper message broadcasting.

### Client Disconnection

Clients were disconnected intentionally to verify that the server handles unexpected disconnects.

### Server Stability

The server was tested with multiple clients for extended periods to ensure continuous operation.

### Edge Cases

* Empty messages
* Long messages
* Rapid message sending

---

# Challenges Faced

**Handling Unexpected Disconnections**

Clients may close the program without sending the QUIT command. The server must detect this and remove the client safely.

**Shared Data Synchronization**

Multiple threads access the client list simultaneously. Locks are required to prevent race conditions.

**Message Broadcasting**

Ensuring that messages are delivered to all connected clients except the sender required careful implementation.

---

# Learning Outcomes

Through this assignment the following concepts were learned:

* TCP socket programming
* Multi-client server design
* Thread-based concurrency
* Application-layer protocol design
* Handling network errors and disconnections
* Testing distributed systems

---

# Author

Rijwith Mamidi
B.Tech Computer Science

Computer Networks Programming Assignment
