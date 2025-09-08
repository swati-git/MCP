from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


async def main():
    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read_stream, write_stream, _,):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            init_response = await session.initialize()
            print("Initialization response:", init_response.serverInfo)
            

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())