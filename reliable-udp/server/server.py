import socket
import json
import os
import hashlib
import time
import threading


FORMAT = 'utf-8'
FILE_INFO = {
    "transfer_id": "abc123",
    "chunk_no": 0,
    "filename": "sample.txt",
    "total_chunks": 3,
    "checksum_algorithm": "SHA-256",
}
FILE_NAME = "sample.txt"
CHUNK_SENT = []
text = {}

f = open(FILE_NAME, "r")
for line_number, line in enumerate(f, start=1):
    text[f"Line {line_number}"] = line
f.close()

CURRENT_CHUNK = -1
LINES_PER_CHUNK = 3
TOTAL_CHUNKS = (len(text) + LINES_PER_CHUNK - 1) // LINES_PER_CHUNK

def checksum(payload):
    text = " ".join(payload)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def server_process(request):
    global CURRENT_CHUNK

    flag = request["flag"]
    #print(request)

    if flag == "SYN":
        response = {
            "flag": "SYN-ACK"
        }
        print(f"flag: {flag} | Client Synchronisede")

    elif flag == "ACK" and "chunk_no" not in request:
        response = {
            "flag": "START",
            "transfer_id": FILE_INFO["transfer_id"],
            "filename": FILE_INFO["filename"],
            "file_size": os.path.getsize(FILE_NAME),
            "total_chunks": TOTAL_CHUNKS,
            "checksum_algorithm": FILE_INFO["checksum_algorithm"],
        }
        print(f"flag: {flag} | Client Synchronisede-Acknowledget")

    elif flag == "START-ACK":
        

        if TOTAL_CHUNKS == 0:
            response = {
                "flag": "END"
            }
        else:
            CURRENT_CHUNK = 0
            chunk_start = CURRENT_CHUNK * LINES_PER_CHUNK
            payload = list(text.values())[
                chunk_start:chunk_start + LINES_PER_CHUNK
            ]

            response = {
                "flag": "DATA",
                "transfer_id": FILE_INFO["transfer_id"],
                "filename": FILE_INFO["filename"],
                "chunk_no": CURRENT_CHUNK,
                "chunk_checksum": checksum(payload),
                "payload": payload
            }
            print(f"flag: {flag} | Client asked for File information")

    elif flag == "ACK":
        chunk_no = int(request["chunk_no"])

        if chunk_no == CURRENT_CHUNK:
            CHUNK_SENT.append(chunk_no)
            CURRENT_CHUNK += 1

            if CURRENT_CHUNK >= TOTAL_CHUNKS:
                response = {
                    "flag": "END"
                }
            else:
                chunk_start = CURRENT_CHUNK * LINES_PER_CHUNK
                payload = list(text.values())[
                    chunk_start:chunk_start + LINES_PER_CHUNK
                ]

                response = {
                    "flag": "DATA",
                    "transfer_id": FILE_INFO["transfer_id"],
                    "filename": FILE_INFO["filename"],
                    "chunk_no": CURRENT_CHUNK,
                    "chunk_checksum": checksum(payload),
                    "payload": payload
                }
            print(f"flag: {flag} | Chunk no: {CURRENT_CHUNK}")
        else:
            response = {
                "flag": "END"
            }

    elif flag == "COMPLETE":
        response = {
            "flag": "COMPLETE"
        }
        print(f"flag: {flag} | Client Received all the chunks")
    else:
        response = {
            "flag": "ERROR",
            "message": "Unknown flag"
        }
        print(f"flag: {flag} | Client Error occured")

    return response


# Initialise the server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 5000))

print("Server started")


def handle_client(server):
    try:
        while True:
            data, addr = server.recvfrom(1024)
            print(addr)
            response = server_process(json.loads(data.decode(FORMAT)))
            

            server.sendto(json.dumps(response).encode(FORMAT), addr)
    except KeyboardInterrupt:
        server.close()
    
thread = threading.Thread(target=handle_client, args=(server,))
thread.start()
