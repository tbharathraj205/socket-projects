# Python Multi-Client TCP Chat Application

A real-time chat application built using Python sockets and multithreading. Multiple clients can connect to a central server, send messages, and receive messages from other connected clients.

## Features

- **TCP Communication:** Reliable communication between clients and the server.
- **Multiple Clients:** Supports multiple clients connecting to one server.
- **Multithreading:** Handles each client using a separate thread.
- **Username Assignment:** Assigns usernames from `usernames.txt`.
- **Message Broadcasting:** Sends messages to other connected clients.
- **Timestamps:** Displays the date and time of each message.
- **Graceful Disconnection:** Allows clients to disconnect using `q`.

## Project Structure

```text
sev-cli/
├── client.py
├── server.py
├── usernames.txt
├── .env
├── .env.example
└── README.md
```

## Requirements

- Python 3.9 or later
- `python-dotenv` package

Install the required package:

```bash
pip install python-dotenv
```

## Configuration

Create a `.env` file in the project root directory.

```env
SERVER_IP=127.0.0.1
PORT=65431
```

- `SERVER_IP`: The IP address of the computer running the server.
- `PORT`: The port used for communication between the server and clients.

**Important:** If clients connect from another computer, replace `127.0.0.1` with the server computer's reachable IP address. Ensure the server's firewall allows connections on the selected port.

Keep `.env` private. Use `.env.example` to share placeholder configuration with others.

## Username Configuration

Add one username per line in `usernames.txt`.

```text
Bharath
Alice
Bob
Charlie
```

The server assigns usernames to clients in the order they connect. Ensure there are enough usernames for the clients you expect to connect.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/tbharathraj205/multiclient-tcp-chat-server.git
cd multiclient-tcp-chat-server
```

### 2. Install dependencies

```bash
pip install python-dotenv
```

### 3. Configure the environment

Create your `.env` file using the configuration described above.

### 4. Start the server

Open a terminal and run:

```bash
python server.py
```

### 5. Start the clients

Open separate terminals and run:

```bash
python client.py
```

Type `yes` to connect, then enter messages to chat.

Type `q` to disconnect from the client.

## Technologies Used

- Python
- Socket Programming
- TCP/IP Networking
- Multithreading
- Environment Variables (`python-dotenv`)

## Learning Outcomes

This project helped me understand:

- Client-server architecture.
- TCP socket communication.
- Handling multiple clients using threads.
- Sending and receiving messages.
- Using locks to protect shared client data.
- Managing configuration through environment variables.

## Future Improvements

- Allow users to choose their own usernames.
- Add private messaging.
- Handle unexpected client disconnections more robustly.
- Add authentication and encrypted communication.
- Improve the chat interface.

## Author

**Bharath Raj T**

GitHub: [tbharathraj205](https://github.com/tbharathraj205)

---

*Built as a hands-on project to learn Python networking and concurrent programming.*
