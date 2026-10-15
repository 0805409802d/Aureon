from fastapi import APIRouter, Body
from typing import Dict, Any
from src.mcp.server import McpProtocolHandler, MCP_TOOLS, MCP_RESOURCES, MCP_PROMPTS

router = APIRouter(prefix="/api/mcp", tags=["Model Context Protocol (MCP)"])

@router.get("/tools")
def get_mcp_tools():
    """Lista las herramientas disponibles en el servidor MCP de Aureon."""
    return {"tools": MCP_TOOLS}

@router.post("/tools/call")
def call_mcp_tool(payload: Dict[str, Any] = Body(...)):
    """Ejecuta una herramienta del servidor MCP de Aureon."""
    tool_name = payload.get("name", "")
    args = payload.get("arguments", {})
    result = McpProtocolHandler.execute_tool(tool_name, args)
    return {"name": tool_name, "result": result}

@router.get("/resources")
def get_mcp_resources():
    """Lista los recursos expuestos en el protocolo MCP."""
    return {"resources": MCP_RESOURCES}

@router.get("/resources/read")
def read_mcp_resource(uri: str):
    """Lee el contenido de un recurso MCP por su URI."""
    return McpProtocolHandler.read_resource(uri)

@router.get("/prompts")
def get_mcp_prompts():
    """Lista los prompts pedagógicos socráticos de MCP."""
    return {"prompts": MCP_PROMPTS}

@router.post("/rpc")
def handle_json_rpc(payload: Dict[str, Any] = Body(...)):
    """Punto de entrada JSON-RPC 2.0 oficial compatible con cualquier cliente MCP."""
    return McpProtocolHandler.handle_request(payload)
