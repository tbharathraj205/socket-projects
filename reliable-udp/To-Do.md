1. Fix packet validation and NACK handling
Start here
Your client currently sends an ACK even when a chunk is invalid. Change the protocol so that:
- Valid chunk → send ACK.
- Invalid checksum → send NACK.
- Wrong sequence number → reject the chunk.
- Duplicate chunk → don't write it twice.
Goal: The receiver never saves corrupted or duplicate data.




2. Add timeout and retransmission

UDP doesn't guarantee delivery. If an ACK is lost, your server may wait forever or become out of sync.
- Start a timer after sending each chunk.
- If no ACK arrives, resend the chunk.
- Limit retries, for example, to 5 attempts.
- Handle socket timeouts without crashing.
Goal: The transfer recovers from lost packets and ACKs.




3. Verify the complete file

A chunk checksum alone doesn't prove the entire file was reconstructed correctly.
- Calculate SHA-256 for the original file.
- Calculate SHA-256 for the received file.
- Compare the two hashes before confirming completion.
Goal: Both files must match byte for byte.




4. Transfer bytes instead of text lines

Your current implementation divides text into lines. Real file transfer should support PDFs, images, ZIP files, and other binary files.
- Read the file in fixed-size byte chunks.
- Encode the payload safely for your JSON protocol, or use a binary packet format.
- Reconstruct the exact original bytes.
Goal: Transfer any file type without corrupting its contents.




5. Implement Go-Back-N sliding window

Your current Stop-and-Wait approach sends one chunk and waits for its ACK. Go-Back-N allows multiple chunks to be in flight.
- Maintain a sending window.
- Track sequence numbers and ACKs.
- Retransmit outstanding chunks after a timeout.
- Compare throughput against Stop-and-Wait.
Goal: Improve transfer speed and understand reliable transport protocols.




6. Test network failures and measure performance

Create a separate test script that simulates:
- Lost data packets.
- Lost ACKs.
- Corrupted payloads.
- Duplicate packets.
- Out-of-order packets.
Measure transfer time, throughput, retransmissions, and successful file verification.

Goal: Demonstrate that your protocol works under unreliable network conditions.




7. Refactor into classes

As you requested for future development, organize the code into classes such as UDPClient, UDPServer, and Packet.

Separate networking, protocol logic, file handling, and testing.

Goal: Make the project easier to maintain and extend.