# Italian Jokes MCP 🇮🇹

A Model Context Protocol (MCP) server that brings Italian humor to your AI conversations! Built with FastMCP framework and featuring full compatibility with SSE, Studio, and Streamable HTTP protocols.

## Features

- 🎭 **Multiple Joke Categories**: One-liner, Observational, Stereotype, Wordplay, and Long jokes
- 🚀 **FastMCP Framework**: Built on the latest FastMCP 2.0 for optimal performance
- 📡 **Multiple Protocols**: Supports stdio, HTTP, SSE, and WebSocket connections
- 📦 **MCPB Compatible**: Packaged as an MCP Bundle for easy installation
- 🔄 **Streaming Support**: Real-time joke delivery with SSE and WebSocket
- 🎯 **Studio Integration**: Full compatibility with MCP Studio and Claude desktop apps

## Installation

### As MCPB Bundle (Recommended)

1. Download the `.mcpb` file
2. Open with Claude for macOS/Windows or any MCPB-compatible application
3. Follow the installation prompts

### Manual Installation

```bash
# Clone or download the project
cd italian-jokes-mcp

# Install Python dependencies
pip install -r requirements.txt

# Run the MCP server
python server.py

# Or run the HTTP server
python http_server.py
```

## Usage

### MCP Tools

The server provides several tools for accessing Italian jokes:

#### `get_italian_joke`
Get a random Italian joke with optional category filtering.

```python
# Get any joke
get_italian_joke()

# Get a specific type
get_italian_joke(subtype="One-liner")
```

#### `get_multiple_jokes`
Fetch multiple jokes at once (1-10 jokes).

```python
get_multiple_jokes(count=5, subtype="Wordplay")
```

#### `list_joke_categories`
List all available joke categories.

#### `health_check`
Check server and API connectivity status.

### HTTP Endpoints

When running the HTTP server (`python http_server.py`):

- `GET /api/joke` - Get a single joke
- `GET /api/jokes` - Get multiple jokes
- `GET /api/categories` - List categories
- `GET /api/stream/jokes` - SSE joke streaming
- `GET /api/stream/chunked` - Chunked transfer encoding
- `WebSocket /ws/jokes` - Real-time joke delivery

### Available Joke Categories

- **All**: Random jokes from all categories
- **One-liner**: Short, punchy jokes
- **Observational**: Cultural observations and humor
- **Stereotype**: Playful stereotypical jokes
- **Wordplay**: Puns and word-based humor  
- **Long**: Longer narrative jokes

## API Response Format

```json
{
  "success": true,
  "joke": {
    "id": 1,
    "text": "Why did the Italian chef refuse to make pizza? He kneaded some space!",
    "type": "Italian",
    "subtype": "Wordplay"
  }
}
```

## Configuration

The server can be configured through environment variables or the manifest configuration:

- `API_TIMEOUT`: Timeout for API requests (default: 10 seconds)
- `DEFAULT_JOKE_COUNT`: Default number of jokes (default: 3)
- `HTTP_PORT`: HTTP server port (default: 8000)
- `ENABLE_LOGGING`: Enable detailed logging (default: true)

## Development

### Project Structure

```
italian-jokes-mcp/
├── server.py              # Main MCP server
├── http_server.py          # HTTP/SSE/WebSocket server
├── manifest.json           # MCPB manifest
├── requirements.txt        # Python dependencies
├── package.json           # Project metadata
├── README.md              # This file
└── LICENSE                # MIT license
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality

```bash
# Format code
black *.py

# Lint code
flake8 *.py
```

## Compatibility

- **MCP Protocol**: >=1.0.0
- **Python**: >=3.8
- **FastMCP**: >=2.0.0
- **Platforms**: Windows, macOS, Linux
- **Claude**: >=3.0.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Italian Jokes API](https://italian-jokes.vercel.app/) for providing the joke content
- [FastMCP](https://github.com/jlowin/fastmcp) for the excellent MCP framework
- [Anthropic](https://github.com/anthropics/mcpb) for the MCPB specification

---

*Viva la risata! (Long live laughter!)* 🇮🇹