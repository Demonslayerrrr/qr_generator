import pandas as pd
from reed_solomon import ReedSolomon

class ErrorCorrector:
    def __init__(self, bit_stream: str, version:int, error_correction_level:str) -> None:
        self.bit_stream = bit_stream.replace(" ","")
        self.version = version
        self.group_storage = []
        self.error_correction_level = error_correction_level
        self.data = pd.read_csv("./src/data.csv")
        self.num_blocks_g1 = int(self.get_block_info["Number of Blocks in Group 1"].values[0])
        self.num_blocks_g2 = int(self.get_block_info["Number of Blocks in Group 2"].values[0])
        self.ec_codewords_per_block = int(self.get_block_info["EC Codewords Per Block"].values[0])
        self.data_codeword_per_block1 = int(self.get_block_info["Data Codewords per Block in Group 1"].values[0])
        self.data_codeword_per_block2 = int(self.get_block_info["Data Codewords per Block in Group 2"].values[0])
        self.rs = ReedSolomon()

    @property
    def padding_handler(self):
        while len(self.bit_stream) % 8 != 0:
            self.bit_stream += "0"

        return self.bit_stream
    
    @property
    def bit_stream_groups(self):
        for i in range(0,len(self.padding_handler),8):
            self.group_storage.append(self.bit_stream[i:i+8])

        return self.group_storage
    
    @property
    def get_block_info(self):
        return self.data[self.data['Version'] == self.version][self.data["EC Level"] == self.error_correction_level]
    
    def generate_ec_blocks(self):
        data_bits = self.bit_stream_groups

        data_bytes = [int(byte, 2) for byte in data_bits]

        print(self.num_blocks_g1, self.num_blocks_g2, self.ec_codewords_per_block, self.data_codeword_per_block1, self.data_codeword_per_block2)

        rs_encoded_bytes = self.rs.rs_encode(data_bytes,self.ec_codewords_per_block)

        rs_encoded_bits =  ['{:08b}'.format(byte) for byte in rs_encoded_bytes]

        groups = {}

        print(len(rs_encoded_bits), len(data_bits), self.data_codeword_per_block1, self.ec_codewords_per_block)

        # for i in range(1,self.num_blocks_g1):
        #     data_codewords = []
        #     ec_codewords = []
        #     for x in range(self.data_codeword_per_block1):
        #         data_codewords.append(data_bits.pop(0))
        #     for y in range(self.ec_codewords_per_block):
        #         ec_codewords.append(rs_encoded_bits.pop(0))
        #     groups[i] = data_codewords + ec_codewords


        return groups
    # def add_finder_pattern(x, y):
    #     pattern = [
    #         [1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 1],
    #         [1, 1, 1, 1, 1, 1, 1],
    #     ]
    #     for i in range(7):
    #         for j in range(7):
    #             qr_matrix[y + i, x + j] = 0 if pattern[i][j] else 255




print(ErrorCorrector("0010 00000001010 01100001011 01111000110 10001011000 10001010011 01110111110 0000", 5, "M").padding_handler)
print(ErrorCorrector("0010 00000001010 01100001011 01111000110 10001011000 10001010011 01110111110 0000", 5, "M").bit_stream_groups)
print(ErrorCorrector("0010 00000001010 01100001011 01111000110 10001011000 10001010011 01110111110 0000", 5, "M").generate_ec_blocks())
