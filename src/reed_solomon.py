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


