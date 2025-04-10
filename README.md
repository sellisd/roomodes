# Agile Roo Modes Collection

A comprehensive collection of custom Roo modes that work together as an agile team. This collection enables multiple developers and AI agents to collaborate effectively on large projects by providing specialized roles with clear responsibilities and interaction patterns.

## Features

- **Specialized Agile Roles**: Five distinct modes covering key agile team roles
- **Integrated Workflows**: Clear interaction patterns between modes
- **External Integration**: Built-in support for Jira and GitHub
- **Customizable Rules**: Role-specific behaviors and permissions
- **Easy Installation**: Simple setup process for any project

## Available Modes

### Product Owner Mode
- Backlog management and prioritization
- User story creation and refinement
- Product roadmap maintenance
- Stakeholder collaboration
- Feature prioritization

### Scrum Master Mode
- Sprint planning and management
- Team velocity tracking
- Process improvement
- Scrum ceremonies facilitation
- Impediment removal

### Tech Lead Mode
- Technical decision making
- Architecture review and planning
- Code standards enforcement
- Technical debt management
- Design pattern guidance

### Developer Mode
- Code implementation
- Unit testing
- Code review
- Technical documentation
- Bug fixing

### QA Mode
- Test strategy development
- Test case management
- Quality metrics tracking
- Bug reporting and verification
- Release validation

## Setup and Configuration

1. **Prerequisites**
   - Get a Jira API key from your Atlassian cloud account
   - Generate a GitHub personal access token
   - Install the required MCP servers:
     ```bash
     # For Jira integration
     uvx mcp-atlassian --jira-url=https://your-domain.atlassian.net \
                       --jira-username=your-email@domain.com \
                       --jira-token=YOUR_TOKEN

     # For GitHub integration
     docker pull ghcr.io/github/github-mcp-server
     ```

2. **Installation**
   Run the Python installer script to set up the custom modes in your project:
   ```bash
   ./modes_installer.py --target /path/to/your/project
   ```

   This will:
   - Create the .roomodes file with custom modes
   - Copy the roorules files to your project root
   - Set up MCP configuration for Jira and GitHub

3. **Configuration**
   - Update `.roo/mcp.json` with your Jira and GitHub credentials
   - Customize mode rules in `.roorules-*` files if needed
   - Adjust file access permissions in mode definitions if required

## Mode Interaction Patterns

```mermaid
sequenceDiagram
    participant PO as Product Owner
    participant SM as Scrum Master
    participant TL as Tech Lead
    participant DEV as Developer
    participant QA as QA

    PO->>SM: Create Sprint
    SM->>TL: Request Technical Review
    TL->>DEV: Provide Technical Guidelines
    DEV->>QA: Submit Implementation
    QA->>SM: Report Testing Status
    SM->>PO: Update Sprint Progress
```

## Best Practices

### Mode Selection
- Choose the appropriate mode based on your current task
- Switch modes when transitioning between different responsibilities
- Use mode-specific tools and capabilities effectively

### Documentation
- Each mode maintains its specific documentation
- Cross-reference documents between modes when needed
- Use standardized templates for consistency

### Workflow Integration
- Follow the established mode interaction patterns
- Use Jira for task tracking and management
- Maintain GitHub integration for code management

### Quality Assurance
- Each mode has built-in quality checks
- Follow role-specific best practices
- Maintain continuous feedback loops

## Development Guidelines

### Adding New Modes
1. Create mode configuration in `modes/`
2. Define mode rules in `roorules/`
3. Update installer script
4. Document mode interactions

### Customizing Existing Modes
1. Modify mode JSON configuration
2. Update corresponding roorules
3. Test mode interactions
4. Update documentation

### Contributing
1. Fork the repository
2. Create feature branch
3. Submit pull request
4. Add tests and documentation

## Troubleshooting

### Common Issues
- **Mode Switching Failed**: Check file permissions and git status
- **MCP Integration Error**: Verify API credentials
- **Rule Conflicts**: Review mode definitions and rules

### Support
- Check documentation in `docs/` directory
- Submit issues via GitHub
- Contact maintainers for support

## License

MIT License - See [LICENSE](LICENSE) for details

## Future Enhancements

- Additional specialized modes
- Enhanced automation capabilities
- Extended template library
- Advanced workflow patterns
- Custom MCP server integrations