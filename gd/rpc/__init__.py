"""Geometry Dash Discord Rich Presence."""

__description__ = "Geometry Dash Discord Rich Presence."
__url__ = "https://github.com/nekitdev/gd.rpc"

__title__ = "rpc"
__author__ = "nekitdev"
__license__ = "MIT"
__version__ = "1.0.0"

from gd.rpc.config import CONFIG_NAME, DEFAULT_CONFIG, GD_NAME, NAME, Config, ConfigData, get_config
from gd.rpc.main import rpc

__all__ = (
    "DEFAULT_CONFIG", "CONFIG_NAME", "GD_NAME", "NAME", "Config", "ConfigData", "get_config", "rpc"
)
