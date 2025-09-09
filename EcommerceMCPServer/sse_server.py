#from fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EcommerceMCPServer")


@mcp.resource("greeting://{name}")
def greet(name: str = "Customer") -> str:
    """Greet customer by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":

    mcp.run(transport="stdio")