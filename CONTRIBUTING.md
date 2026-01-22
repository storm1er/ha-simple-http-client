# Contributing to Simple cURL

Thank you for your interest in contributing to Simple cURL for Home Assistant! This document provides guidelines for contributing and instructions for publishing the integration to HACS.

## Ways to Contribute

- Report bugs via [GitHub Issues](https://github.com/storm1er/ha-simple-curl/issues)
- Suggest new features or improvements
- Submit pull requests for bug fixes or enhancements
- Improve documentation
- Help answer questions from other users

## Development Setup

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your changes
4. Make your changes and test them
5. Submit a pull request

### Testing Locally

To test your changes:

1. Copy the `custom_components/simple_curl` folder to your Home Assistant `custom_components` directory
2. Add to your `configuration.yaml`:
   ```yaml
   simple_curl:
   ```
3. Restart Home Assistant
4. Verify the service appears in **Developer Tools** → **Services**
5. Test the service in your automations or scripts
6. Check Home Assistant logs for any errors

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Handle errors gracefully

## Submitting Pull Requests

1. Ensure your code passes all validation checks (see below)
2. Update the README if you're adding new features
3. Add examples for new functionality
4. Update the version number in `manifest.json`
5. Create a clear, descriptive pull request

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

Update the version in:
- `custom_components/simple_curl/manifest.json`
- Git tag when creating a release

## Additional Resources

### HACS Documentation
- [HACS Publisher Documentation](https://www.hacs.xyz/docs/publish/)
- [HACS Integration Requirements](https://www.hacs.xyz/docs/publish/integration/)
- [HACS Default Repository Inclusion](https://www.hacs.xyz/docs/publish/include/)

### Home Assistant Documentation
- [Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest/)
- [Service Development](https://developers.home-assistant.io/docs/dev_101_services/)
- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)

### Repositories
- [HACS Default Repository](https://github.com/hacs/default)
- [Integration Blueprint](https://github.com/jpawlowski/hacs.integration_blueprint)

## Questions or Problems?

- Check existing [GitHub Issues](https://github.com/storm1er/ha-simple-curl/issues)
- Create a new issue with detailed information
- For HACS-specific questions, see [HACS documentation](https://www.hacs.xyz/)

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
