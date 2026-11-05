from dataclasses import dataclass

class ConfigError(Exception):
    """Config Errors"""

@dataclass
class MazeConfig:
    """represent the configuration settings for maze generation."""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = None

    @classmethod
    def parse_config(cls, filename: str) -> "MazeConfig":
        """read the configuration file as filename and instance the MazeConfig class.
            if a filename or value errors occurs the method dont instance this class and launch the first error."""

        """pattern values ro start the object"""
        width: int = 0
        height: int = 0
        entry: tuple[int, int] = (0, 0)
        exit_pos: tuple[int, int] = (0, 0)
        output_file: str = ""
        perfect: bool = True
        seed: int = 0

        """control to distinc if a key was find in the file"""
        has_width = False
        has_height = False
        has_entry = False
        has_exit = False
        has_output = False
        has_perfect = False

        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                """open file and verify """
                for line_num, line in enumerate(file, start=1):
                    current_line: str = line.strip()
                    
                    if not current_line or current_line.startswith("#"):
                        continue

                    if "=" not in current_line:
                        raise ConfigError(f"SintaxError on line {line_num}:\n    {line.strip()}")

                    key, value = current_line.split("=", 1)
                    current_key = key.strip().upper()
                    current_value = value.strip()

                    try:
                        if current_key == "WIDTH":
                            width = int(current_value)
                            has_width = True
                        elif current_key == "HEIGHT":
                            height = int(current_value)
                            has_height = True
                        elif current_key == "OUTPUT_FILE":
                            output_file = current_value
                            has_output = True
                        elif current_key == "PERFECT":
                            perfect = _parse_bool(current_value, line, line_num)
                            has_perfect = True
                        elif current_key == "ENTRY":
                            """entry = _parse_coords(current_value)"""
                            has_entry = True
                        elif current_key == "EXIT":
                            """exit_pos = _parse_coords(current_value)"""
                            has_exit = True
                        elif current_key == "SEED":
                            seed = int(current_value)
                    except ValueError as err:
                        raise ConfigError(
                            f"Value error on line {line_num} for key '{current_key}': {err}"
                        ) from err

            if not (has_width and has_height and has_entry and has_exit and has_output and has_perfect):
                raise ConfigError("Missing one or more mandatory configuration keys.")

            return cls(
                width=width,
                height=height,
                entry=entry,
                exit=exit_pos,
                output_file=output_file,
                perfect=perfect,
                seed=seed,
            )

        except FileNotFoundError:
            raise ConfigError(f"FileError: '{filename}' not found")
        except PermissionError:
            raise ConfigError(f"FileError: '{filename}' permission denied")
        except OSError as err:
            raise ConfigError(f"FileError: '{filename}' : {err}")


    def _parse_bool(value: str) -> bool:
        """Converts string to boolean."""
        """normalize value for not case sensitive read"""
        normalized_value = value.strip().lower()

        if normalized_value == "true":
            return True
        if normalized_value == "false":
            return False
        raise ValueError(f"Invalid boolean value: '{value}' (expected True or False)")

if __name__ == "__main__":
    print("=== A testar o Parser de Configuração (Card 02) ===")
    
    # Cria um ficheiro de configuração temporário para teste
    test_filename = "test_config.txt"
    with open(test_filename, "w", encoding="utf-8") as f:
        f.write("# Ficheiro de teste\n")
        f.write("WIDTH = 15\n")
        f.write("HEIGHT = 10\n")
        f.write("ENTRY = 0,0\n")
        f.write("EXIT = 14,9\n")
        f.write("OUTPUT_FILE = maze_out.txt\n")
        f.write("PERFECT = True\n")
        f.write("SEED = 42\n")

    try:
        # Testa a função diretamente
        config = MazeConfig.parse_config(test_filename)
        print("[OK] parse_config executado com sucesso!")
        print(f"  -> Objeto gerado: {config}")
        print(f"  -> Largura: {config.width}, Altura: {config.height}")
        print(f"  -> Entrada: {config.entry}, Saída: {config.exit}")
        print(f"  -> Perfeito: {config.perfect}, Seed: {config.seed}")
    except ConfigError as e:
        print(f"[ERRO] Falha no teste: {e}")
