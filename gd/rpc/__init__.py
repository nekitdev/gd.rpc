"""Geometry Dash Discord Rich Presence."""

__description__ = "Geometry Dash Discord Rich Presence."
__url__ = "https://github.com/nekitdev/gd.rpc"

__title__ = "rpc"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "1.0.1"

from gd.rpc.config import DEFAULT_CONFIG, Config, ConfigData, get_config, get_default_config
from gd.rpc.main import rpc

__all__ = (
    # config
    "DEFAULT_CONFIG",
    "Config",
    "ConfigData",
    "get_config",
    "get_default_config",
    # main
    "rpc",
)
