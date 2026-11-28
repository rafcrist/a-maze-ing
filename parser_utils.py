class ConfigError(Exception):
    """Exception raised for configuration file and validation errors."""


def validate_positive(value: int, key_name: str) -> None:
    """Validate that an integer parameter is strictly positive (> 0)."""
    if value <= 0:
        raise ConfigError(
            f"{key_name} must be strictly positive (> 0), got {value}"
        )


def parse_int(value: str, key_name: str, line_num: int) -> int:
    """Convert string to int, raising ConfigError on invalid input."""
    try:
        return int(value)
    except ValueError as err:
        raise ConfigError(
            f"Value error on line {line_num} for key '{key_name}': {err}"
        ) from err


def parse_bool(value: str, key_name: str, line_num: int) -> bool:
    """Convert string to boolean, raising ConfigError on invalid input."""
    normalized_value = value.strip().lower()
    if normalized_value == "true":
        return True
    if normalized_value == "false":
        return False
    raise ConfigError(
        f"Value error on line {line_num} for key '{key_name}': "
        f"Invalid boolean value: '{value}' (expected True or False)"
    )


def parse_coords(
    value: str, key_name: str, line_num: int
) -> tuple[int, int]:
    """Convert string 'x,y' to tuple of ints, raising ConfigError on error."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(
            f"Value error on line {line_num} for key '{key_name}': "
            f"Invalid coordinates format: '{value}' (expected x,y)"
        )
    try:
        return (int(parts[0].strip()), int(parts[1].strip()))
    except ValueError as err:
        raise ConfigError(
            f"Value error on line {line_num} for key '{key_name}': "
            f"Invalid coordinate numbers in '{value}': {err}"
        ) from err
