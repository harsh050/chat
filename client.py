import asyncio

# Function to handle receiving messages
async def receive_messages(reader):
    while True:
        try:
            message = await reader.read(100)
            print(message.decode('utf-8').strip())
        except:
            print("Disconnected from the server.")
            break

# Function to handle sending messages
async def send_messages(writer, username):
    while True:
        message = input('')
        writer.write(f'{username}: {message}'.encode('utf-8'))
        await writer.drain()

async def main():
    username = input("Enter your username: ")

    # Connect to the server
    reader, writer = await asyncio.open_connection('127.0.0.1', 12345)
    
    # Start receiving and sending message tasks concurrently
    asyncio.create_task(receive_messages(reader))
    await send_messages(writer, username)

# Run the client
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Client shut down.")
