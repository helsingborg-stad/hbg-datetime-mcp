import logging

from mcp.server import MCPServer
import uvicorn
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from src.Settings import settings
from src.logger.middleware import RequestLoggingMiddleware
from src.logger.setup import setup_logging
from src.logger.tool import log_tool_errors

setup_logging(
    log_dir=settings.log_dir,
    level=settings.log_level,
    max_bytes=settings.log_max_bytes,
    backup_count=settings.log_backup_count,
    console=settings.log_to_console,
)
logger = logging.getLogger("hbg.main")

mcp = MCPServer("HBG DateTime MCP")
app = RequestLoggingMiddleware(mcp.streamable_http_app())


@mcp.tool()
@log_tool_errors
async def get_time_utc():
    """Get the current time in UTC as an ISO 8601 string.

    Returns:
        dict: A dictionary containing the current time in UTC as an ISO 8601 string, with the key "time".
    """
    return {"time": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
@log_tool_errors
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
    logger.info(
        "Starting Datetime MCP on %s:%s", settings.listen_host, settings.listen_port)

    uvicorn.run(
        'main:app',
        host=settings.listen_host,
        port=settings.listen_port,
        reload=settings.development,
        # Keep the root logger config from setup_logging; the middleware above
        # is the single source of request logs.
        log_config=None,
        access_log=False,
    )
