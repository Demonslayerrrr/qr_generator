import pandas as pd

class BitStreamSender:
    def __init__(self) -> None:
        self.indicators = {
            "numeric": "0001",
            "alphanumeric": "0010",
            "bytes": "0100",
            "kanji": "1000"
        }
        self.character_count_indicator_table = {
            "numeric": {range(1, 10): 10, range(10, 27): 12, range(27, 41): 14},
            "alphanumeric": {range(1, 10): 9, range(10, 27): 11, range(27, 41): 13},
            "bytes": {range(1, 10): 8, range(10, 27): 16, range(27, 41): 16},
            "kanji": {range(1, 10): 8, range(10, 27): 10, range(27, 41): 12}
        }
        self.terminator = "0000"
        self.data = pd.read_csv("./src/data.csv")

    def get_character_count_length(self, mode: str, version: int) -> int:
        for version_range, count_length in self.character_count_indicator_table[mode].items():
            if version in version_range:
                return count_length
        raise ValueError(f"Version {version} out of range for mode {mode}")

    def build_bit_stream(self, mode: str, character_count: int, encoded: str, version: int) -> str:
        count_len = self.get_character_count_length(mode, version)
        return (
            self.indicators[mode] +
            format(character_count, f"0{count_len}b") +
            encoded +
            self.terminator
        )

    def estimate_version_and_level(self, mode: str, character_count: int, encoded: str):
        for version in range(1, 41):
            count_len = self.get_character_count_length(mode, version)
            temp_stream = (
                self.indicators[mode] +
                format(character_count, f"0{count_len}b") +
                encoded +
                self.terminator
            )
            bits_len = len(temp_stream)
            bytes_len = (bits_len + 7) // 8
            for level in ['L', 'M', 'Q', 'H']:
                version_data = self.data[(self.data['Version'] == version) & (self.data['EC Level'] == level)]
                if not version_data.empty:
                    codewords = version_data['Total Data Codewords'].values[0]
                    if bytes_len <= codewords:
                        return version, level
        return None, None

