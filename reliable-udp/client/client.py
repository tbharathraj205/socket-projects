import socket
import json
import hashlib
import time
import os

FORMAT = 'utf-8'
CHUNK_RECEIVED = []
FILE_INFO = {
    "transfer_id": None,
    "chunk_no": -1,
    "filename": None,
    "total_chunks": None,
    "checksum_algorithm": None,
}
def write(payload, no):
    

    with open("sample.txt", "a", encoding="utf-8") as file:
        file.writelines(f"{line}\n" for line in payload)

    print(f"Chunk {no} added")

def checksum(payload, chunk_checksum):
    text = " ".join(payload)
    payload_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return chunk_checksum == payload_hash

def client_process(response):
    flag = response["flag"]
    request = {}

    if flag == "SYN-ACK":
        request = {
            "flag": "ACK",
        }
        print("Server Acknowledged")

    elif flag == "START":

        # storeing the rsponse to the client machine
        FILE_INFO["transfer_id"] = response["transfer_id"]
        FILE_INFO["filename"] = response["filename"]
        FILE_INFO["total_chunks"] = response["total_chunks"]
        FILE_INFO["checksum_algorithm"] = response["checksum_algorithm"]

        request = {
            "flag": "START-ACK",
            "transfer_id": FILE_INFO["transfer_id"],
            "chunk_no": FILE_INFO["chunk_no"],
        }

    elif flag == "DATA":

        # to check if this is the correct file(filename,tranfer_id,chunk_no,checksum)
        payload = response["payload"]

        if (
            response["filename"] == FILE_INFO["filename"]
            and response["transfer_id"] == FILE_INFO["transfer_id"]
            and response["chunk_no"] == FILE_INFO["chunk_no"] + 1
            and checksum(payload, response["chunk_checksum"])
        ):
            FILE_INFO["chunk_no"] = response["chunk_no"]
            
            write(payload,FILE_INFO["chunk_no"]) # to writethe paylaod into a file

            for line in payload:
                CHUNK_RECEIVED.append(line)

            request = {
                "flag": "ACK",
                "transfer_id": FILE_INFO["transfer_id"],
                "chunk_no": FILE_INFO["chunk_no"]
            }
            print(f"Flag: {flag} | Chunk no: {FILE_INFO["chunk_no"] - 1}")
        else:
            request = {
                "flag": "ACK",
                "transfer_id": FILE_INFO["transfer_id"],
                "chunk_no": FILE_INFO["chunk_no"]
            }
            print(f"flag: {flag} | Server sent wrong file Requesting{FILE_INFO["chunk_no"]}")

    elif flag == "END":
        print("All chunks received")
        request = {
            "flag": "COMPLETE",
            "transfer_id": FILE_INFO["transfer_id"]
        }
        

    return request


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

request = {
    "flag": "SYN"
}

client.sendto(json.dumps(request).encode(FORMAT), ("127.0.0.1", 5000))

while True:
    data, addr = client.recvfrom(1024)
    response = json.loads(data.decode(FORMAT))

    if response["flag"] == "COMPLETE":
        print("Transfer completed")
        break

    request = client_process(response)
    #time.sleep(10)

    client.sendto(json.dumps(request).encode(FORMAT), addr)

#print(CHUNK_RECEIVED)
client.close()