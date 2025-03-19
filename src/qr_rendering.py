import numpy as np

class QRCodeEncoder:
    def __init__(self, version):
        self.size = 4 * version + 17
        self.matrix = np.full((self.size, self.size), None)
        
    def is_reserved(self, row, col):
        size = self.size
        if (row < 9 and col < 9) or (row < 9 and col >= size - 8) or (row >= size - 8 and col < 9):
            return True

        if row == 6 or col == 6:
            return True

        if row < 9 and col in [8, size-8] or col < 9 and row in [8, size-8]:
            return True
        return False
    
    def __str__(self):
        # Create a formatted string to represent the matrix
        matrix_str = ""
        for row in range(self.size):
            row_str = ""
            for col in range(self.size):
                if self.is_reserved(row, col):
                    row_str += "X"  # Reserved positions marked as X
                else:
                    row_str += " "  # Empty positions
            matrix_str += row_str + "\n"
        return matrix_str

a = QRCodeEncoder(5)

# Print the matrix using the custom string representation
print(a)
