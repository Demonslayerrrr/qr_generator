import pandas as pd
from encode import Encoder


class BitStreamSender:
    def __init__(self, mode,char_count,encoded) -> None:
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
        self.paddings = ["11101100", "00010001" ]
        self.data = pd.read_csv("data.csv")

        self.mode = mode
        self.char_count = char_count
        self.encoded = encoded
        self.version, self.ec_level = self.estimate_version_and_level(mode,char_count,encoded)

    def get_character_count_length(self, mode: str) -> int:
        for version_range, count_length in self.character_count_indicator_table[mode].items():
            if self.version in version_range:
                return count_length
        raise ValueError(f"Version {self.version} out of range for mode {mode}")

    def build_temporary_bit_stream(self, mode: str, character_count: int, encoded: str) -> str:
        count_len = self.get_character_count_length(mode)
        return (
            self.indicators[mode] +
            format(character_count, f"0{count_len}b") +
            encoded +
            self.terminator
        )

    def add_paddings(self, bit_stream: str) -> str:
        bits_len = len(bit_stream)

        if bits_len % 8 != 0:
            bit_stream += "0" * (8 - bits_len % 8)

        total_codewords = self.data[
            (self.data['Version'] == self.version) & (self.data['EC Level'] == self.ec_level)
            ]['Total Data Codewords'].values[0]

        while len(bit_stream) < total_codewords * 8:
            bit_stream += self.paddings[(len(bit_stream) // 8) % 2]

        return bit_stream


    def build_bit_stream(self) -> str:
            bit_stream = self.build_temporary_bit_stream(self.mode, self.char_count, self.encoded)
            return self.add_paddings(bit_stream)

    def estimate_version_and_level(self, mode: str, character_count: int, encoded: str):
        for version in range(1, 41):
            for version_range, count_length in self.character_count_indicator_table[mode].items():
                if version in version_range:
                    count_len = count_length
                    break
            else:
                continue

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
