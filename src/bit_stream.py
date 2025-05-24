import pandas as pd
from encode import Encoder

class BitStreamSender:
    def __init__(self, char_count,encoded,mode) -> None:
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
        self.version, self.ec_level = self.estimate_version_and_level(mode, char_count, encoded)

    def get_character_count_length(self, mode: str) -> int:
        for version_range, count_length in self.character_count_indicator_table[mode].items():
            if self.version in version_range:
                return count_length
        raise ValueError(f"Version {self.version} out of range for mode {mode}")

    def build_bit_stream_without_paddings(self, mode: str, character_count: int, encoded: str) -> str:
        count_len = self.get_character_count_length(mode)
        return (
            self.indicators[mode] +
            format(character_count, f"0{count_len}b") +
            encoded +
            self.terminator
        )

    def make_8_bits_groups(self):
        bit_stream = self.build_bit_stream_without_paddings(self.mode, self.char_count, self.encoded)
        groups = []
        for i in range(0, len(bit_stream), 8):
            groups.append(bit_stream[i:i + 8])
        return groups


    def build_bit_stream(self) -> str:
        groups = self.make_8_bits_groups()

        for idx, val in enumerate(groups):
            if len(val) < 8:
                groups[idx] = val + "0" * (8 - len(val))

        total_codewords = self.data[
            (self.data['Version'] == self.version) & (self.data['EC Level'] == self.ec_level)
            ]['Total Data Codewords'].values[0]

        groups_str = "".join(groups)
        while len(groups_str) < total_codewords * 8:
            groups_str += self.paddings[(len(groups_str) // 8) % 2]

        return groups_str

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