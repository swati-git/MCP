from google.adk.agents.llm_agent import LlmAgent
#from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from typing import List, Dict, Any, Optional
from src.utils.config_loader import config_loader
import logging
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
import asyncio

logger = logging.getLogger(__name__)

class AgentWrapper:

    def __init__(self, tool_filter: Optional[List[str]] = None):
        """
        Initialize the agent wrapper.
        
        Args:
            tool_filter: Optional list of tool names to allow. If None, all tools are loaded.
        """
        self.tool_filter = tool_filter
        self.agent: Optional[LlmAgent] = None
        self.toolsets: List[MCPToolset] = []
        self.server_status: Dict[str, str] = {}
        
        logger.info("AgentWrapper initialized")
        if tool_filter:
            logger.info(f"Tool filter active: {tool_filter}")


    async def _build_agent(self) -> None:
            logger.info("Building agent ...")
            
            try:
                toolsets = await self._load_toolsets()
                
                if not toolsets:
                    logger.warning("No toolsets loaded - agent will have no tools available")
                
                self.agent = LlmAgent(
                    model="gemini-2.0-flash-exp", 
                    name="mcp_assistant",
                    instruction=self._get_agent_instruction(),
                    tools=[tool for tool in toolsets]  # Creates new list of ToolUnion, to avoid the error list invariant
                )
                
                self.toolsets = toolsets
                logger.info(f"Agent built successfully with {len(toolsets)} toolsets")
                
            except Exception as e:
                logger.error(f"Failed to build agent: {e}")
                raise

    def _get_agent_instruction(self) -> str:
            """Get the system instruction that defines the agent's behavior and capabilities."""
            return """You are a helpful assistant with access to tools that can help users view the products and add them to a shopping cart."""

    async def _load_toolsets(self) -> List[MCPToolset]:
            """
            Load toolsets from configured MCP servers.
            
            This method iterates through  configured servers, attempts to connect
            and loads their available tools into MCPToolset instances.
            
            Returns:
                List of successfully connected MCPToolset instances.
            """
            servers = config_loader.get_servers()
            toolsets = []
            
            logger.info(f"Loading toolsets from {len(servers)} configured servers...")
            
            for server_name, server_config in servers.items():
                try:
                    if not config_loader.validate_server_config(server_name, server_config):
                        self.server_status[server_name] = "invalid_config"
                        continue
                    
                    # Create connection parameters based on server type
                    connection_params = await self._create_connection_params(
                        server_name, server_config
                    )
                    
                    if not connection_params:
                        self.server_status[server_name] = "connection_failed"
                        continue
                    
                    toolset = MCPToolset(
                        connection_params=connection_params,
                        tool_filter=self.tool_filter  # Apply tool filtering if specified
                    )
                    

                    tools = await toolset.get_tools()
                    tool_names = [tool.name for tool in tools]
                    
                    if tools:
                        toolsets.append(toolset)
                        self.server_status[server_name] = "connected"
                        logger.info(f"Connected to {server_name}: {len(tool_names)} tools loaded")
                    else:
                        logger.warning(f"No tools found on server '{server_name}'")
                        self.server_status[server_name] = "no_tools"
                        
                except Exception as e:
                    logger.error(f"Failed to connect to server '{server_name}': {e}")
                    self.server_status[server_name] = f"error: {str(e)}"
                    continue
            
            logger.info(f"Successfully loaded {len(toolsets)} toolsets")
            return toolsets


    async def _create_connection_params(
            self, 
            server_name: str, 
            server_config: Dict[str, Any]
        ) -> Optional[Any]:
            """
            Create appropriate connection parameters based on server transport type.
            
            Args:
                server_name: Name of the server for logging
                server_config: Server configuration dictionary
                
            Returns:
                Connection parameters object or None if creation failed
            """
            server_type = server_config["type"]
            
            try:
                if server_type == "http":
                    # Create HTTP connection parameters for streamable HTTP servers
                    return StreamableHTTPServerParams(url=server_config["url"])
                else:
                    raise ValueError(f"Unsupported server type: {server_type}")
                    
            except Exception as e:
                logger.error(f"Error creating connection params for '{server_name}': {e}")
                return None
            
    async def close(self) -> None:
        """
        Gracefully close all toolset connections and cleanup resources.
        """
        logger.info("Shutting down agent and closing toolset connections...")
        
        for i, toolset in enumerate(self.toolsets):
            try:
                await toolset.close()
                logger.debug(f"Closed toolset {i+1}")
            except Exception as e:
                logger.error(f"Error closing toolset {i+1}: {e}")
        
        self.toolsets.clear()
        self.agent = None
        
        # Small delay to ensure cleanup completes
        await asyncio.sleep(0.5)
        logger.info("Agent shutdown complete")
    
    def get_server_status(self) -> Dict[str, str]:
        """Get the current connection status of all configured servers."""
        return self.server_status.copy()

    def is_ready(self) -> bool:
        """Check if the agent is properly initialized and ready for use."""
        return self.agent is not None
