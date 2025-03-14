class ReedSolomon:
    def __init__(self):
        self.GF_EXP = [0] * 512
        self.GF_LOG = [0] * 256
        self._init_galois_field()

    def _init_galois_field(self):
        """Initialize Galois Field tables for fast arithmetic in GF(2^8)."""
        poly = 0x11D  
        x = 1
        for i in range(255):
            self.GF_EXP[i] = x
            self.GF_LOG[x] = i
            x <<= 1
            if x & 0x100:
                x ^= poly
        for i in range(255, 512):  
            self.GF_EXP[i] = self.GF_EXP[i - 255]

    def gf_multiply(self, x, y):
        """Multiply two numbers in GF(2^8)."""
        if x == 0 or y == 0:
            return 0
        return self.GF_EXP[self.GF_LOG[x] + self.GF_LOG[y]]

    def gf_poly_multiply(self, p, q):
        """Multiply two polynomials in GF(2^8)."""
        result = [0] * (len(p) + len(q) - 1)
        for i in range(len(p)):
            for j in range(len(q)):
                result[i + j] ^= self.gf_multiply(p[i], q[j])
        return result

    def generate_generator_poly(self, degree):
        """Generate the generator polynomial for Reed-Solomon."""
        g = [1]
        for i in range(degree):
            g = self.gf_poly_multiply(g, [1, self.GF_EXP[i]])
        return g

    def rs_encode(self, data, ec_length):
        """Encode data with Reed-Solomon and return the error correction bytes."""
        generator = self.generate_generator_poly(ec_length)

        message = data + [0] * ec_length
        for i in range(len(data)):
            coef = message[i]
            if coef != 0:
                for j in range(len(generator)):
                    message[i + j] ^= self.gf_multiply(generator[j], coef)
        return message[-ec_length:]  

# bit_stream = "00100000000101001100001011011110001101000101100010001010011011101111100000000000"
# data_bytes = [bit_stream[i:i+8] for i in range(0, len(bit_stream), 8)]
# data_values = [int(byte, 2) for byte in data_bytes]

# rs = ReedSolomon()
# ec_length = 10  
# error_correction_bytes = rs.rs_encode(data_values, ec_length)

# ec_bits = ['{:08b}'.format(byte) for byte in error_correction_bytes]
# final_message = data_bytes + ec_bits 

# print("Data Bytes:", data_bytes)
# print("Error Correction Bytes:", ec_bits)
# print("Final Message (Binary Groups):", final_message)
