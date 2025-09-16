# Italian Jokes MCP Server 🇮🇹

A Model Context Protocol (MCP) server that provides access to Italian jokes through the Italian Jokes API. This server allows AI assistants to fetch and share Italian jokes with various subtypes.

## Features

- 🎭 **Multiple Joke Types**: Access jokes from different subtypes including One-liner, Observational, Stereotype, Wordplay, and Long jokes
- 🔄 **Random Selection**: Get random jokes or specify a particular subtype
- 🌐 **API Integration**: Seamlessly integrates with the Italian Jokes API
- 📝 **Rich Formatting**: Returns jokes with proper formatting and metadata
- ⚡ **Fast Response**: Optimized for quick joke retrieval

## Available Tools

### `get_italian_joke`
Retrieves a random Italian joke or a joke of a specific subtype.

**Parameters:**
- `subtype` (optional): The type of joke to fetch
  - Available options: `All`, `One-liner`, `Observational`, `Stereotype`, `Wordplay`, `Long`

### `list_joke_subtypes`
Lists all available Italian joke subtypes.

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Build the project:
   ```bash
   npm run build
   ```

## Usage

### Development
Run the server in development mode:
```bash
npm run dev
```

### Production
Build and run the server:
```bash
npm run build
npm start
```

### Integration with Claude Desktop

Add this server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "italian-jokes": {
      "command": "node",
      "args": ["path/to/italian-jokes-mcp-server/dist/index.js"]
    }
  }
}
```

## API Reference

This server integrates with the [Italian Jokes API](https://italian-jokes.vercel.app/) which provides:

- **Endpoint**: `GET /api/jokes`
- **Query Parameters**: 
  - `subtype`: Filter jokes by subtype
- **Response Format**:
  ```json
  {
    "id": 1,
    "joke": "Why did the Mafia cross the road? Forget about it.",
    "type": "Italian",
    "subtype": "One-liner"
  }
  ```

## Example Usage

Once integrated with an MCP-compatible client:

1. **Get a random joke**:
   - Use the `get_italian_joke` tool without parameters

2. **Get a specific type of joke**:
   - Use the `get_italian_joke` tool with `subtype: "One-liner"`

3. **List available subtypes**:
   - Use the `list_joke_subtypes` tool

## Error Handling

The server includes comprehensive error handling for:
- Network timeouts
- API unavailability
- Invalid subtypes
- Malformed responses

## Contributing

Feel free to contribute by:
- Adding new features
- Improving error handling
- Enhancing documentation
- Reporting bugs

## License

MIT License - feel free to use this in your own projects!

---

*Viva la risata! (Long live laughter!)* 🎉