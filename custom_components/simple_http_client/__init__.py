"""Simple HTTP Client integration for Home Assistant."""
import logging
import aiohttp
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "simple_http_client"

# This integration has no configuration parameters
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

# Service schema
SERVICE_FETCH_SCHEMA = vol.Schema({
    vol.Required("url"): cv.url,
    vol.Optional("method", default="GET"): vol.In(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]),
    vol.Optional("headers"): vol.Schema({cv.string: cv.string}),
    vol.Optional("body"): cv.string,
    vol.Optional("timeout", default=10): cv.positive_int,
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Simple HTTP Client component."""

    async def async_handle_fetch(call: ServiceCall) -> ServiceResponse:
        """Handle the fetch service call."""
        url = call.data["url"]
        method = call.data.get("method", "GET")
        headers = call.data.get("headers", {})
        body = call.data.get("body")
        timeout = call.data.get("timeout", 10)

        _LOGGER.debug(
            "Fetching URL: %s with method: %s, headers: %s",
            url,
            method,
            headers,
        )

        session = async_get_clientsession(hass)

        try:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                data=body,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as response:
                status = response.status
                content = await response.text()
                response_headers = dict(response.headers)

                _LOGGER.debug(
                    "Response status: %s, content length: %s",
                    status,
                    len(content),
                )

                # Return the response data to be captured in a variable
                return {
                    "status": status,
                    "content": content,
                    "headers": response_headers,
                }

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching %s: %s", url, err)
            return {
                "status": 0,
                "content": "",
                "error": str(err),
            }
        except Exception as err:
            _LOGGER.error("Unexpected error fetching %s: %s", url, err)
            return {
                "status": 0,
                "content": "",
                "error": str(err),
            }

    # Register the service with response support
    # SupportsResponse.ONLY means this service ALWAYS returns data
    hass.services.async_register(
        DOMAIN,
        "fetch",
        async_handle_fetch,
        schema=SERVICE_FETCH_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )

    _LOGGER.info("Simple HTTP Client integration loaded successfully")

    return True
