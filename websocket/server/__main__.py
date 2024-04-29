"""Script entry point to run the Matter Server."""

import argparse
import asyncio
from contextlib import suppress
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys
import threading
from typing import Final

from aiorun import run
import coloredlogs

from matter_server.common.const import VERBOSE_LOG_LEVEL
from matter_server.server import stack

from .server import MatterServer

DEFAULT_PORT = 5580
# Default to None to bind to all addresses on both IPv4 and IPv6
DEFAULT_LISTEN_ADDRESS = None
DEFAULT_STORAGE_PATH = os.path.join(Path.home(), ".matter_server")

FORMAT_DATE: Final = "%Y-%m-%d"
FORMAT_TIME: Final = "%H:%M:%S"
FORMAT_DATETIME: Final = f"{FORMAT_DATE} {FORMAT_TIME}"
MAX_LOG_FILESIZE = 1000000 * 10  # 10 MB

# Get parsed passed in arguments.
parser = argparse.ArgumentParser(
    description="Distribution addon server using WebSockets."
)


parser.add_argument(
    "--storage-path",
    type=str,
    default=DEFAULT_STORAGE_PATH,
    help=f"Storage path to keep persistent data, defaults to {DEFAULT_STORAGE_PATH}",
)
parser.add_argument(
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help=f"TCP Port to run the websocket server, defaults to {DEFAULT_PORT}",
)
parser.add_argument(
    "--listen-address",
    type=str,
    action="append",
    default=DEFAULT_LISTEN_ADDRESS,
    help="IP address to bind the websocket server to, defaults to any IPv4 and IPv6 address.",
)
parser.add_argument(
    "--log-level",
    type=str,
    default="info",
    help="Global logging level. Example --log-level debug, default=info, possible=(critical, error, warning, info, debug, verbose)",
)
parser.add_argument(
    "--log-file",
    type=str,
    default=None,
    help="Log file to write to (optional).",
)

args = parser.parse_args()


def _setup_logging() -> None:
    log_fmt = (
        "%(asctime)s.%(msecs)03d (%(threadName)s) %(levelname)s [%(name)s] %(message)s"
    )


def main() -> None:
    """Run main execution."""

    # make sure storage path exists
    if not os.path.isdir(args.storage_path):
        os.mkdir(args.storage_path)

    _setup_logging()

    # Init server
    server = MatterServer(
        args.storage_path,
        int(args.vendorid),
        int(args.fabricid),
        int(args.port),
        args.listen_address,
        args.primary_interface,
        args.paa_root_cert_dir,
    )

    async def handle_stop(loop: asyncio.AbstractEventLoop) -> None:
        # pylint: disable=unused-argument
        await server.stop()

    # run the server
    run(server.start(), shutdown_callback=handle_stop)


if __name__ == "__main__":
    main()
