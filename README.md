# `gd.rpc`

![Image]

[![License][License Badge]][License]
[![Version][Version Badge]][Package]
[![Downloads][Downloads Badge]][Package]
[![Discord][Discord Badge]][Discord]

[![Documentation][Documentation Badge]][Documentation]
[![Check][Check Badge]][Actions]

> *Geometry Dash Discord Rich Presence.*

## Installing

**Python 3.7 or above is required.**

### pip

Installing the library with `pip` is quite simple:

```console
$ pip install gd.rpc
```

Alternatively, the library can be installed from source:

```console
$ git clone https://github.com/nekitdev/gd.rpc.git
$ cd gd.rpc
$ python -m pip install .
```

### poetry

You can add `gd.rpc` as a dependency with the following command:

```console
$ poetry add gd.rpc
```

Or by directly specifying it in the configuration like so:

```toml
[tool.poetry.dependencies]
"gd.rpc" = "^1.0.0"
```

Alternatively, you can add it directly from the source:

```toml
[tool.poetry.dependencies."gd.rpc"]
git = "https://github.com/nekitdev/gd.rpc.git"
```

## Usage

Using `gd.rpc` is as simple as:

```console
$ python -m gd.rpc
config: ~/.config/gd/rpc.toml
connecting...
press [ctrl + c] or close the console to exit...
```

## Compiling

Compiling an executable version of the `gd.rpc` library:

```console
$ pyinstaller --onefile --icon assets/gd.rpc.ico --exclude numpy --exclude PIL --exclude IPython --exclude Crypto --exclude lxml --add-data gd/rpc;gd/rpc gd.rpc.py
```

## Showcase

The showcase can be found [here][Showcase].

## Documentation

You can find the documentation [here][Documentation].

## Support

If you need support with the library, you can send an [email][Email]
or refer to the official [Discord server][Discord].

## Changelog

You can find the changelog [here][Changelog].

## Security Policy

You can find the Security Policy of `gd.rpc` [here][Security].

## Contributing

If you are interested in contributing to `gd.rpc`, make sure to take a look at the
[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].

## License

`gd.rpc` is licensed under the MIT License terms. See [License][License] for details.

[Image]: https://github.com/nekitdev/gd.rpc/blob/main/assets/gd.rpc.svg?raw=true

[Email]: mailto:support@nekit.dev

[Discord]: https://nekit.dev/discord

[Actions]: https://github.com/nekitdev/gd.rpc/actions

[Showcase]: https://youtube.com/watch?v=-L3SW8MbduQ

[Changelog]: https://github.com/nekitdev/gd.rpc/blob/main/CHANGELOG.md
[Code of Conduct]: https://github.com/nekitdev/gd.rpc/blob/main/CODE_OF_CONDUCT.md
[Contributing Guide]: https://github.com/nekitdev/gd.rpc/blob/main/CONTRIBUTING.md
[Security]: https://github.com/nekitdev/gd.rpc/blob/main/SECURITY.md

[License]: https://github.com/nekitdev/gd.rpc/blob/main/LICENSE

[Package]: https://pypi.org/project/gd.rpc
[Documentation]: https://nekitdev.github.io/gd.rpc

[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2
[License Badge]: https://img.shields.io/pypi/l/gd.rpc
[Version Badge]: https://img.shields.io/pypi/v/gd.rpc
[Downloads Badge]: https://img.shields.io/pypi/dm/gd.rpc

[Documentation Badge]: https://github.com/nekitdev/gd.rpc/workflows/docs/badge.svg
[Check Badge]: https://github.com/nekitdev/gd.rpc/workflows/check/badge.svg

