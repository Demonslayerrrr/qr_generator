import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from dataclasses import dataclass
from pandas import read_csv
from masking import Masking
from matplotlib import use
use('TkAgg')
from PIL import Image

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

        self.format_string_table = read_csv("qr_format_strings_v1_to_v40.csv")

        self.version_info=''
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
                self.reserved[i, 8] = bool_state
                self.reserved[8, i] = bool_state

        for i in range(8):
            self.reserved[self.size - 1 - i, 8] = bool_state
            self.reserved[8, self.size - 1 - i] = bool_state

    def toggle_reserve_version_area(self, bool_state:bool):
        self.reserved[0:6, self.size - 11:self.size - 8] = bool_state
        self.reserved[self.size - 11:self.size - 8, 0:6] = bool_state

    def place_bits(self):
        row, col = self.size - 1, self.size - 1
        direction_up = True
        bit_index = 0
        going_left = True

        while col >= 0 and bit_index < len(self.bits):
            if col == 6:
                col -= 1
                continue

            if not self.reserved[row, col]:
                self.matrix[row, col] = int(self.bits[bit_index])
                bit_index += 1

            if going_left:
                col -= 1
                going_left = False
            else:
                col += 1
                going_left = True

                if direction_up:
                    if row > 0:
                        row -= 1
                    else:
                        col -= 2
                        direction_up = False
                else:
                    if row < self.size - 1:
                        row += 1
                    else:
                        col -= 2
                        direction_up = True

    def place_format_string(self, mask_pattern: int):
        self.toggle_reserve_format_area(False)

        format_string = self.format_string_table[
            (self.format_string_table["Mask Pattern"] == mask_pattern) &
            (self.format_string_table["ECC Level"] == self.error_correction_level)
            ]["Format String"].values[0]
        format_string = str(format_string).zfill(15)
        bits = [int(b) for b in format_string]
        bit_index = 0
        for i in range(9):
            if i != 6:
                if not self.is_reserved(8, i):
                    self.matrix[8, i] = bits[bit_index]
                    self.reserved[8, i] = True
                    bit_index += 1

        for i in range(8, -1, -1):
            if i != 6:
                if not self.is_reserved(i, 8):
                    self.matrix[i, 8] = bits[bit_index]
                    self.reserved[i, 8] = True
                    bit_index += 1

        bit_index = 0
        for i in range(7):
            if not self.is_reserved(self.size - 1 - i, 8):
                self.matrix[self.size - 1 - i, 8] = bits[bit_index]
                self.reserved[self.size - 1 - i, 8] = True
                bit_index += 1

        temp_list = list(reversed(bits[7:15]))
        temp_index = 0
        for i in range(8):
            if not self.is_reserved(8, self.size - 1 - i):
                self.matrix[8, self.size - 1 - i] = temp_list[temp_index]
                self.reserved[8, self.size - 1 - i] = True
                temp_index += 1

    def place_version_string(self):
        self.toggle_reserve_version_area(False)

        G = 0b1111100100101

        version_bits = self.version << 12

        for i in range(17, 11, -1):
            if (version_bits >> i) & 1:
                version_bits ^= G << (i - 12)

        remainder = version_bits & 0b111111111111

        self.version_info = (self.version << 12) | remainder
        print(self.version_info)

        bit_index = 0
        for col in range(6):
            for row in range(3):
                bit_value = (self.version_info >> bit_index) & 1
                matrix_row = self.size - 11 + row
                matrix_col = col

                self.matrix[matrix_row, matrix_col] = bit_value
                self.reserved[matrix_row, matrix_col] = True
                bit_index += 1
        bit_index = 0
        for col in range(3):
            for row in range(6):
                bit_value = (self.version_info >> bit_index) & 1
                matrix_row = row
                matrix_col = self.size - 11 + col

                self.matrix[matrix_row, matrix_col] = bit_value
                self.reserved[matrix_row, matrix_col] = True
                bit_index += 1


    def visualize(self,color:str, style:str, image:bool):
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
        masking.apply_mask(mask_pattern, self.matrix)

        self.place_format_string(mask_pattern)

        if self.version >= 7:
            self.place_version_string()

        cmap = mcolors.ListedColormap(['white',color])

        display_matrix = np.where(self.matrix == None, 0, self.matrix).astype(int)

        match style:
            case "dots":
                fig, ax = plt.subplots()
                ax.set_aspect('equal')
                ax.axis('off')

                cell_size = 10
                dot_radius = cell_size * 0.45
                bg_radius = cell_size * 0.5

                for y in range(self.size):
                    for x in range(self.size):
                        center_x = x * cell_size + cell_size / 2
                        center_y = y * cell_size + cell_size / 2

                        bg = plt.Circle((center_x, center_y), bg_radius, color='white', zorder=1)
                        ax.add_artist(bg)

                        if display_matrix[y][x]:
                            fg = plt.Circle((center_x, center_y), dot_radius, color=color, zorder=2)
                            ax.add_artist(fg)

                ax.set_xlim(0, self.size * cell_size)
                ax.set_ylim(self.size * cell_size, 0)
                plt.show()

            case "squares":
                plt.figure(figsize=(8, 8))
                plt.imshow(display_matrix, cmap=cmap, interpolation='nearest')
                plt.xticks([])
                plt.yticks([])
                if not image:
                    plt.show()
                else:
                    plt.savefig("qr.png",dpi=300, bbox_inches="tight")
                    qr_img = Image.open("qr.png").convert("RGB")
                    logo = Image.open("coca-cola.png")

                    qr_width, qr_height = qr_img.size
                    logo_size = int(qr_width * 0.25)
                    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

                    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

                    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

                    qr_img.show()

