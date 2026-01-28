# Simple HTTP Client for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/storm1er/ha-simple-http-client.svg)](https://github.com/storm1er/ha-simple-http-client/releases)
[![License](https://img.shields.io/github/license/storm1er/ha-simple-http-client.svg)](LICENSE)

> **⚠️ IMPORTANT: Integration Renamed**
>
> This integration was previously called **"Simple cURL"** (domain: `simple_curl`). It has been renamed to **"Simple HTTP Client"** (domain: `simple_http_client`).
>
> **If you're upgrading from version v1.0.0:**
>
> **For HACS users:**
> 1. In `configuration.yaml`: remove `simple_curl:`
> 2. Restart Home Assistant to disable the old integration
> 3. In HACS → Integrations, find "Simple cURL" and remove it
> 4. Remove old repo repository: `https://github.com/storm1er/ha-simple-curl`
> 4. Add repository: `https://github.com/storm1er/ha-simple-http-client`
> 5. Download "Simple HTTP Client"
> 6. In `configuration.yaml`: add `simple_http_client:`
> 7. Restart Home Assistant
> 8. Update all service calls: `simple_curl.fetch` → `simple_http_client.fetch`
>
> **For manual installation users:**
> 1. Delete `custom_components/simple_curl/` folder
> 1. Download upgraded integration in `custom_components/simple_curl/` folder
> 2. In `configuration.yaml`: change `simple_curl:` to `simple_http_client:`
> 3. Update all service calls: `simple_curl.fetch` → `simple_http_client.fetch`
> 4. Restart Home Assistant

A lightweight Home Assistant integration that provides a simple service to fetch URLs with custom HTTP methods and headers. The response is returned as a variable that can be used directly in your automations and scripts.

## Why Use This?

Unlike the built-in `rest` integration which requires YAML configuration and creates sensors, Simple HTTP Client provides a **callable service** that:

- Works directly in automations and scripts without any configuration
- Returns data as variables using Home Assistant's `response_variable` feature
- Supports all HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.)
- Handles custom headers and request bodies
- Provides complete response data (status, content, headers)

Perfect for one-off API calls, webhooks, or dynamic URL fetching where you don't need persistent sensors.

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots (⋮) in the top right → **Custom repositories**
3. Add this repository URL: `https://github.com/storm1er/ha-simple-http-client`
4. Select category: **Integration**
5. Click **Add**
6. Find "Simple HTTP Client" in HACS and click **Download**
7. Add to your `configuration.yaml`:
   ```yaml
   simple_http_client:
   ```
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/storm1er/ha-simple-http-client/releases)
2. Extract and copy the `custom_components/simple_http_client` folder to your Home Assistant `custom_components` directory
3. Add to your `configuration.yaml`:
   ```yaml
   simple_http_client:
   ```
4. Restart Home Assistant

**Note:** This integration must be added to `configuration.yaml` to load. It does not appear in **Settings** → **Devices & Services**.

### Verify Installation

After restarting Home Assistant with `simple_http_client:` in your configuration.yaml:

1. Go to **Developer Tools** → **Services**
2. Search for `simple_http_client.fetch`
3. If the service appears, installation was successful!

Alternatively, check the logs at **Settings** → **System** → **Logs** for:
```
Simple HTTP Client integration loaded successfully
```

## Service: `simple_http_client.fetch`

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | Yes | - | The URL to fetch |
| `method` | No | `GET` | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) |
| `headers` | No | `{}` | HTTP headers as key-value pairs |
| `body` | No | - | Request body content (for POST, PUT, PATCH) |
| `timeout` | No | `10` | Request timeout in seconds |

### Response Data

The service returns a dictionary with the following fields:

- **`status`**: HTTP status code (integer)
- **`content`**: Response body as text (string)
- **`headers`**: Response headers (dictionary)
- **`error`**: Error message if request failed (string, only present on error)

Use the `response_variable` parameter to capture the response data in your automations.

## Usage Examples

### Basic GET Request

```yaml
automation:
  - alias: "Fetch API Data"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: simple_http_client.fetch
        data:
          url: "https://api.example.com/data"
        response_variable: api_response

      - service: notify.notify
        data:
          message: "API returned: {{ api_response.content }}"
```

### POST Request with Authentication

```yaml
script:
  post_to_api:
    sequence:
      - service: simple_http_client.fetch
        data:
          url: "https://api.example.com/endpoint"
          method: "POST"
          headers:
            Authorization: "Bearer {{ states('input_text.api_token') }}"
            Content-Type: "application/json"
          body: '{"temperature": {{ states("sensor.temperature") }}}'
        response_variable: result

      - service: persistent_notification.create
        data:
          title: "API Response"
          message: "Status: {{ result.status }}, Response: {{ result.content }}"
```

### Parsing JSON Response

```yaml
automation:
  - alias: "Fetch Weather Data"
    trigger:
      - platform: time_pattern
        hours: "/1"
    action:
      - service: simple_http_client.fetch
        data:
          url: "https://api.weather.example.com/current"
          headers:
            Accept: "application/json"
        response_variable: weather

      - variables:
          weather_data: "{{ weather.content | from_json }}"

      - service: input_text.set_value
        target:
          entity_id: input_text.current_temp
        data:
          value: "{{ weather_data.temperature }}"
```

### Conditional Actions Based on Response

```yaml
automation:
  - alias: "Check API Status"
    trigger:
      - platform: state
        entity_id: input_boolean.check_api
        to: "on"
    action:
      - service: simple_http_client.fetch
        data:
          url: "https://api.example.com/status"
          timeout: 5
        response_variable: api_status

      - if:
          - condition: template
            value_template: "{{ api_status.status == 200 }}"
        then:
          - service: light.turn_on
            target:
              entity_id: light.status_indicator
            data:
              rgb_color: [0, 255, 0]
        else:
          - service: light.turn_on
            target:
              entity_id: light.status_indicator
            data:
              rgb_color: [255, 0, 0]
```

### Error Handling

```yaml
automation:
  - alias: "Fetch with Error Handling"
    trigger:
      - platform: time_pattern
        minutes: "/15"
    action:
      - service: simple_http_client.fetch
        data:
          url: "https://api.example.com/data"
          timeout: 10
        response_variable: response

      - if:
          - condition: template
            value_template: "{{ 'error' in response }}"
        then:
          - service: persistent_notification.create
            data:
              title: "API Error"
              message: "Failed to fetch data: {{ response.error }}"
        else:
          - service: logbook.log
            data:
              name: "API Success"
              message: "Fetched successfully with status {{ response.status }}"
```

### Dynamic URL with Template

```yaml
script:
  fetch_device_status:
    sequence:
      - service: simple_http_client.fetch
        data:
          url: "http://{{ states('input_text.device_ip') }}/api/status"
          headers:
            X-API-Key: "{{ states('input_text.device_api_key') }}"
        response_variable: device_data

      - service: notify.notify
        data:
          message: "Device status: {{ device_data.content }}"
```

## Important Notes

- **Response Content Format**: The response `content` is always returned as text. For JSON APIs, use the `from_json` filter to parse it.
- **Error Handling**: Network errors, timeouts, and connection failures are caught and returned in the `error` field instead of raising exceptions.
- **Status Code `0`**: Indicates a network or connection error (not a valid HTTP response).
- **Timeout**: Default is 10 seconds. Adjust based on your API's expected response time.
- **Security**: Be careful not to log sensitive data like API keys or tokens. Use secrets for sensitive information.

## Troubleshooting

### Service not found

If the `simple_http_client.fetch` service doesn't appear after restart:

1. **Verify `configuration.yaml`**: Make sure you added `simple_http_client:` to your configuration.yaml file
2. **Check YAML syntax**: Run **Developer Tools** → **YAML** → **Check Configuration** to ensure no YAML errors
3. **Verify installation**: Confirm the integration is in `custom_components/simple_http_client/`
4. **Check logs**: Go to **Settings** → **System** → **Logs** and search for "simple_http_client" errors
5. **Restart again**: Sometimes a second restart is needed

Common issues:
- **Forgot to add to configuration.yaml** - This is the most common issue! The integration won't load without it.
- **YAML indentation error** - Make sure `simple_http_client:` is at the root level (no indentation)
- **Typo in domain name** - Must be exactly `simple_http_client:` (with underscore, not dash)

### Request fails with error

- Check the URL is accessible from your Home Assistant instance
- Verify headers and authentication are correct
- Increase the `timeout` if the API is slow to respond
- Check Home Assistant logs for detailed error messages

### Response is empty

- Some APIs return empty bodies for certain status codes (204, 304, etc.)
- Check `response.status` to understand what the server returned
- Verify the API endpoint is correct

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting pull requests, reporting issues, or publishing this integration to HACS.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you find this integration useful, consider:
- Starring the repository on GitHub
- Reporting issues or suggesting features via [GitHub Issues](https://github.com/storm1er/ha-simple-http-client/issues)
- Contributing improvements via pull requests

## Credits

Built for Home Assistant 2026.* and later, using the modern `response_variable` service pattern.
