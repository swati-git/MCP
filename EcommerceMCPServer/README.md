## Prerequisites

- Python 3.10 or higher  
- `uv` package manager

Please ensure you have both installed before proceeding.

If you don't have uv installed, install it:

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

To Install dependencies:

# Create virtual env and activate it
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv add fastmcp

# Verify the installation using
fastmcp version

# Features
Server uses HTTP/Streamable transport protocol