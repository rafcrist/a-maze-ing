from typing import Optional

from entry_parser import read_raw_config
from parser_utils import (
    ConfigError,
    parse_bool,
    parse_coords,
    parse_int,
    validate_positive,
)


class MazeConfig:
    """Validated configuration settings for maze generation."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int] = None,
    ) -> None:
        validate_positive(width, "WIDTH")
        validate_positive(height, "HEIGHT")

        if not output_file.strip():
            raise ConfigError("OUTPUT_FILE value cannot be empty.")

        if entry == exit_pos:
            raise ConfigError(
                f"ENTRY and EXIT coordinates must be distinct, got {entry}."
            )

        for pos_name, pos in [("ENTRY", entry), ("EXIT", exit_pos)]:
            x, y = pos
            if x < 0 or y < 0:
                raise ConfigError(
                    f"{pos_name} coordinates ({x}, {y}) cannot be negative."
                )
            if x >= width or y >= height:
                raise ConfigError(
                    f"{pos_name} coordinates ({x}, {y}) exceed maze "
                    f"dimensions (width={width}, height={height})."
                )

        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_pos
        self._output_file = output_file
        self._perfect = perfect
        self._seed = seed

    @classmethod
    def from_file(cls, filename: str) -> "MazeConfig":
        """Factory method that builds a MazeConfig from a config file."""
        raw_values, line_numbers = read_raw_config(filename)

        width = parse_int(
            raw_values["WIDTH"], "WIDTH", line_numbers["WIDTH"]
        )
        height = parse_int(
            raw_values["HEIGHT"], "HEIGHT", line_numbers["HEIGHT"]
        )
        entry = parse_coords(
            raw_values["ENTRY"], "ENTRY", line_numbers["ENTRY"]
        )
        exit_pos = parse_coords(
            raw_values["EXIT"], "EXIT", line_numbers["EXIT"]
        )
        output_file = raw_values["OUTPUT_FILE"]
        perfect = parse_bool(
            raw_values["PERFECT"], "PERFECT", line_numbers["PERFECT"]
        )

        seed: Optional[int] = None
        if "SEED" in raw_values:
            seed = parse_int(
                raw_values["SEED"], "SEED", line_numbers["SEED"]
            )

        return cls(
            width=width,
            height=height,
            entry=entry,
            exit_pos=exit_pos,
            output_file=output_file,
            perfect=perfect,
            seed=seed,
        )

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        return self._exit

    @property
    def output_file(self) -> str:
        return self._output_file

    @property
    def perfect(self) -> bool:
        return self._perfect

    @property
    def seed(self) -> Optional[int]:
        return self._seed

    def __repr__(self) -> str:
        return (
            f"\n=== MazeConfig ==="
            f"\n width={self._width}"
            f"\n height={self._height}"
            f"\n entry={self._entry}"
            f"\n exit={self._exit}"
            f"\n output_file={self._output_file!r}"
            f"\n perfect={self._perfect}"
            f"\n seed={self._seed}"
        )
