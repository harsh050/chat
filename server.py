import asyncio

clients = {}  # Dictionary to track clients and usernames

# Broadcast a message to all clients
async def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:  # Do not send to the sender
            try:
                await client.send(message)
            except:
                await remove_client(client)

# Handle individual client connections
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    # Send and receive username
    writer.write("Enter your username: ".encode('utf-8'))
    await writer.drain()
    data = await reader.read(100)
    username = data.decode('utf-8').strip()

    if username in clients.values():
        writer.write("Username already taken! Disconnecting...".encode('utf-8'))
        await writer.drain()
        writer.close()
        return

    clients[writer] = username
    print(f"Username {username} added for {addr}")

    # Notify everyone
    await broadcast(f"{username} has joined the chat!".encode('utf-8'), writer)

    while True:
        try:
            # Continuously listen for messages
            data = await reader.read(100)
            message = data.decode('utf-8').strip()

            if not message:
                break  # Client disconnected

            print(f"Received message from {username}: {message}")
            await broadcast(f"{username}: {message}".encode('utf-8'), writer)
        except:
            break

    # Client disconnects
    await remove_client(writer)
    print(f"{username} disconnected")
    writer.close()

async def remove_client(writer):
    username = clients[writer]
    del clients[writer]
    await broadcast(f"{username} has left the chat.".encode('utf-8'), writer)

# Main function to start the server
async def main():
    server_ip = "127.0.0.1"
    server_port = "12345"
    server = await asyncio.start_server(handle_client, server_ip, server_port)
    addr = server.sockets[0].getsockname()
    print(f'Server started on {addr}')

    async with server:
        await server.serve_forever()

# Run the server
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server shut down.")
