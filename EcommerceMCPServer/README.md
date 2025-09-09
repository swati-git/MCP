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
uv add mcp

# Verify the installation using
mcp version

# Features
sse_server uses stio transport protocol

# Dev tools

For monitoring the logs install tmux(Terminal Multiplexing)
brew install tmux
[tmux](https://jeongwhanchoi.medium.com/install-tmux-on-osx-and-basics-commands-for-beginners-be22520fd95e)

# Testing tools

MCP inspector , which comes bundled in the mcp package