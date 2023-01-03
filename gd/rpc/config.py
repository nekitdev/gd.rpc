from builtins import getattr as get_attribute
from pathlib import Path
from typing import Any, Optional, Type, TypeVar, cast

import toml
from attrs import define
from wraps import Option, wrap_optional

from gd.constants import DEFAULT_ENCODING, DEFAULT_ERRORS
from gd.enums import Difficulty, LevelType, Scene
from gd.string_utils import case_fold, tick
from gd.typing import IntoPath, StringDict

__all__ = ("DEFAULT_CONFIG", "CONFIG_NAME", "GD_NAME", "NAME", "Config", "ConfigData", "get_config")

HOME = Path.home()

CONFIG_NAME = ".config"
GD_NAME = "gd"

NAME = "rpc.toml"

DEFAULT_PATH = Path(__file__).parent / NAME
PATH = HOME / CONFIG_NAME / GD_NAME / NAME


T = TypeVar("T")


class ConfigData(StringDict[T]):
    """Extension of [`StringDict[T]`][gd.typing.StringDict] that
    allows accessing values as attributes.
    """

    def __getattr__(self, name: str) -> Option[T]:
        return wrap_optional(self.get(name))


AnyConfigData = ConfigData[Any]


@define()
class EditorConfig:
    """Represents the configuration of the RPC for when the user is in the editor."""

    details: str
    """The `details` of the RPC."""
    state: str
    """The `state` of the RPC."""


@define()
class LevelConfig:
    """Represents the configuration of the RPC for when the user is playing some level."""

    details: str
    """The `details` of the RPC."""
    state: str
    """The `state` of the RPC."""

    small: str
    """The `small` of the RPC."""

    progress_precision: int
    """The record precision to use."""


@define()
class SceneConfig:
    """The configuration to use for specific scenes, excluding the editor and level ones."""

    main: str
    """The name of the *main* scene."""
    select: str
    """The name of the *selection* scene."""
    editor_or_level: str
    """The name of the *editor or level* scene (depends on the context)."""
    search: str
    """The name of the *search* scene."""
    leaderboard: str
    """The name of the *leaderboard* scene"""
    online: str
    """The name of the *online* scene."""
    official_select: str
    """The name of the *official selection* scene."""
    official_level: str
    """The name of the *official level* scene."""

    def get(self, scene: Scene) -> Optional[str]:
        return get_attribute(self, case_fold(scene.name), None)


@define()
class DifficultyConfig:
    """The configuration to use for difficulty display."""

    unknown: str
    """The name of the *unknown* difficulty."""
    auto: str
    """The name of the *auto* difficulty."""
    easy: str
    """The name of the *easy* difficulty."""
    normal: str
    """The name of the *normal* difficulty."""
    hard: str
    """The name of the *hard* difficulty."""
    harder: str
    """The name of the *harder* difficulty."""
    insane: str
    """The name of the *insane* difficulty."""
    demon: str
    """The name of the *unspecified demon* difficulty."""

    easy_demon: str
    """The name of the *easy demon* difficulty."""
    medium_demon: str
    """The name of the *medium demon* difficulty."""
    hard_demon: str
    """The name of the *hard demon* difficulty."""
    insane_demon: str
    """The name of the *insane demon* difficulty."""
    extreme_demon: str
    """The name of the *extreme demon* difficulty."""

    def get(self, difficulty: Difficulty) -> Optional[str]:
        return get_attribute(self, case_fold(difficulty.name), None)


@define()
class LevelTypeConfig:
    null: str
    """The name of the *null* (unknown) level type."""
    official: str
    """The name of the *official* level type."""
    editor: str
    """The name of the *editor* level type."""
    saved: str
    """The name of the *saved* level type."""
    online: str
    """The name of the *online* level type."""

    def get(self, level_type: LevelType) -> Optional[str]:
        return get_attribute(self, case_fold(level_type.name), None)


@define()
class ModeConfig:
    """The configuration to use for level play mode display."""

    normal: str
    """The name of the *normal* mode."""
    practice: str
    """The name of the *practice* mode."""


EXPECTED = "expected {}"


def expected(name: str) -> str:
    return EXPECTED.format(tick(name))


EXPECTED_RPC = expected("rpc")
EXPECTED_RPC_PROCESS_NAME = expected("rpc.process_name")
EXPECTED_RPC_REFRESH_SECONDS = expected("rpc.refresh_seconds")
EXPECTED_RPC_CLIENT_ID = expected("rpc.client_id")
EXPECTED_RPC_EDITOR = expected("rpc.editor")
EXPECTED_RPC_EDITOR_DETAILS = expected("rpc.editor.details")
EXPECTED_RPC_EDITOR_STATE = expected("rpc.editor.state")
EXPECTED_RPC_LEVEL = expected("rpc.level")
EXPECTED_RPC_LEVEL_DETAILS = expected("rpc.level.details")
EXPECTED_RPC_LEVEL_STATE = expected("rpc.level.state")
EXPECTED_RPC_LEVEL_SMALL = expected("rpc.level.small")
EXPECTED_RPC_LEVEL_PROGRESS_PRECISION = expected("rpc.level.progress_precision")
EXPECTED_RPC_SCENE = expected("rpc.scene")
EXPECTED_RPC_SCENE_MAIN = expected("rpc.scene.main")
EXPECTED_RPC_SCENE_SELECT = expected("rpc.scene.select")
EXPECTED_RPC_SCENE_EDITOR_OR_LEVEL = expected("rpc.scene.editor_or_level")
EXPECTED_RPC_SCENE_SEARCH = expected("rpc.scene.search")
EXPECTED_RPC_SCENE_LEADERBOARD = expected("rpc.scene.leaderboard")
EXPECTED_RPC_SCENE_ONLINE = expected("rpc.scene.online")
EXPECTED_RPC_SCENE_OFFICIAL_SELECT = expected("rpc.scene.official_select")
EXPECTED_RPC_SCENE_OFFICIAL_LEVEL = expected("rpc.scene.official_level")
EXPECTED_RPC_DIFFICULTY = expected("rpc.difficulty")
EXPECTED_RPC_DIFFICULTY_UNKNOWN = expected("rpc.difficulty.unknown")
EXPECTED_RPC_DIFFICULTY_AUTO = expected("rpc.difficulty.auto")
EXPECTED_RPC_DIFFICULTY_EASY = expected("rpc.difficulty.easy")
EXPECTED_RPC_DIFFICULTY_NORMAL = expected("rpc.difficulty.normal")
EXPECTED_RPC_DIFFICULTY_HARD = expected("rpc.difficulty.hard")
EXPECTED_RPC_DIFFICULTY_HARDER = expected("rpc.difficulty.harder")
EXPECTED_RPC_DIFFICULTY_INSANE = expected("rpc.difficulty.insane")
EXPECTED_RPC_DIFFICULTY_DEMON = expected("rpc.difficulty.demon")
EXPECTED_RPC_DIFFICULTY_EASY_DEMON = expected("rpc.difficulty.easy_demon")
EXPECTED_RPC_DIFFICULTY_MEDIUM_DEMON = expected("rpc.difficulty.medium_demon")
EXPECTED_RPC_DIFFICULTY_HARD_DEMON = expected("rpc.difficulty.hard_demon")
EXPECTED_RPC_DIFFICULTY_INSANE_DEMON = expected("rpc.difficulty.insane_demon")
EXPECTED_RPC_DIFFICULTY_EXTREME_DEMON = expected("rpc.difficulty.extreme_demon")
EXPECTED_RPC_LEVEL_TYPE = expected("rpc.level_type")
EXPECTED_RPC_LEVEL_TYPE_NULL = expected("rpc.level_type.null")
EXPECTED_RPC_LEVEL_TYPE_OFFICIAL = expected("rpc.level_type.official")
EXPECTED_RPC_LEVEL_TYPE_EDITOR = expected("rpc.level_type.editor")
EXPECTED_RPC_LEVEL_TYPE_SAVED = expected("rpc.level_type.saved")
EXPECTED_RPC_LEVEL_TYPE_ONLINE = expected("rpc.level_type.online")
EXPECTED_RPC_MODE = expected("rpc.mode")
EXPECTED_RPC_MODE_NORMAL = expected("rpc.mode.normal")
EXPECTED_RPC_MODE_PRACTICE = expected("rpc.mode.practice")


C = TypeVar("C", bound="Config")


@define()
class Config:
    """Represents the configuration of the RPC."""

    process_name: str
    """The process name of the game."""
    refresh_seconds: int
    """The seconds to wait before refreshing the RPC."""
    client_id: int
    """The client ID of the Discord application."""

    editor: EditorConfig
    """The configuration of the RPC for when the user is in the editor."""

    level: LevelConfig
    """The configuration of the RPC for when the user is playing some level."""

    scene: SceneConfig
    """The configuration to use for specific scenes, excluding the editor and level ones."""

    difficulty: DifficultyConfig
    """The configuration to use for difficulty display."""

    level_type: LevelTypeConfig
    """The configuration to use for level type display."""

    mode: ModeConfig
    """The configuration to use for level play mode display."""

    # dynamic code ahead...

    @classmethod
    def from_string(cls: Type[C], string: str) -> C:
        """Parses a [`Config`][gd.rpc.config.Config] from `string`.

        Arguments:
            string: The string to parse.

        Returns:
            The newly parsed [`Config`][gd.rpc.config.Config].
        """
        return cls.from_data(cls.parse(string))

    @classmethod
    def from_path(
        cls: Type[C], path: IntoPath, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
    ) -> C:
        """Parses a [`Config`][gd.rpc.config.Config] from file `path`.

        Arguments:
            path: The path to the config.

        Returns:
            The newly parsed [`Config`][gd.rpc.config.Config] instance.
        """
        return cls.from_string(Path(path).read_text(encoding, errors))

    @staticmethod
    def parse(string: str) -> AnyConfigData:
        return cast(AnyConfigData, toml.loads(string, AnyConfigData))

    @classmethod
    def from_data(cls: Type[C], config_data: AnyConfigData) -> C:
        """Creates a [`Config`][gd.rpc.config.Config]
        from [`ConfigData`][gd.rpc.config.ConfigData].

        Arguments:
            config_data: The configuration data to use.

        Returns:
            The newly created [`Config`][gd.rpc.config.Config] instance.
        """
        default_config = DEFAULT_CONFIG

        rpc_data = config_data.rpc.unwrap_or_else(AnyConfigData)

        process_name = rpc_data.process_name.unwrap_or(default_config.process_name)
        refresh_seconds = rpc_data.refresh_seconds.unwrap_or(default_config.refresh_seconds)
        client_id = rpc_data.client_id.unwrap_or(default_config.client_id)

        editor_data = rpc_data.editor.unwrap_or_else(AnyConfigData)
        editor_config = default_config.editor

        editor = EditorConfig(
            details=editor_data.details.unwrap_or(editor_config.details),
            state=editor_data.state.unwrap_or(editor_config.state),
        )

        level_data = rpc_data.level.unwrap_or_else(AnyConfigData)
        level_config = default_config.level

        level = LevelConfig(
            details=level_data.details.unwrap_or(level_config.details),
            state=level_data.state.unwrap_or(level_config.state),
            small=level_data.small.unwrap_or(level_config.small),
            progress_precision=level_data.progress_precision.unwrap_or(level_config.progress_precision),
        )

        scene_data = rpc_data.scene.unwrap_or_else(AnyConfigData)
        scene_config = default_config.scene

        scene = SceneConfig(
            main=scene_data.main.unwrap_or(scene_config.main),
            select=scene_data.select.unwrap_or(scene_config.select),
            editor_or_level=scene_data.editor_or_level.unwrap_or(scene_config.editor_or_level),
            search=scene_data.search.unwrap_or(scene_config.search),
            leaderboard=scene_data.leaderboard.unwrap_or(scene_config.leaderboard),
            online=scene_data.online.unwrap_or(scene_config.online),
            official_select=scene_data.official_select.unwrap_or(scene_config.official_select),
            official_level=scene_data.official_level.unwrap_or(scene_config.official_level),
        )

        difficulty_data = rpc_data.difficulty.unwrap_or_else(AnyConfigData)
        difficulty_config = default_config.difficulty

        difficulty = DifficultyConfig(
            unknown=difficulty_data.unknown.unwrap_or(difficulty_config.unknown),
            auto=difficulty_data.auto.unwrap_or(difficulty_config.auto),
            easy=difficulty_data.easy.unwrap_or(difficulty_config.easy),
            normal=difficulty_data.normal.unwrap_or(difficulty_config.normal),
            hard=difficulty_data.hard.unwrap_or(difficulty_config.hard),
            harder=difficulty_data.harder.unwrap_or(difficulty_config.harder),
            insane=difficulty_data.insane.unwrap_or(difficulty_config.insane),
            demon=difficulty_data.demon.unwrap_or(difficulty_config.demon),
            easy_demon=difficulty_data.easy_demon.unwrap_or(difficulty_config.easy_demon),
            medium_demon=difficulty_data.medium_demon.unwrap_or(difficulty_config.medium_demon),
            hard_demon=difficulty_data.hard_demon.unwrap_or(difficulty_config.hard_demon),
            insane_demon=difficulty_data.insane_demon.unwrap_or(difficulty_config.insane_demon),
            extreme_demon=difficulty_data.extreme_demon.unwrap_or(difficulty_config.extreme_demon),
        )
            
        level_type_data = rpc_data.level_type.unwrap_or_else(AnyConfigData)
        level_type_config = default_config.level_type

        level_type = LevelTypeConfig(
            null=level_type_data.null.unwrap_or(level_type_config.null),
            official=level_type_data.official.unwrap_or(level_type_config.official),
            editor=level_type_data.editor.unwrap_or(level_type_config.editor),
            saved=level_type_data.saved.unwrap_or(level_type_config.saved),
            online=level_type_data.online.unwrap_or(level_type_config.online),
        )

        mode_data = rpc_data.mode.unwrap_or_else(AnyConfigData)
        mode_config = default_config.mode

        mode = ModeConfig(
            normal=mode_data.normal.unwrap_or(mode_config.normal),
            practice=mode_data.practice.unwrap_or(mode_config.practice),
        )

        return cls(
            process_name=process_name,
            refresh_seconds=refresh_seconds,
            client_id=client_id,
            editor=editor,
            level=level,
            scene=scene,
            difficulty=difficulty,
            level_type=level_type,
            mode=mode,
        )

    @classmethod
    def unsafe_from_string(cls: Type[C], string: str) -> C:
        return cls.unsafe_from_data(cls.parse(string))

    @classmethod
    def unsafe_from_path(
        cls: Type[C], path: IntoPath, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
    ) -> C:
        return cls.unsafe_from_string(Path(path).read_text(encoding, errors))

    @classmethod
    def unsafe_from_data(cls: Type[C], config_data: AnyConfigData) -> C:
        rpc_data = config_data.rpc.expect(EXPECTED_RPC)

        process_name = rpc_data.process_name.expect(EXPECTED_RPC_PROCESS_NAME)
        refresh_seconds = rpc_data.refresh_seconds.expect(EXPECTED_RPC_REFRESH_SECONDS)
        client_id = rpc_data.client_id.expect(EXPECTED_RPC_CLIENT_ID)

        editor_data = rpc_data.editor.expect(EXPECTED_RPC_EDITOR)

        editor = EditorConfig(
            details=editor_data.details.expect(EXPECTED_RPC_EDITOR_DETAILS),
            state=editor_data.state.expect(EXPECTED_RPC_EDITOR_STATE),
        )

        level_data = rpc_data.level.expect(EXPECTED_RPC_LEVEL)

        level = LevelConfig(
            details=level_data.details.expect(EXPECTED_RPC_LEVEL_DETAILS),
            state=level_data.state.expect(EXPECTED_RPC_LEVEL_STATE),
            small=level_data.small.expect(EXPECTED_RPC_LEVEL_SMALL),
            progress_precision=level_data.progress_precision.expect(
                EXPECTED_RPC_LEVEL_PROGRESS_PRECISION
            ),
        )

        scene_data = rpc_data.scene.expect(EXPECTED_RPC_SCENE)

        scene = SceneConfig(
            main=scene_data.main.expect(EXPECTED_RPC_SCENE_MAIN),
            select=scene_data.select.expect(EXPECTED_RPC_SCENE_SELECT),
            editor_or_level=scene_data.editor_or_level.expect(EXPECTED_RPC_SCENE_EDITOR_OR_LEVEL),
            search=scene_data.search.expect(EXPECTED_RPC_SCENE_SEARCH),
            leaderboard=scene_data.leaderboard.expect(EXPECTED_RPC_SCENE_LEADERBOARD),
            online=scene_data.online.expect(EXPECTED_RPC_SCENE_ONLINE),
            official_select=scene_data.official_select.expect(EXPECTED_RPC_SCENE_OFFICIAL_SELECT),
            official_level=scene_data.official_level.expect(EXPECTED_RPC_SCENE_OFFICIAL_LEVEL),
        )

        difficulty_data = rpc_data.difficulty.expect(EXPECTED_RPC_DIFFICULTY)

        difficulty = DifficultyConfig(
            unknown=difficulty_data.unknown.expect(EXPECTED_RPC_DIFFICULTY_UNKNOWN),
            auto=difficulty_data.auto.expect(EXPECTED_RPC_DIFFICULTY_AUTO),
            easy=difficulty_data.easy.expect(EXPECTED_RPC_DIFFICULTY_EASY),
            normal=difficulty_data.normal.expect(EXPECTED_RPC_DIFFICULTY_NORMAL),
            hard=difficulty_data.hard.expect(EXPECTED_RPC_DIFFICULTY_HARD),
            harder=difficulty_data.harder.expect(EXPECTED_RPC_DIFFICULTY_HARDER),
            insane=difficulty_data.insane.expect(EXPECTED_RPC_DIFFICULTY_INSANE),
            demon=difficulty_data.demon.expect(EXPECTED_RPC_DIFFICULTY_DEMON),
            easy_demon=difficulty_data.easy_demon.expect(EXPECTED_RPC_DIFFICULTY_EASY_DEMON),
            medium_demon=difficulty_data.medium_demon.expect(EXPECTED_RPC_DIFFICULTY_MEDIUM_DEMON),
            hard_demon=difficulty_data.hard_demon.expect(EXPECTED_RPC_DIFFICULTY_HARD_DEMON),
            insane_demon=difficulty_data.insane_demon.expect(EXPECTED_RPC_DIFFICULTY_INSANE_DEMON),
            extreme_demon=difficulty_data.extreme_demon.expect(EXPECTED_RPC_DIFFICULTY_EXTREME_DEMON),
        )

        level_type_data = rpc_data.level_type.expect(EXPECTED_RPC_LEVEL_TYPE)

        level_type = LevelTypeConfig(
            null=level_type_data.null.expect(EXPECTED_RPC_LEVEL_TYPE_NULL),
            official=level_type_data.official.expect(EXPECTED_RPC_LEVEL_TYPE_OFFICIAL),
            editor=level_type_data.editor.expect(EXPECTED_RPC_LEVEL_TYPE_EDITOR),
            saved=level_type_data.saved.expect(EXPECTED_RPC_LEVEL_TYPE_SAVED),
            online=level_type_data.online.expect(EXPECTED_RPC_LEVEL_TYPE_ONLINE),
        )

        mode_data = rpc_data.mode.expect(EXPECTED_RPC_MODE)

        mode = ModeConfig(
            normal=mode_data.normal.expect(EXPECTED_RPC_MODE_NORMAL),
            practice=mode_data.practice.expect(EXPECTED_RPC_MODE_PRACTICE),
        )

        return cls(
            process_name=process_name,
            refresh_seconds=refresh_seconds,
            client_id=client_id,
            editor=editor,
            level=level,
            scene=scene,
            difficulty=difficulty,
            level_type=level_type,
            mode=mode,
        )


DEFAULT_CONFIG = Config.unsafe_from_path(DEFAULT_PATH)


def ensure_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> None:
    if not PATH.exists():
        PATH.parent.mkdir(parents=True, exist_ok=True)

        PATH.write_text(DEFAULT_PATH.read_text(encoding, errors), encoding, errors)


ensure_config()


def get_config(encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS) -> Config:
    return Config.from_path(PATH)
