# Roomodes

A collection of custom Roo modes for agile software development


## Setup and configuration

- Get an API key from your atlassian JIRA cloud account
- Use with https://github.com/sooperset/mcp-atlassian
  configure it in `.roo/mcp.json` in the root of your project directory
```shell 
{
  "mcpServers": {
    "atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian",
         "--jira-url=https://domainname.atlassian.net",
         "--jira-username=email@address.com",
         "--jira-token=TOKEN" ],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Usage

Concatenate the `json` modes and save it as `.roomodes` in your project root directory
