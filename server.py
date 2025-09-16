#!/usr/bin/env python3
"""
Italian Jokes MCP Server
A Model Context Protocol server that provides Italian jokes using FastMCP framework.
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from enum import Enum

import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Italian Jokes MCP 🇮🇹")

class JokeSubtype(str, Enum):
    """Available joke subtypes from the Italian Jokes API"""
    ALL = "All"
    ONE_LINER = "One-liner"
    OBSERVATIONAL = "Observational"
    STEREOTYPE = "Stereotype"
    WORDPLAY = "Wordplay"
    LONG = "Long"

class JokeResponse(BaseModel):
    """Response model for Italian jokes"""
    id: int
    joke: str
    type: str
    subtype: str

class ItalianJokesAPI:
    """Client for the Italian Jokes API"""
    
    BASE_URL = "https://italian-jokes.vercel.app/api/jokes"
    
    @staticmethod
    def get_joke(subtype: Optional[str] = None) -> Dict[str, Any]:
        """Fetch a joke from the Italian Jokes API"""
        try:
            params = {}
            if subtype and subtype != "All":
                params["subtype"] = subtype
            
            response = requests.get(ItalianJokesAPI.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching joke: {e}")
            raise Exception(f"Failed to fetch joke: {str(e)}")

@mcp.tool
def get_italian_joke(subtype: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a random Italian joke from the Italian Jokes API.
    
    Args:
        subtype: Optional joke subtype. Available options: All, One-liner, Observational, Stereotype, Wordplay, Long
    
    Returns:
        A dictionary containing the joke data with id, joke text, type, and subtype
    """
    try:
        # Validate subtype if provided
        if subtype and subtype not in [e.value for e in JokeSubtype]:
            return {
                "error": f"Invalid subtype. Available options: {', '.join([e.value for e in JokeSubtype])}"
            }
        
        joke_data = ItalianJokesAPI.get_joke(subtype)
        
        # Validate response structure
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
        logger.error(f"Error in get_italian_joke: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool
def get_joke_by_category(category: str) -> Dict[str, Any]:
    """
    Get an Italian joke from a specific category.
    
    Args:
        category: The joke category (One-liner, Observational, Stereotype, Wordplay, Long)
    
    Returns:
        A dictionary containing the joke data
    """
    return get_italian_joke(category)

@mcp.tool
def get_multiple_jokes(count: int = 3, subtype: Optional[str] = None) -> Dict[str, Any]:
    """
    Get multiple Italian jokes at once.
    
    Args:
        count: Number of jokes to fetch (1-10, default: 3)
        subtype: Optional joke subtype filter
    
    Returns:
        A dictionary containing a list of jokes
    """
    try:
        if count < 1 or count > 10:
            return {
                "success": False,
                "error": "Count must be between 1 and 10"
            }
        
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
        logger.error(f"Error in get_multiple_jokes: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool
def list_joke_categories() -> Dict[str, Any]:
    """
    List all available joke categories/subtypes.
    
    Returns:
        A dictionary containing all available joke categories
    """
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

# Add resource for API information
@mcp.resource("file://italian-jokes-api-info")
def get_api_info() -> str:
    """Information about the Italian Jokes API"""
    return """
    Italian Jokes API Information:
    
    Base URL: https://italian-jokes.vercel.app/api/jokes
    
    Available Subtypes:
    - All: Random jokes from all categories
    - One-liner: Short, punchy jokes
    - Observational: Observational humor about Italian culture
    - Stereotype: Playful stereotypical jokes
    - Wordplay: Puns and word-based humor
    - Long: Longer narrative jokes
    
    Response Format:
    {
        "id": number,
        "joke": "string",
        "type": "Italian",
        "subtype": "string"
    }
    """

# Add prompt for joke generation assistance
@mcp.prompt("italian-joke-session")
def joke_session_prompt() -> str:
    """Prompt for starting an Italian joke session"""
    return """
    Welcome to the Italian Jokes session! 🇮🇹
    
    I can help you get Italian jokes in various categories:
    - One-liner: Quick and punchy
    - Observational: Cultural observations
    - Stereotype: Playful stereotypes
    - Wordplay: Puns and word games
    - Long: Story-based jokes
    
    Just ask me for a joke, specify a category, or request multiple jokes!
    
    Examples:
    - "Tell me a joke"
    - "Get me a one-liner joke"
    - "I want 5 wordplay jokes"
    - "Show me all joke categories"
    """

# Health check endpoint for monitoring
@mcp.tool
def health_check() -> Dict[str, Any]:
    """
    Check the health status of the MCP server and API connectivity.
    
    Returns:
        Health status information
    """
    try:
        # Test API connectivity
        response = requests.get("https://italian-jokes.vercel.app/api/jokes", timeout=5)
        api_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        api_status = "unreachable"
    
    return {
        "server": "healthy",
        "api_status": api_status,
        "timestamp": str(asyncio.get_event_loop().time()),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    logger.info("Starting Italian Jokes MCP Server...")
    mcp.run()