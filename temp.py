#!/usr/bin/env python3

import pathlib
import typing
import uuid
from abc import ABC, abstractmethod
from argparse import ArgumentParser

# The global (system-wide) temporary folder
SYSTEM_TMP_HOME = "/tmp"


class TmpNameGen(ABC):
    """The parent class for objects with the ability to create a dynamically-changing file name string."""

    @abstractmethod
    def name(self) -> str:
        """Generates a name string to use for a file name."""
        return ""


class CountNameGen(TmpNameGen):
    """A name generator which yields progressively increasing numerical values (as strings).

    e.g. `1`, `2`, `3`, ...
    """

    def __init__(self):
        """Initializes the internal counter."""
        self._count = 0

    def name(self) -> str:
        """Increments the current count, then returns the string number."""
        self._count += 1
        return str(self._count)


class UuidNameGen(TmpNameGen):
    def name(self) -> str:
        """Gets a generated universally unique id."""
        return str(uuid.uuid4().hex)


class TmpGen:
    """The actual temporary file generator, which creates unique temporary objects."""

    def __init__(self, name_gen: typing.Optional[TmpNameGen] = None):
        if name_gen:
            self._namer = name_gen
        else:
            self._namer = self._default_namer()

    def _default_namer(self) -> TmpNameGen:
        """The default naming algorithm for a temporary file or directory."""
        return UuidNameGen()

    def _get_unique(self) -> pathlib.Path:
        """Creates a unique path to a child of the global temporary object home."""
        while True:
            # Append the name generated to the global home temporary directory
            target = pathlib.Path(SYSTEM_TMP_HOME) / self._namer.name()
            # Check if the name will not conflict an existing temporary item
            if not target.exists():
                return target

    def _make(self, is_file=True) -> pathlib.Path:
        """Creates a new temporary object.

        If the argument `is_file` is true, then the path created is treated as a file and created immediately.
        Otherwise, a directory is created. Finally, the path is then returned."""
        # Get path
        target = self._get_unique()
        if is_file:
            # Create file
            target.touch()
        else:
            # Create dir
            target.mkdir()
        # Return path
        return target

    def tmp_file(self) -> pathlib.Path:
        return self._make(is_file=True)

    def tmp_dir(self) -> pathlib.Path:
        return self._make(is_file=False)


def tmp_file() -> pathlib.Path:
    """Easy-access getter for a temporary file."""
    return TmpGen().tmp_file()


def tmp_dir() -> pathlib.Path:
    """Easy-access getter for a temporary directory."""
    return TmpGen().tmp_dir()


def main():
    parser = ArgumentParser(
        description="A utility script to create temporary files and/or directories"
    )
    gen_group = parser.add_mutually_exclusive_group()
    gen_group.add_argument(
        "--number",
        "-n",
        help="Use a deterministic, numerically increasing value as the temporary object's name",
        action="store_true",
    )
    gen_group.add_argument(
        "--uuid",
        "-u",
        help="Use a non-deterministic universally-unique identifier as the temporary object's name",
        action="store_true",
    )
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        "--file",
        "-f",
        help="Create a temporary file; A single buffer of text",
        action="store_true",
    )
    type_group.add_argument(
        "--directory",
        "-d",
        help="Create a temporary directory; A folder which may hold a dynamic number of files",
        action="store_true",
    )
    args = parser.parse_args()
    # Generator Type
    if args.number:
        gen = TmpGen(name_gen=CountNameGen())
    elif args.uuid:
        gen = TmpGen(name_gen=UuidNameGen())
    else:
        gen = TmpGen()

    if args.directory:
        return f"{gen.tmp_dir()}/"
    else:
        return str(gen.tmp_file())


if __name__ == "__main__":
    print(main())
