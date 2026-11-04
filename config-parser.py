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
                    stripped_line: str = line.strip()
                    
                    if not stripped_line or stripped_line.startswith("#"):
                        continue

                    if "=" not in stripped_line:
                        raise ConfigError(f"Invalid syntax on line {line_num}:\n    {line.strip()}")

                    key, value = stripped_line.split("=", 1)
                    clean_key = key.strip().upper()
                    clean_val = value.strip()

                    try:
                        if clean_key == "WIDTH":
                            width = int(clean_val)
                            has_width = True
                        elif clean_key == "HEIGHT":
                            height = int(clean_val)
                            has_height = True
                        elif clean_key == "OUTPUT_FILE":
                            output_file = clean_val
                            has_output = True
                        elif clean_key == "PERFECT":
                            perfect = """_parse_bool(clean_val)"""
                            has_perfect = True
                        elif clean_key == "ENTRY":
                            """entry = _parse_coords(clean_val)"""
                            has_entry = True
                        elif clean_key == "EXIT":
                            """exit_pos = _parse_coords(clean_val)"""
                            has_exit = True
                        elif clean_key == "SEED":
                            seed = int(clean_val)
                    except ValueError as err:
                        raise ConfigError(
                            f"Value error on line {line_num} for key '{clean_key}': {err}"
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
