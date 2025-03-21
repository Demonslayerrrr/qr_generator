import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

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
    def __init__(self, version):
        self.version = version
        self.size = 4 * version + 17
        self.matrix = np.full((self.size, self.size), None) 
        self.reserved = np.zeros((self.size, self.size), dtype=bool)

    def place_finder_patterns(self,pattern: FinderPattern):
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
            if not self.is_reserved(i, 6):
                self.matrix[i, 6] = not (i % 2)

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
        row, col =4 * self.version + 9, 8 
        self.matrix[row, col] = 1
        self.reserved[row, col] = True

    def reserve_format_area(self):
        
        self.matrix[8,0] =1

    def reserve_version_area(self):
        pass

    def visualize(self):
        display_matrix = 1 - np.where(self.matrix == None, 0, self.matrix).astype(int)

        plt.figure(figsize=(8, 8))
        plt.imshow(display_matrix, cmap='gray', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.show()

qr = QRCodeEncoder(7) 
qr.place_finder_patterns(FinderPattern())
qr.place_alignment_patterns(AlignmentPattern())
qr.place_timing_patterns()
qr.place_dark_module()
qr.reserve_format_area()
qr.visualize()