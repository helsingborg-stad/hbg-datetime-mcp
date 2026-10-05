import logging

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from src.Settings import settings

mcp = MCPServer("HBG DateTime MCP")


@mcp.tool()
async def get_time_utc():
    """Get the current time in UTC as an ISO 8601 string.

    Returns:
        dict: A dictionary containing the current time in UTC as an ISO 8601 string, with the key "time".
    """
    return {"time": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
async def get_time_unix():
    """Get the current time as a Unix timestamp.

    Returns:
        dict: A dictionary containing the current time as a Unix timestamp, with the key "time".
    """
    return {"time": int(datetime.now(timezone.utc).timestamp())}


@mcp.tool()
async def get_time_by_zone(zone: str):
    """Get the current time in the specified time zone as an ISO 8601 string.

    Args:
        zone (str): The time zone to get the current time for. Must be a valid
            IANA time zone name (e.g., "America/New_York", "Europe/London", "Asia/Tokyo").

    Returns:
        dict: A dictionary containing the current time in the specified time zone as an ISO 8601 string, with the key "time".
    """
    return {"time": datetime.now(ZoneInfo(zone)).isoformat()}

if __name__ == "__main__":
    logger = logging.getLogger("hbg")
    logger.info(
        "Starting Datetime MCP on %s:%s with allowed hosts %s and allowed origins %s", settings.listen_host, settings.listen_port, settings.allowed_hosts, settings.allowed_origins)
    try:
        mcp.run(
            "streamable-http",
            stateless_http=True,
            host=settings.listen_host,
            port=settings.listen_port,
            transport_security=TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=settings.allowed_hosts.split(","),
                allowed_origins=settings.allowed_origins.split(","),
            )
        )
    except KeyboardInterrupt:
        logger.info("Stopped Datetime MCP")
