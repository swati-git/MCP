#from fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP
import click
import logging

@click.command()
@click.option("--port", default=8000, help="Port to run the server on")
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--log-level", default="INFO", help="Logging level")

def main(port: int, host: str, log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting  Ecommerce MCP Server...")

    mcp = FastMCP(
        "Ecommerce Server",
        host=host,
        port=port,
        stateless_http=True  # Enable streamable HTTP protocol
    )

    @mcp.resource("products://list_products")
    def list_products() -> list:
        """List the products available in the store."""
        products_list = ["Laptop", "Smartphone", "Headphones", "Camera", "Smartwatch"]
        return products_list
  
    @mcp.tool("add_to_cart://{product_name}")
    def add_to_cart(product_name: str) -> str:
        """
        Add a product to the shopping cart.

        This tool allows a client to add a specified product to their shopping cart.
        The product name should match one of the available products.
        """
        # Here, you would typically add the product to a user's cart in a database or session.
        return f"Product '{product_name}' has been added to your cart."
    
    @mcp.tool(
        title="cart checkout",
        description="Proceed to checkout and finalize the purchase of items in the cart.",
    )
    def checkout() -> str:
        # Here, you would typically process the payment and finalize the order.
        return "Checkout complete! Your order has been placed successfully."
    
    try:
        logger.info(f"Ecommerce server running on {host}:{port}")
        mcp.run(transport="streamable-http")  # Use new streamable HTTP transport
    except KeyboardInterrupt:
        logger.info("Server shutting down gracefully...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("Ecommerce server stopped")


if __name__ == "__main__":
    main()