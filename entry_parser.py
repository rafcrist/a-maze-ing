from parser_utils import ConfigError

REQUIRED_KEYS: list[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]
ALLOWED_KEYS: list[str] = REQUIRED_KEYS + ["SEED"]


def read_raw_config(
    filename: str,
) -> tuple[dict[str, str], dict[str, int]]:
    """Read and validate raw KEY=VALUE entries from a config file."""
    raw_values: dict[str, str] = {}
    line_numbers: dict[str, int] = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                current_line = line.strip()

                if not current_line or current_line.startswith("#"):
                    continue

                if "=" not in current_line:
                    raise ConfigError(
                        f"SyntaxError on line {line_num}: {current_line}"
                    )

                key, value = current_line.split("=", 1)
                current_key = key.strip().upper()
                current_value = value.strip()

                if current_key not in ALLOWED_KEYS:
                    raise ConfigError(
                        f"Invalid key: '{current_key}' on line {line_num}"
                    )

                if current_key in raw_values:
                    raise ConfigError(
                        f"Duplicate key '{current_key}' on line {line_num}"
                    )

                if not current_value:
                    raise ConfigError(
                        f"Empty value for key '{current_key}' "
                        f"on line {line_num}"
                    )

                raw_values[current_key] = current_value
                line_numbers[current_key] = line_num
    except FileNotFoundError:
        raise ConfigError(f"FileError: '{filename}' not found")
    except PermissionError:
        raise ConfigError(f"FileError: '{filename}' permission denied")
    except OSError as err:
        raise ConfigError(f"FileError: '{filename}': {err}")

    missing_keys: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in raw_values:
            missing_keys.append(key)

    if missing_keys:
        missing_str = ", ".join(missing_keys)
        raise ConfigError(
            f"Missing mandatory configuration keys: {missing_str}"
        )

    return raw_values, line_numbers
