#!/usr/bin/env python3
"""
HTTP Server for Italian Jokes MCP
Provides SSE, Studio, and Streamable HTTP compatibility
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import uvicorn

from server import ItalianJokesAPI, JokeSubtype, JokeResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Italian Jokes HTTP Server...")
    yield
    logger.info("Shutting down Italian Jokes HTTP Server...")

# Initialize FastAPI app
app = FastAPI(
    title="Italian Jokes MCP HTTP Server",
    description="HTTP interface for Italian Jokes MCP with SSE and streaming support",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test API connectivity
        import requests
        response = requests.get("https://italian-jokes.vercel.app/api/jokes", timeout=5)
        api_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        api_status = "unreachable"
    
    return {
        "status": "healthy",
        "api_status": api_status,
        "version": "1.0.0"
    }

# Standard REST endpoints
@app.get("/api/joke")
async def get_joke(subtype: Optional[str] = Query(None, description="Joke subtype")):
    """Get a single Italian joke"""
    try:
        if subtype and subtype not in [e.value for e in JokeSubtype]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid subtype. Available: {', '.join([e.value for e in JokeSubtype])}"
            )
        
        joke_data = ItalianJokesAPI.get_joke(subtype)
        joke_response = JokeResponse(**joke_data)
        
        return {
            "success": True,
            "joke": {
                "id": joke_response.id,
                "text": joke_response.joke,
                "type": joke_response.type,
                "subtype": joke_response.subtype
            }
        }
    except Exception as e:
        logger.error(f"Error getting joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jokes")
async def get_multiple_jokes(
    count: int = Query(3, ge=1, le=10, description="Number of jokes"),
    subtype: Optional[str] = Query(None, description="Joke subtype")
):
    """Get multiple Italian jokes"""
    try:
        if subtype and subtype not in [e.value for e in JokeSubtype]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid subtype. Available: {', '.join([e.value for e in JokeSubtype])}"
            )
        
        jokes = []
        for i in range(count):
            try:
                joke_data = ItalianJokesAPI.get_joke(subtype)
                joke_response = JokeResponse(**joke_data)
                jokes.append({
                    "id": joke_response.id,
                    "text": joke_response.joke,
                    "type": joke_response.type,
                    "subtype": joke_response.subtype
                })
            except Exception as e:
                logger.warning(f"Failed to fetch joke {i+1}: {e}")
                continue
        
        return {
            "success": True,
            "count": len(jokes),
            "jokes": jokes
        }
    except Exception as e:
        logger.error(f"Error getting multiple jokes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    """Get available joke categories"""
    return {
        "success": True,
        "categories": [
            {
                "value": subtype.value,
                "description": f"{subtype.value} jokes"
            }
            for subtype in JokeSubtype
        ]
    }

# SSE (Server-Sent Events) endpoints
async def joke_stream_generator(
    count: int = 5,
    subtype: Optional[str] = None,
    interval: float = 2.0
) -> AsyncGenerator[str, None]:
    """Generate a stream of jokes"""
    for i in range(count):
        try:
            joke_data = ItalianJokesAPI.get_joke(subtype)
            joke_response = JokeResponse(**joke_data)
            
            event_data = {
                "index": i + 1,
                "total": count,
                "joke": {
                    "id": joke_response.id,
                    "text": joke_response.joke,
                    "type": joke_response.type,
                    "subtype": joke_response.subtype
                }
            }
            
            yield f"data: {json.dumps(event_data)}\n\n"
            
            if i < count - 1:  # Don't wait after the last joke
                await asyncio.sleep(interval)
                
        except Exception as e:
            error_data = {
                "error": str(e),
                "index": i + 1,
                "total": count
            }
            yield f"data: {json.dumps(error_data)}\n\n"

@app.get("/api/stream/jokes")
async def stream_jokes(
    count: int = Query(5, ge=1, le=20, description="Number of jokes to stream"),
    subtype: Optional[str] = Query(None, description="Joke subtype"),
    interval: float = Query(2.0, ge=0.5, le=10.0, description="Interval between jokes in seconds")
):
    """Stream jokes using Server-Sent Events"""
    if subtype and subtype not in [e.value for e in JokeSubtype]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subtype. Available: {', '.join([e.value for e in JokeSubtype])}"
        )
    
    return EventSourceResponse(
        joke_stream_generator(count, subtype, interval),
        media_type="text/event-stream"
    )

# Streamable HTTP endpoints (chunked responses)
async def chunked_jokes_generator(
    count: int = 3,
    subtype: Optional[str] = None
) -> AsyncGenerator[bytes, None]:
    """Generate chunked joke responses"""
    yield b'{"success": true, "jokes": ['
    
    for i in range(count):
        try:
            joke_data = ItalianJokesAPI.get_joke(subtype)
            joke_response = JokeResponse(**joke_data)
            
            joke_json = {
                "id": joke_response.id,
                "text": joke_response.joke,
                "type": joke_response.type,
                "subtype": joke_response.subtype
            }
            
            if i > 0:
                yield b','
            
            yield json.dumps(joke_json).encode('utf-8')
            
            # Small delay to demonstrate streaming
            await asyncio.sleep(0.5)
            
        except Exception as e:
            logger.warning(f"Failed to fetch joke {i+1}: {e}")
            continue
    
    yield b']}'

@app.get("/api/stream/chunked")
async def stream_chunked_jokes(
    count: int = Query(3, ge=1, le=10, description="Number of jokes"),
    subtype: Optional[str] = Query(None, description="Joke subtype")
):
    """Stream jokes using chunked transfer encoding"""
    if subtype and subtype not in [e.value for e in JokeSubtype]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subtype. Available: {', '.join([e.value for e in JokeSubtype])}"
        )
    
    return StreamingResponse(
        chunked_jokes_generator(count, subtype),
        media_type="application/json"
    )

# MCP Studio compatibility endpoints
@app.get("/mcp/info")
async def mcp_info():
    """MCP server information for Studio compatibility"""
    return {
        "name": "Italian Jokes MCP",
        "version": "1.0.0",
        "description": "MCP server for Italian jokes with FastMCP framework",
        "capabilities": {
            "tools": [
                "get_italian_joke",
                "get_joke_by_category", 
                "get_multiple_jokes",
                "list_joke_categories",
                "health_check"
            ],
            "resources": ["italian-jokes-api-info"],
            "prompts": ["italian-joke-session"]
        },
        "protocols": ["stdio", "http", "sse"],
        "endpoints": {
            "http": "/api",
            "sse": "/api/stream",
            "health": "/health"
        }
    }

@app.get("/mcp/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "get_italian_joke",
                "description": "Get a random Italian joke",
                "parameters": {
                    "subtype": {
                        "type": "string",
                        "description": "Optional joke subtype",
                        "enum": [e.value for e in JokeSubtype]
                    }
                }
            },
            {
                "name": "get_multiple_jokes",
                "description": "Get multiple Italian jokes",
                "parameters": {
                    "count": {
                        "type": "integer",
                        "description": "Number of jokes (1-10)",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "subtype": {
                        "type": "string",
                        "description": "Optional joke subtype",
                        "enum": [e.value for e in JokeSubtype]
                    }
                }
            },
            {
                "name": "list_joke_categories",
                "description": "List all available joke categories"
            },
            {
                "name": "health_check",
                "description": "Check server and API health"
            }
        ]
    }

# WebSocket support for real-time communication
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/jokes")
async def websocket_jokes(websocket: WebSocket):
    """WebSocket endpoint for real-time joke delivery"""
    await websocket.accept()
    
    try:
        while True:
            # Wait for client message
            data = await websocket.receive_text()
            request = json.loads(data)
            
            command = request.get("command", "get_joke")
            subtype = request.get("subtype")
            count = request.get("count", 1)
            
            if command == "get_joke":
                try:
                    joke_data = ItalianJokesAPI.get_joke(subtype)
                    joke_response = JokeResponse(**joke_data)
                    
                    response = {
                        "success": True,
                        "joke": {
                            "id": joke_response.id,
                            "text": joke_response.joke,
                            "type": joke_response.type,
                            "subtype": joke_response.subtype
                        }
                    }
                    await websocket.send_text(json.dumps(response))
                    
                except Exception as e:
                    error_response = {
                        "success": False,
                        "error": str(e)
                    }
                    await websocket.send_text(json.dumps(error_response))
            
            elif command == "stream_jokes":
                try:
                    for i in range(min(count, 10)):
                        joke_data = ItalianJokesAPI.get_joke(subtype)
                        joke_response = JokeResponse(**joke_data)
                        
                        response = {
                            "success": True,
                            "index": i + 1,
                            "total": count,
                            "joke": {
                                "id": joke_response.id,
                                "text": joke_response.joke,
                                "type": joke_response.type,
                                "subtype": joke_response.subtype
                            }
                        }
                        await websocket.send_text(json.dumps(response))
                        await asyncio.sleep(1)  # Delay between jokes
                        
                except Exception as e:
                    error_response = {
                        "success": False,
                        "error": str(e)
                    }
                    await websocket.send_text(json.dumps(error_response))
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

if __name__ == "__main__":
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )