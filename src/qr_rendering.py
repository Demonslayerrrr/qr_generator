import numpy as np
import matplotlib
matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pandas import read_csv
from masking import Masking

@dataclass
class LeftTopFinderPattern:
    matrix = np.array([
        1,1,1,1,1,1,1,0,
        1,0,0,0,0,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,0,0,0,0,1,0,
        1,1,1,1,1,1,1,0,
        0,0,0,0,0,0,0,0,
    ]).reshape(8,8)

@dataclass
class RightTopFinderPattern:
    matrix = np.array([
        0,1,1,1,1,1,1,1,
        0,1,0,0,0,0,0,1,
        0,1,0,1,1,1,0,1,
        0,1,0,1,1,1,0,1,
        0,1,0,1,1,1,0,1,
        0,1,0,0,0,0,0,1,
        0,1,1,1,1,1,1,1,
        0,0,0,0,0,0,0,0,
    ]).reshape(8,8)

@dataclass
class LeftBottomFinderPattern:
    matrix = np.array([
        0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,0,
        1,0,0,0,0,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,1,1,1,0,1,0,
        1,0,0,0,0,0,1,0,
        1,1,1,1,1,1,1,0,
    ]).reshape(8,8)
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
        self.matrix = np.full((self.size, self.size), 0) 
        self.reserved = np.zeros((self.size, self.size), dtype=bool)

        self.format_string_table = read_csv("./src/format_string_table.csv")
        self.version_string_table = read_csv("./src/version_string_table.csv")
        


    def place_finder_patterns(self, 
                              left_top:LeftTopFinderPattern,
                              right_top:RightTopFinderPattern,
                              left_bottom:LeftBottomFinderPattern):
        self.matrix[0:8, 0:8] = left_top.matrix
        self.matrix[0:8, self.size - 8:self.size] = right_top.matrix
        self.matrix[self.size - 8:self.size, 0:8] = left_bottom.matrix

        self.reserved[0:8, 0:8] = True
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
        direction_up = True
        bit_index = 0
        
        while col >= 0 and bit_index < len(self.bits):
            if not self.reserved[row][col]:
                self.matrix[row][col] = int(self.bits[bit_index])
                bit_index += 1
            
            if direction_up:
                if row > 0:
                    row -= 1
                else:
                    col -= 1
                    direction_up = False
            else:
                if row < self.size - 1:
                    row += 1
                else:
                    col -= 1
                    direction_up = True
                    
            if col == 6:
                col -= 1

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
        self.place_finder_patterns(LeftTopFinderPattern(),
                                   RightTopFinderPattern(),
                                   LeftBottomFinderPattern())
        self.place_alignment_patterns(AlignmentPattern())
        self.place_timing_patterns()
        self.place_dark_module()
        self.toggle_reserve_format_area(True)
        if self.version >= 7:
            self.toggle_reserve_version_area(True)
        self.place_bits()
        masking = Masking(self.matrix,self.size,self.reserved)
        mask_pattern = masking.evaluate_mask()
        masking.apply_mask(mask_pattern)

        
        display_matrix = 1 - np.where(self.matrix == None, 0, self.matrix).astype(int)

        plt.figure(figsize=(8, 8))
        plt.imshow(display_matrix, cmap='gray', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.show()


