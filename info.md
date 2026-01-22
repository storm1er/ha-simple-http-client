## Simple cURL for Home Assistant

A lightweight custom integration that provides a callable service to fetch URLs with custom HTTP methods and headers, returning the response as a variable for use in automations and scripts.

### Features

- No configuration required
- Fetch any URL with custom HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.)
- Set custom headers and request body
- Response data stored in variables using `response_variable`
- Returns status code, content, and response headers
- Built-in error handling

### Quick Example

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
          method: "GET"
          headers:
            Authorization: "Bearer token"
        response_variable: api_response

      - service: notify.notify
        data:
          message: "API returned: {{ api_response.content }}"
```

### Service: `simple_curl.fetch`

**Parameters:**
- `url` (required): The URL to fetch
- `method` (optional): HTTP method (default: GET)
- `headers` (optional): HTTP headers as key-value pairs
- `body` (optional): Request body content
- `timeout` (optional): Timeout in seconds (default: 10)

**Returns:**
- `status`: HTTP status code
- `content`: Response body as text
- `headers`: Response headers
- `error`: Error message (if failed)

For detailed documentation and more examples, see the [GitHub repository](https://github.com/storm1er/ha-simple-curl).
