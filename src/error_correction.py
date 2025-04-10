import pandas as pd
from reed_solomon import ReedSolomon

class ErrorCorrector:
    def __init__(self, bit_stream: str) -> None:
        self.bit_stream = bit_stream.replace(" ", "")
        self.data = pd.read_csv("./src/data.csv")
        self.version, self.error_correction_level = self.choose_qr_version_and_level()
        self.num_blocks_g1 = int(self.get_block_info["Number of Blocks in Group 1"].values[0])
        self.num_blocks_g2 = (
            int(self.get_block_info["Number of Blocks in Group 2"].values[0])
            if (len(values := self.get_block_info["Number of Blocks in Group 2"].values) > 0 and pd.notna(values[0]))
            else 0
        )
        self.ec_codewords_per_block = int(self.get_block_info["EC Codewords Per Block"].values[0])
        self.data_codeword_per_block1 = int(self.get_block_info["Data Codewords per Block in Group 1"].values[0])
        self.data_codeword_per_block2 = (
            int(self.get_block_info["Data Codewords per Block in Group 2"].values[0])
            if (len(values := self.get_block_info["Data Codewords per Block in Group 2"].values) > 0 and pd.notna(values[0]))
            else 0
        )
        self.rs = ReedSolomon()

    @property
    def padding_handler(self):
        while len(self.bit_stream) % 8 != 0:
            self.bit_stream += "0"
        return self.bit_stream

    @property
    def bit_stream_groups(self):
        group_storage = [self.bit_stream[i:i + 8] for i in range(0, len(self.padding_handler), 8)]
        return group_storage

    @property
    def get_block_info(self):
        return self.data[(self.data['Version'] == self.version) & (self.data["EC Level"] == self.error_correction_level)]

    def generate_ec_blocks(self):
        data_bits = self.bit_stream_groups
        data_bytes = [int(byte, 2) for byte in data_bits]

        total_data_codewords = (self.num_blocks_g1 * self.data_codeword_per_block1) + (self.num_blocks_g2 * self.data_codeword_per_block2)

        if len(data_bytes) < total_data_codewords:
            data_bytes.extend([0] * (total_data_codewords - len(data_bytes)))
        elif len(data_bytes) > total_data_codewords:
            data_bytes = data_bytes[:total_data_codewords]

        blocks = []
        index = 0

        for i in range(self.num_blocks_g1):
            block = data_bytes[index:index + self.data_codeword_per_block1]
            index += self.data_codeword_per_block1
            ec_codewords = self.rs.rs_encode(block, self.ec_codewords_per_block)
            ec_block = block + ec_codewords
            blocks.append(ec_block)

        for i in range(self.num_blocks_g2):
            block = data_bytes[index:index + self.data_codeword_per_block2]
            index += self.data_codeword_per_block2
            ec_codewords = self.rs.rs_encode(block, self.ec_codewords_per_block)
            ec_block = block + ec_codewords
            blocks.append(ec_block)

        binary_blocks = [[format(code, '08b') for code in block] for block in blocks]
        return binary_blocks

    def generate_interleave_blocks(self):
        blocks = self.generate_ec_blocks()

        interleaved_data = []
        interleaved_ec = []

        max_data_codewords = max(self.data_codeword_per_block1, self.data_codeword_per_block2)

        for i in range(max_data_codewords):
            for block in blocks:
                if i < len(block) - self.ec_codewords_per_block:
                    interleaved_data.append(block[i])

        for i in range(self.ec_codewords_per_block):
            for block in blocks:
                interleaved_ec.append(block[-self.ec_codewords_per_block + i])

        final_bit_stream = ''.join(interleaved_data + interleaved_ec)
        return final_bit_stream

    def choose_qr_version_and_level(self):
        data_bytes = len(self.bit_stream) / 8
        error_correction_levels = ['L', 'M', 'Q', 'H']

        for version in range(1, 41):
            for level in error_correction_levels:
                version_data = self.data[(self.data['Version'] == version) & (self.data['EC Level'] == level)]
                if not version_data.empty:
                    codewords = version_data['Total Data Codewords'].values[0]
                    if data_bytes <= codewords:
                        return version, level

        return None, None

a =ErrorCorrector("0100 0000000000011000 01101000 01110100 01110100 01110000 01110011 00111010 00101111 00101111 01110101 01100110 01100011 01100110 01101001 01100111 01101000 01110100 01110000 01100001 01110011 01110011 00101110 01100011 01101111 01101101 0000")
b =a.generate_interleave_blocks()

print(b,len(b), a.version, a.error_correction_level)