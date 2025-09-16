#!/usr/bin/env node

/**
 * Italian Jokes MCP Server
 * 
 * A Model Context Protocol server that provides access to Italian jokes
 * through the Italian Jokes API created by Daniel Bliss.
 * 
 * Data Source: https://italian-jokes.vercel.app/
 * Original API: https://github.com/d-bliss/italian-jokes-api
 * 
 * This server acts as a bridge between the Model Context Protocol
 * and the Italian Jokes API service.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';

// Italian Jokes API configuration
const ITALIAN_JOKES_API_BASE = 'https://italian-jokes.vercel.app/api/jokes';

// Available joke subtypes
const JOKE_SUBTYPES = [
  'All',
  'One-liner',
  'Observational',
  'Stereotype',
  'Wordplay',
  'Long'
] as const;

type JokeSubtype = typeof JOKE_SUBTYPES[number];

interface JokeResponse {
  id: number;
  joke: string;
  type: string;
  subtype: string;
}

class ItalianJokesServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'italian-jokes-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'get_italian_joke',
            description: 'Get a random Italian joke or a joke of a specific subtype',
            inputSchema: {
              type: 'object',
              properties: {
                subtype: {
                  type: 'string',
                  description: 'The subtype of joke to fetch',
                  enum: JOKE_SUBTYPES,
                },
              },
              additionalProperties: false,
            },
          },
          {
            name: 'list_joke_subtypes',
            description: 'List all available Italian joke subtypes',
            inputSchema: {
              type: 'object',
              properties: {},
              additionalProperties: false,
            },
          },
        ] satisfies Tool[],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'get_italian_joke':
            return await this.getItalianJoke(args?.subtype as JokeSubtype);

          case 'list_joke_subtypes':
            return await this.listJokeSubtypes();

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${errorMessage}`,
            },
          ],
        };
      }
    });
  }

  private async getItalianJoke(subtype?: JokeSubtype) {
    try {
      let url = ITALIAN_JOKES_API_BASE;
      
      if (subtype && subtype !== 'All') {
        url += `?subtype=${encodeURIComponent(subtype)}`;
      }

      const response = await axios.get<JokeResponse>(url, {
        timeout: 10000,
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'Italian-Jokes-MCP-Server/1.0.0',
        },
      });

      const joke = response.data;

      return {
        content: [
          {
            type: 'text',
            text: `🇮🇹 **Italian Joke** (${joke.subtype})

${joke.joke}

---
*Joke ID: ${joke.id} | Type: ${joke.type}*`,
          },
        ],
      };
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 404) {
          throw new Error('No jokes found for the specified subtype');
        } else if (error.code === 'ECONNABORTED') {
          throw new Error('Request timeout - the Italian Jokes API is not responding');
        } else {
          throw new Error(`API Error: ${error.response?.status || 'Unknown'} - ${error.message}`);
        }
      }
      throw new Error(`Failed to fetch Italian joke: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private async listJokeSubtypes() {
    return {
      content: [
        {
          type: 'text',
          text: `🇮🇹 **Available Italian Joke Subtypes:**

${JOKE_SUBTYPES.map((subtype, index) => `${index + 1}. **${subtype}**${subtype === 'All' ? ' (Random from all subtypes)' : ''}`).join('\n')}

Use the \`get_italian_joke\` tool with the \`subtype\` parameter to get jokes of a specific type, or omit the parameter for a random joke.

*Viva la risata! (Long live laughter!)*`,
        },
      ],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Italian Jokes MCP server running on stdio');
  }
}

const server = new ItalianJokesServer();
server.run().catch(console.error);