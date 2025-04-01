# Roomodes

A collection of custom Roo modes for agile software development. With these custom modes the heavy load of long term planning is moved out of the project and promts and into a dedicated system. Thus multiple developers and agents can collaborate on the same large project.


## Setup and configuration

- Get an API key from your atlassian JIRA cloud account
- Use with https://github.com/sooperset/mcp-atlassian
  configure `.roo/mcp.json` in the root of your project directory
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

Run the Python installer script to set up the custom modes in your project:

```shell
./modes_installer.py --target /path/to/your/project
```

This will:
- Create the .roomodes file with custom modes
- Copy the clinerules files to your project root
