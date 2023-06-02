from asyncio import set_event_loop
from time import time
from typing import Optional

from gd.asyncio import shutdown_loop
from gd.enums import Difficulty
from gd.level import Level
from gd.memory.state import get_state
from gd.string_utils import case_fold
from gd.tasks import loop
from toml import TomlDecodeError as TOMLDecodeError
from pypresence import AioPresence as AsyncPresence  # type: ignore  # no stubs or types

from gd.rpc.config import PATH, get_config

__all__ = ("rpc",)

ICON = "icon"  # do not change

DEFAULT = "default"
DEFAULT_NAME = "unknown"

DEFAULT_FEATURED = False
DEFAULT_EPIC = False

FEATURED = "featured"
EPIC = "epic"

DASH = "-"
UNDER = "_"


def get_timestamp() -> int:
    """Returns the time in seconds since the epoch as an integer.

    Returns:
        The time in seconds since the epoch.
    """
    return int(time())


config = get_config()

process_name = config.process_name

if process_name == DEFAULT:
    memory_state = get_state()

else:
    memory_state = get_state(process_name)

start = get_timestamp()

presence = AsyncPresence(str(config.client_id))


def get_image_name(
    difficulty: Difficulty,
    featured: bool = DEFAULT_FEATURED,
    epic: bool = DEFAULT_EPIC,
) -> str:
    """Computes an image name based on `difficulty` and `featured` / `epic`.

    Arguments:
        difficulty: The related level difficulty to look up.
        featured: Whether the related level is featured.
        epic: Whether the related level is epic.

    Returns:
        The name of the image to use.
    """
    parts = case_fold(difficulty.name).split(UNDER)

    if epic:
        parts.append(EPIC)

    elif featured:
        parts.append(FEATURED)

    return DASH.join(parts)


@loop(seconds=config.refresh_seconds)
async def update_loop() -> None:
    # declare variables as global since we edit them
    global config
    global start

    try:
        memory_state.reload()  # attempt to reload the state

    except LookupError:  # can not find the process
        start = get_timestamp()  # restart the time

        await presence.clear()  # clear presence state

        return

    try:
        config = get_config()  # try to load the config

    except TOMLDecodeError:  # if config is invalid
        pass  # do nothing, keeping the old config

    # annotations for mypy
    details: Optional[str]
    state: Optional[str]

    account_manager_pointer = memory_state.account_manager

    if account_manager_pointer.is_null():
        name = DEFAULT_NAME

    else:
        account_manager = account_manager_pointer.value

        name = account_manager.name  # get the name

        if not name:  # set default if not found
            name = DEFAULT_NAME

    game_manager_pointer = memory_state.game_manager

    if game_manager_pointer.is_null():
        return

    game_manager = game_manager_pointer.value

    editor_layer_pointer = game_manager.editor_layer
    play_layer_pointer = game_manager.play_layer

    if play_layer_pointer.is_null():  # if not playing any levels
        if editor_layer_pointer.is_null():
            scene = game_manager.scene

            details = config.scene.get(scene)
            state = None

        else:
            editor_layer = editor_layer_pointer.value

            level_settings = editor_layer.level_settings.value
            level = level_settings.level.value

            format_map = dict(
                object_count=editor_layer.object_count,
                level_name=level.name,
                name=name,
            )

            details = config.editor.details.format_map(format_map)
            state = config.editor.state.format_map(format_map)

        small_image = None
        small_text = None

    else:  # if playing some level
        play_layer = play_layer_pointer.value

        progress = round(play_layer.progress, config.level.progress_precision)

        attempt = play_layer.attempt

        level_settings = play_layer.level_settings.value

        level = level_settings.level.value

        normal_record = level.normal_record
        practice_record = level.practice_record

        mode = config.mode.practice if play_layer.is_practice() else config.mode.normal

        level_id = level.level_id
        level_name = level.name
        level_creator_name = level.creator_name
        level_difficulty = level.difficulty
        level_attempts = level.attempts
        level_stars = level.stars
        level_type = level.type

        featured = level.is_featured()
        epic = level.is_epic()

        if level_type.is_official():
            level_model = Level.official(level_id)

            level_difficulty = level_model.difficulty
            level_creator_name = level_model.creator.name
            featured = level_model.is_featured()
            epic = level_model.is_epic()

        if level_type.is_editor():
            level_difficulty = Difficulty.UNKNOWN
            level_creator_name = name

        format_map = dict(
            name=name,
            progress=progress,
            attempt=attempt,
            mode=mode,
            level_normal_record=normal_record,
            level_practice_record=practice_record,
            level_type=config.level_type.get(level_type),
            level_id=level_id,
            level_name=level_name,
            level_creator_name=level_creator_name,
            level_difficulty=config.difficulty.get(level_difficulty),
            level_attempts=level_attempts,
            level_stars=level_stars,
        )

        details = config.level.details.format_map(format_map)
        state = config.level.state.format_map(format_map)

        small_image = get_image_name(level_difficulty, featured, epic)
        small_text = config.level.small.format_map(format_map)

    await presence.update(
        pid=memory_state.process_id,
        state=state,
        details=details,
        start=start,
        large_image=ICON,
        large_text=name,
        small_image=small_image,
        small_text=small_text,
    )


CONFIG = "config: {}"
CONNECTING = "connecting..."
EXIT = "press [ctrl + c] or close the console to exit..."


def rpc() -> None:
    print(CONFIG.format(PATH.as_posix()))
    print(CONNECTING)

    loop = presence.loop

    set_event_loop(loop)

    loop.run_until_complete(presence.connect())

    print(EXIT)

    update_loop.start()

    try:
        presence.loop.run_forever()

    except KeyboardInterrupt:
        presence.close()
        shutdown_loop(loop)
