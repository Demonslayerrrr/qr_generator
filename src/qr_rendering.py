import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pandas import read_csv

@dataclass
class FinderPattern:
    matrix = np.array([
        1,1,1,1,1,1,1,
        1,0,0,0,0,0,1,
        1,0,1,1,1,0,1,
        1,0,1,1,1,0,1,
        1,0,1,1,1,0,1,
        1,0,0,0,0,0,1,
        1,1,1,1,1,1,1
    ]).reshape(7, 7)

@dataclass
class AlignmentPattern:
    matrix = np.array([
        1,1,1,1,1,
        1,0,0,0,1,
        1,0,1,0,1,
        1,0,0,0,1,
        1,1,1,1,1
    ]).reshape(5, 5)

class QRCodeEncoder:
    def __init__(self, version:int,error_correction_level:str,bits:str):
        self.version = version
        self.error_correction_level = error_correction_level
        self.bits = bits
        self.size = 4 * version + 17
        self.matrix = np.full((self.size, self.size), None) 
        self.reserved = np.zeros((self.size, self.size), dtype=bool)

        self.format_string_table = read_csv("./src/format_string_table.csv")
        self.version_string_table = read_csv("./src/version_string_table.csv")
        


    def place_finder_patterns(self, pattern: FinderPattern):
        self.matrix[0:7, 0:7] = pattern.matrix
        self.matrix[0:7, self.size - 7:self.size] = pattern.matrix
        self.matrix[self.size - 7:self.size, 0:7] = pattern.matrix

        self.reserved[0:7, 0:7] = True
        self.reserved[0:8, self.size - 8:self.size] = True
        self.reserved[self.size - 8:self.size, 0:8] = True

    def place_alignment_patterns(self, pattern: AlignmentPattern):
        if self.version < 2:
            return  

        alignment_positions = self.get_alignment_positions()
        for r, c in alignment_positions:
            if not self.is_reserved(r, c):
                if r == 6 or c == 6:
                    self.matrix[r-2:r+3, c-2:c+3] = pattern.matrix
                    self.reserved[r-3:r+4, c-3:c+4] = True
                else:
                    self.matrix[r-2:r+3, c-2:c+3] = pattern.matrix
                    self.reserved[r-2:r+3, c-2:c+3] = True

    def place_timing_patterns(self):
        for i in range(0, self.size - 8):
            if not self.is_reserved(6, i):
                self.matrix[6, i] = not (i % 2)
                self.reserved[6,i] = True
            if not self.is_reserved(i, 6):
                self.matrix[i, 6] = not (i % 2)
                self.reserved[i, 6] = True

    def get_alignment_positions(self):
        alignment_centers = [
            [],  # Version 1 (no alignment pattern)
            [6, 18],  # Version 2
            [6, 22],  # Version 3
            [6, 26],  # Version 4
            [6, 30],  # Version 5
            [6, 34],  # Version 6
            [6, 22, 38],  # Version 7
            [6, 24, 42],  # Version 8
            [6, 26, 46],  # Version 9
            [6, 28, 50],  # Version 10
            [6, 30, 54],  # Version 11
            [6, 32, 58],  # Version 12
            [6, 34, 62],  # Version 13
            [6, 26, 46, 66],  # Version 14
            [6, 26, 48, 70],  # Version 15
            [6, 26, 50, 74],  # Version 16
            [6, 30, 54, 78],  # Version 17
            [6, 30, 56, 82],  # Version 18
            [6, 30, 58, 86],  # Version 19
            [6, 34, 62, 90],  # Version 20
            [6, 28, 50, 72, 94],  # Version 21
            [6, 26, 50, 74, 98],  # Version 22
            [6, 30, 54, 78, 102],  # Version 23
            [6, 28, 54, 80, 106],  # Version 24
            [6, 32, 58, 84, 110],  # Version 25
            [6, 30, 58, 86, 114],  # Version 26
            [6, 34, 62, 90, 118],  # Version 27
            [6, 26, 50, 74, 98, 122],  # Version 28
            [6, 30, 54, 78, 102, 126],  # Version 29
            [6, 26, 52, 78, 104, 130],  # Version 30
            [6, 30, 56, 82, 108, 134],  # Version 31
            [6, 34, 60, 86, 112, 138],  # Version 32
            [6, 30, 58, 86, 114, 142],  # Version 33
            [6, 34, 62, 90, 118, 146],  # Version 34
            [6, 30, 54, 78, 102, 126, 150],  # Version 35
            [6, 24, 50, 76, 102, 128, 154],  # Version 36
            [6, 28, 54, 80, 106, 132, 158],  # Version 37
            [6, 32, 58, 84, 110, 136, 162],  # Version 38
            [6, 26, 54, 82, 110, 138, 166],  # Version 39
            [6, 30, 58, 86, 114, 142, 170],  # Version 40
        ]

        alignment_coords = alignment_centers[self.version - 1]
        return [(r, c) for r in alignment_coords for c in alignment_coords if not (r < 9 and c < 9)]

    def is_reserved(self, row, col):
        return self.reserved[row, col]
    
    def place_dark_module(self):
        row, col = 4 * self.version + 9, 8 
        self.matrix[row, col] = 1
        self.reserved[row, col] = True

    def toggle_reserve_format_area(self,bool_state:bool):
        for i in range(9):
            if i != 6: 
                if not self.is_reserved(i, 8):
                    self.reserved[i, 8] = bool_state
                if not self.is_reserved(8, i):
                    self.reserved[8, i] = bool_state
        
        for i in range(8):
            if not self.is_reserved(self.size - 1 - i, 8):
                self.reserved[self.size - 1 - i, 8] = bool_state
            if not self.is_reserved(8, self.size - 1 - i):
                self.reserved[8, self.size - 1 - i] = bool_state

    def toggle_reserve_version_area(self, bool_state:bool):
        self.reserved[0:6, self.size - 11:self.size - 8] = bool_state
        self.reserved[self.size - 11:self.size - 8, 0:6] = bool_state

    def place_bits(self):
        row, col = self.size - 1, self.size - 1 
        direction = -1  
        bit_index = 0

        while col > 0:
            if col == 6:  
                col -= 1

            for i in range(2): 
                c = col - i
                if c < 0:
                    continue
                if not self.reserved[row][c] and bit_index < len(self.bits):
                    self.matrix[row][c] = int(self.bits[bit_index])
                    bit_index += 1
                
                row += direction
                if row < 0 or row >= self.size:
                    row -= direction
                    direction = -direction
                    col -= 2  
                    break

    def mask_condition(self, row, col, mask_pattern:int):
        match mask_pattern:
            case 0: return (row+col)%2 == 0
            case 1: return row%2 == 0
            case 2: return col%3 == 0
            case 3: return (row+col)%3 == 0
            case 4: return (row//2 + col//3)%2 == 0
            case 5: return (row*col)%2 + (row*col)%3 == 0
            case 6: return ((row*col)%2 + (row*col)%3)%2 == 0
            case 7: return ((row*col)%3 + (row+col)%2)%2 == 0
            case _: return False

    def apply_mask(self, mask_pattern:int):
        for r in range(self.size):
            for c in range(self.size):
                if not self.reserved[r, c]:
                    if self.mask_condition(r, c, mask_pattern):
                        self.matrix[r, c] = not self.matrix[r, c]
    def calculate_score(self):
        score = 0
        for r in range(self.size):
            for c in range(self.size):
                if not self.reserved[r, c]:
                    if self.matrix[r, c] == 1:
                        score += 3
                        if r > 0 and not self.reserved[r-1, c]:
                            score += 1
                        if c > 0 and not self.reserved[r, c-1]:
                            score += 1
                        if r < self.size - 1 and not self.reserved[r+1, c]:
                            score += 1
                        if c < self.size - 1 and not self.reserved[r, c+1]:
                            score += 1
        return score
    def evaluate_mask(self):
        best_score = 0
        best_mask = 0
        for mask in range(8):
            self.apply_mask(mask)
            score = self.calculate_score()
            if score > best_score:
                best_score = score
                best_mask = mask
            self.apply_mask(mask)

        return best_mask
    
    def place_format_string(self,mask_pattern:int):
        self.toggle_reserve_format_area(False)
        format_string = self.format_string_table[(self.format_string_table["Mask Pattern"] == mask_pattern) & (self.format_string_table["ECC Level"] == self.error_correction_level)]["Type Information Bits"].values[0]
        
        for i in range(9):
            if i != 6: 
                self.matrix[i,8] = format_string[i]

                self.matrix[8, i] = format_string[i]
        
        for i in range(8):

            self.matrix[self.size - 1 - i, 8] = format_string[len(format_string) - i]
            self.reserved[8, self.size - 1 - i] = format_string[len(format_string) - i]

    def visualize(self):
        self.place_finder_patterns(FinderPattern())
        self.place_alignment_patterns(AlignmentPattern())
        self.place_timing_patterns()
        self.place_dark_module()
        self.toggle_reserve_format_area(True)
        if self.version >= 7:
            self.toggle_reserve_version_area(True)
        self.place_bits()
        mask_pattern = self.evaluate_mask()
        self.apply_mask(mask_pattern)

        
        display_matrix = 1 - np.where(self.matrix == None, 0, self.matrix).astype(int)

        plt.figure(figsize=(8, 8))
        plt.imshow(display_matrix, cmap='gray', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.show()

# qr = QRCodeEncoder(3, "0100000000000000000000000000000000000000000000000000000000000000101101000000000000000000000000001000011000000000000000000000000001010110000000000000000000000000110001100000000000000000000000001100011000000000000000000000000011110111000000000000000000000000011101100000000000000000000000001111011100000000000000000000000000100110000000000000000000000000110001100000000000000000000000000100001000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001011110000000000000000000000001000000100000000000000000000000001110001000000000000000000000000100101010000000000000000000000000011110000000000000000000000000000110001000000000000000000000000111100010000000000000000000000000101010100000000000000000000000010001100000000000000000000000000000101110000000000000000000000001110101000000000000000000000000000000011000000000000000000000000001100010000000000000000000000001011110000000000000000000000000000001011000000000000000000000000011111000000000000000000000000000001011000000000000000000000000010011101000000000000000000000000")
qr = QRCodeEncoder(2,"L", "0100000000000001100001101000011101000111010001110000011100110011101000101111001011110111010101100110011000110110011001101001011000100110000100000011101101110100101101001001011111100110111000101111011110001100")
qr.visualize()