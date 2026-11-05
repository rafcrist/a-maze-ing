from dataclasses import dataclass
from typing import Optional


class ConfigError(Exception):
    """Config Errors"""


@dataclass(frozen=True)
class MazeConfig:
    """Represent the configuration settings for maze generation."""

    _width: int
    _height: int
    _entry: tuple[int, int]
    _exit: tuple[int, int]
    _output_file: str
    _perfect: bool
    _seed: Optional[int] = None

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

    @staticmethod
    def _validate_positive(value: int) -> None:
        """Validates that value is strictly positive (> 0)."""
        if value <= 0:
            raise ValueError(
                f"Value must be strictly positive (> 0), got {value}"
            )

    @staticmethod
    def _check_duplicate(flag: bool, key_name: str, line_num: int) -> None:
        """Raises ConfigError if a key has already been defined."""
        if flag:
            raise ConfigError(f"Duplicate key '{key_name}' on line {line_num}")

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Converts string to boolean."""
        normalized_value = value.strip().lower()
        if normalized_value == "true":
            return True
        if normalized_value == "false":
            return False
        raise ValueError(
            f"Invalid boolean value: '{value}' (expected True or False)"
        )

    @staticmethod
    def _parse_coords(value: str) -> tuple[int, int]:
        """Converts string 'x,y' to tuple of ints."""
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError(
                f"Invalid coordinates format: '{value}' expected (x,y)"
            )
        try:
            return (int(parts[0].strip()), int(parts[1].strip()))
        except ValueError as err:
            raise ValueError(
                f"Invalid coordinate numbers in '{value}': {err}"
            ) from err

    @classmethod
    def parse_config(cls, filename: str) -> "MazeConfig":
        """Read configuration file, validate parameters,
            and instantiate MazeConfig."""
        width: int = 0
        height: int = 0
        entry: tuple[int, int] = (0, 0)
        exit_pos: tuple[int, int] = (0, 0)
        output_file: str = ""
        perfect: bool = True
        seed: Optional[int] = None

        has_width = False
        has_height = False
        has_entry = False
        has_exit = False
        has_output = False
        has_perfect = False
        has_seed = False

        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, start=1):
                    current_line: str = line.strip()

                    if not current_line or current_line.startswith("#"):
                        continue

                    if "=" not in current_line:
                        raise ConfigError(
                            f"SyntaxError on line {line_num} : {line.strip()}"
                        )

                    key, value = current_line.split("=", 1)
                    current_key = key.strip().upper()
                    current_value = value.strip()

                    try:
                        if current_key == "WIDTH":
                            cls._check_duplicate(
                                has_width, current_key, line_num
                            )
                            width = int(current_value)
                            cls._validate_positive(width)
                            has_width = True
                        elif current_key == "HEIGHT":
                            cls._check_duplicate(
                                has_height, current_key, line_num
                            )
                            height = int(current_value)
                            cls._validate_positive(height)
                            has_height = True
                        elif current_key == "OUTPUT_FILE":
                            cls._check_duplicate(
                                has_output, current_key, line_num
                            )
                            if not current_value:
                                raise ValueError(
                                    "OUTPUT_FILE value cannot be empty"
                                )
                            output_file = current_value
                            has_output = True
                        elif current_key == "PERFECT":
                            cls._check_duplicate(
                                has_perfect, current_key, line_num
                            )
                            perfect = cls._parse_bool(current_value)
                            has_perfect = True
                        elif current_key == "ENTRY":
                            cls._check_duplicate(
                                has_entry, current_key, line_num
                            )
                            entry = cls._parse_coords(current_value)
                            has_entry = True
                        elif current_key == "EXIT":
                            cls._check_duplicate(
                                has_exit, current_key, line_num
                            )
                            exit_pos = cls._parse_coords(current_value)
                            has_exit = True
                        elif current_key == "SEED":
                            cls._check_duplicate(
                                has_seed, current_key, line_num
                            )
                            seed = int(current_value)
                            has_seed = True
                        else:
                            raise ConfigError(
                                f"Invalid key: '{current_key}' "
                                f"on line {line_num}"
                            )
                    except ValueError as err:
                        raise ConfigError(
                            f"\nValue error on line {line_num} "
                            f"for key '{current_key}': {err}"
                        ) from err

            if not (
                has_width
                and has_height
                and has_entry
                and has_exit
                and has_output
                and has_perfect
            ):
                raise ConfigError(
                    "Missing one or more mandatory configuration keys."
                )

            if entry == exit_pos:
                raise ConfigError(
                    "ENTRY and EXIT coordinates must be distinct, "
                    f"got {entry}"
                )

            for pos_name, (x, y) in [("ENTRY", entry), ("EXIT", exit_pos)]:
                if x < 0 or y < 0:
                    raise ConfigError(
                        f"{pos_name} coordinates ({x}, {y}) "
                        "cannot be negative."
                    )
                if x >= width or y >= height:
                    raise ConfigError(
                        f"{pos_name} coordinates ({x}, {y}) "
                        "exceed maze dimensions "
                        f"(width={width}, height={height})."
                    )

            return cls(
                _width=width,
                _height=height,
                _entry=entry,
                _exit=exit_pos,
                _output_file=output_file,
                _perfect=perfect,
                _seed=seed,
            )

        except FileNotFoundError:
            raise ConfigError(f"FileError: '{filename}' not found")
        except PermissionError:
            raise ConfigError(f"FileError: '{filename}' permission denied")
        except OSError as err:
            raise ConfigError(f"FileError: '{filename}' : {err}")
