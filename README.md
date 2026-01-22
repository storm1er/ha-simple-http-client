# Home Assistant Simple cURL Integration

A simple Home Assistant custom integration that provides a service to fetch URLs with custom methods and headers, returning the response as a variable for use in automations and scripts.

## Installation

1. Copy the `custom_components/simple_curl` folder to your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. The integration will be loaded automatically.

## Features

- No configuration required - just install and use
- Fetch any URL with custom HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.)
- Set custom headers
- Send request body
- Response data stored in variables for use in automations
- Returns status code, content, and response headers

## Service: `simple_curl.fetch`

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | Yes | - | The URL to fetch |
| `method` | No | `GET` | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) |
| `headers` | No | `{}` | HTTP headers as key-value pairs |
| `body` | No | - | Request body content |
| `timeout` | No | `10` | Request timeout in seconds |

### Response Data

The service returns a dictionary with:
- `status`: HTTP status code (integer)
- `content`: Response body as text (string)
- `headers`: Response headers (dictionary)
- `error`: Error message if request failed (string, only present on error)

### How `response_variable` Works

This service is registered with `supports_response=SupportsResponse.ONLY`, which means it **always returns data**. Home Assistant automatically captures the returned dictionary when you specify `response_variable` in your service call.

**The mechanism:**
1. The service handler returns a dictionary (in the Python code)
2. When you call the service with `response_variable: my_var_name`
3. Home Assistant automatically stores that dictionary in the variable `my_var_name`
4. You can then access it in subsequent actions: `{{ my_var_name.content }}`, `{{ my_var_name.status }}`, etc.

This is a built-in Home Assistant feature for services that return data - you don't need to do anything special beyond adding `response_variable` to your service call.

## Usage Examples

### Basic GET Request in Automation

```yaml
automation:
  - alias: "Fetch API Data"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: simple_curl.fetch
        data:
          url: "https://api.example.com/data"
        response_variable: api_response

      - service: notify.notify
        data:
          message: "API returned: {{ api_response.content }}"
```

### POST Request with Headers

```yaml
script:
  fetch_with_auth:
    sequence:
      - service: simple_curl.fetch
        data:
          url: "https://api.example.com/endpoint"
          method: "POST"
          headers:
            Authorization: "Bearer your_token_here"
            Content-Type: "application/json"
          body: '{"key": "value"}'
        response_variable: result

      - condition: template
        value_template: "{{ result.status == 200 }}"

      - service: persistent_notification.create
        data:
          title: "Success"
          message: "Response: {{ result.content }}"
```

### Using Response in Conditions

```yaml
automation:
  - alias: "Check API and Act"
    trigger:
      - platform: state
        entity_id: input_boolean.check_api
        to: "on"
    action:
      - service: simple_curl.fetch
        data:
          url: "https://api.example.com/status"
        response_variable: api_data

      - if:
          - condition: template
            value_template: "{{ api_data.status == 200 }}"
        then:
          - service: light.turn_on
            target:
              entity_id: light.living_room
        else:
          - service: persistent_notification.create
            data:
              message: "API request failed with status {{ api_data.status }}"
```

### Extracting JSON Response

```yaml
script:
  process_json_api:
    sequence:
      - service: simple_curl.fetch
        data:
          url: "https://api.example.com/json"
          headers:
            Accept: "application/json"
        response_variable: api_response

      - variables:
          parsed_data: "{{ api_response.content | from_json }}"

      - service: input_text.set_value
        target:
          entity_id: input_text.api_result
        data:
          value: "{{ parsed_data.field_name }}"
```

### Error Handling

```yaml
automation:
  - alias: "Fetch with Error Handling"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    action:
      - service: simple_curl.fetch
        data:
          url: "https://api.example.com/data"
          timeout: 5
        response_variable: response

      - if:
          - condition: template
            value_template: "{{ 'error' in response }}"
        then:
          - service: persistent_notification.create
            data:
              title: "API Error"
              message: "Failed to fetch: {{ response.error }}"
        else:
          - service: logbook.log
            data:
              name: "API Success"
              message: "Status: {{ response.status }}"
```

## Notes

- The service returns response data that can be captured using `response_variable`
- Response content is always returned as text - use `from_json` filter for JSON responses
- Network errors and timeouts are caught and returned in the `error` field
- Status code `0` indicates a network/connection error

## Publishing to HACS

This repository is structured to be published to the Home Assistant Community Store (HACS). Here's how to get your integration listed in the HACS default repository:

### Prerequisites

Before submitting to HACS, you need to:

1. **Update the repository URLs** - Replace all instances of `yourusername` with your actual GitHub username in:
   - `custom_components/simple_curl/manifest.json` (documentation, issue_tracker, codeowners)
   - `info.md`
   - This README

2. **Create a GitHub repository** - Push this code to a public GitHub repository

3. **Create icon/logo assets** for the Home Assistant brands repository:
   - Icon: 256x256px square PNG
   - Logo (optional): Landscape PNG respecting your brand

### Step-by-Step Submission Process

#### 1. Submit to home-assistant/brands

First, add your integration's visual assets:

1. Fork the [home-assistant/brands](https://github.com/home-assistant/brands) repository
2. Create the directory `custom_integrations/simple_curl/`
3. Add your assets:
   - `icon.png` (256x256px, square)
   - `icon@2x.png` (512x512px, square, optional)
   - `logo.png` (landscape, optional)
   - `logo@2x.png` (2x resolution, optional)
4. Create a pull request

**Image Requirements:**
- Icons must be square (1:1 aspect ratio)
- Icons should be 128-256px (normal) and 256-512px (hDPI)
- Logos should be landscape and respect your brand's aspect ratio
- Use PNG format
- Do not use Home Assistant branded images

#### 2. Validate Your Repository

Ensure your repository passes automated checks:

1. **GitHub Actions are set up** - The `.github/workflows/validate.yml` file runs:
   - HACS validation
   - Hassfest validation

2. **Test as a custom repository** in HACS:
   - Open HACS in Home Assistant
   - Click the three dots (⋮) → Custom repositories
   - Add your GitHub repository URL
   - Select category: Integration
   - Install and test it

3. **Create a GitHub Release**:
   - Tag your code with a version (e.g., `v1.0.0`)
   - Create a release on GitHub
   - Ensure GitHub Actions pass after the release

#### 3. Submit to HACS Default Repository

Once your repository is validated:

1. Fork the [hacs/default](https://github.com/hacs/default) repository
2. Add your repository URL to `integration` file (maintain alphabetical order):
   ```
   yourusername/ha-simple-curl
   ```
3. Create a pull request from your fork (not from an organization)
4. Fill out the pull request template completely
5. Wait for automated checks to pass
6. HACS team will review and merge if everything is correct

#### 4. Maintenance

After acceptance:

- Create GitHub releases for new versions (users can select from the 5 latest)
- Keep your repository active (not archived)
- Respond to issues and pull requests
- Update documentation as needed

### Required Files Checklist

This repository already includes all required files:

- ✅ `custom_components/simple_curl/` - Integration code
- ✅ `custom_components/simple_curl/manifest.json` - Integration metadata
- ✅ `custom_components/simple_curl/services.yaml` - Service definitions
- ✅ `hacs.json` - HACS configuration
- ✅ `info.md` - HACS integration description
- ✅ `README.md` - Documentation
- ✅ `.github/workflows/validate.yml` - Automated validation

### Additional Resources

- [HACS Publisher Documentation](https://www.hacs.xyz/docs/publish/)
- [HACS Integration Requirements](https://www.hacs.xyz/docs/publish/integration/)
- [HACS Default Repository](https://github.com/hacs/default)
- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [Integration Manifest Documentation](https://developers.home-assistant.io/docs/creating_integration_manifest/)

## License

This integration is provided as-is for Home Assistant 2026.* and later.
