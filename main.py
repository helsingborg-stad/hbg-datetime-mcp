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
async def iso_to_unix(iso_time: str):
    """Convert an ISO 8601 time string to a Unix timestamp.

    Args:
        iso_time (str): The ISO 8601 time string to convert.

    Returns:
        dict: A dictionary containing the Unix timestamp corresponding to the given ISO 8601 time string, with the key "time".
    """
    dt = datetime.fromisoformat(iso_time)
    return {"time": int(dt.timestamp())}


@mcp.tool()
async def unix_to_iso(unix_time: int):
    """Convert a Unix timestamp to an ISO 8601 time string.

    Args:
        unix_time (int): The Unix timestamp to convert.

    Returns:
        dict: A dictionary containing the ISO 8601 time string corresponding to the given Unix timestamp, with the key "time".
    """
    dt = datetime.fromtimestamp(unix_time, timezone.utc)
    return {"time": dt.isoformat()}


@mcp.tool()
async def get_weekday_name(iso_time: str):
    """Get the name of the weekday for a given ISO 8601 time string.

    Args:
        iso_time (str): The ISO 8601 time string to get the weekday for.

    Returns:
        dict: A dictionary containing the name of the weekday corresponding to the given ISO 8601 time string, with the key "weekday".
    """
    dt = datetime.fromisoformat(iso_time)
    return {"weekday": dt.strftime("%A")}


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
