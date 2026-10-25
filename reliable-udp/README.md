# Reliable File Transfer over UDP

A simple Python project that transfers a text file from a server to a client using UDP sockets.

## Features

- UDP client-server communication
- File transfer using chunks
- SHA-256 checksum verification
- ACK messages to acknowledge received chunks
- JSON-based message format
- Thread-based server request handling

## Requirements

- Python 3
- Basic knowledge of socket programming

## Project Structure

```text
 /
├── client/
│   └── client.py
├── server/
│   ├── sample.txt
│   └── server.py
├── README.md
└── sudo-json.md
```

## How to Run

**1. Start the server**

```bash
python server.py
```

**2. Start the client** in another terminal:

```bash
python client.py
```

The client connects to the server at `127.0.0.1:5000` and receives the file in chunks.

## How It Works

1. The client sends a connection request.
2. The server responds and sends file information.
3. The file is divided into chunks.
4. The server sends each chunk with its checksum.
5. The client verifies the checksum and acknowledges the chunk.
6. The server signals the end of the transfer.

## Technologies Used

- Python
- UDP sockets
- JSON
- SHA-256 hashing
- Multithreading

## Future Improvements

- NACK-based error recovery
- Timeout and retransmission handling
- Whole-file checksum verification
- Sliding-window protocol (Go-Back-N)
- Support for binary files
