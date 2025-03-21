import pandas as pd
from reed_solomon import ReedSolomon

class ErrorCorrector:
    def __init__(self, bit_stream: str, version: int, error_correction_level: str) -> None:
        self.bit_stream = bit_stream.replace(" ", "") 
        self.version = version
        self.error_correction_level = error_correction_level
        self.data = pd.read_csv("./src/data.csv")  
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

        total_data_codewords = (self.num_blocks_g1 * self.data_codeword_per_block1) + \
                               (self.num_blocks_g2 * self.data_codeword_per_block2)

        if len(data_bytes) < total_data_codewords:
            data_bytes.extend([0] * (total_data_codewords - len(data_bytes)))
        elif len(data_bytes) > total_data_codewords:
            data_bytes = data_bytes[:total_data_codewords]

        groups = {}
        index = 0
        blocks_g1 = []

        for i in range(self.num_blocks_g1):
            block = data_bytes[index:index + self.data_codeword_per_block1]
            index += self.data_codeword_per_block1
            ec_codewords = self.rs.rs_encode(block, self.ec_codewords_per_block)
            ec_block = block + ec_codewords
            binary_ec_block = [format(code, '08b') for code in ec_block]
            blocks_g1.append(binary_ec_block)
            groups[1] = blocks_g1


        blocks_g2 = []
        for i in range(self.num_blocks_g2):
            block = data_bytes[index:index + self.data_codeword_per_block2]
            index += self.data_codeword_per_block2
            ec_codewords = self.rs.rs_encode(block, self.ec_codewords_per_block)
            ec_block = block + ec_codewords
            binary_ec_block = [format(code, '08b') for code in ec_block]
            blocks_g2.append(binary_ec_block)
            groups[2] = blocks_g2

        return blocks_g1, blocks_g2
    
    def generate_interleave_blocks(self):
        blocks_g1, blocks_g2 = self.generate_ec_blocks()
        
        interleaved_data = []
        interleaved_ec = []
        
        max_data_codewords = max(self.data_codeword_per_block1, self.data_codeword_per_block2)
        
        for i in range(max_data_codewords):
            for block in blocks_g1:
                if i < len(block) - self.ec_codewords_per_block: 
                    interleaved_data.append(block[i])
            for block in blocks_g2:
                if i < len(block) - self.ec_codewords_per_block: 
                    interleaved_data.append(block[i])

        for i in range(self.ec_codewords_per_block):
            for block in blocks_g1:
                interleaved_ec.append(block[-self.ec_codewords_per_block + i])
            for block in blocks_g2:
                interleaved_ec.append(block[-self.ec_codewords_per_block + i])


        final_bit_stream = ''.join(interleaved_data + interleaved_ec)

        return final_bit_stream
