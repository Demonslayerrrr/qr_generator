from functools import reduce

class Encoder:
    def __init__(self) -> None:
        self._ALPHANUMERIC_TABLE = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
        'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27,
        'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36,
        '$': 37, '%': 38, '*': 39, '+': 40, '-': 41, '.': 42, '/': 43, ':': 44
        }
        self._ALPHANUMERIC_MULTIPLIER = 45

        self._RANGES_KANJI= {(0x8140, 0x9FFC):0x8140, (0xE040, 0xEBBF):0xC140}
        self._KANJI_MULTIPLIER = 0xC0

    def numeric(self, s: str) -> tuple:
        s = s.replace(" ", "")  # remove all spaces
        character_count = len(s)

        output = ""
        i = 0
        while i < len(s):
            if i + 3 <= len(s):
                group = s[i:i + 3]
                output += format(int(group), "010b")
                i += 3
            elif i + 2 <= len(s):
                group = s[i:i + 2]
                output += format(int(group), "07b")
                i += 2
            else:
                group = s[i]
                output += format(int(group), "04b")
                i += 1

        return character_count, output, "numeric"

    def alphanumeric(self, s: str) -> tuple:
        def encode_pair(pair):
            if len(pair) == 2:
                val = 45 * self._ALPHANUMERIC_TABLE[pair[0]] + self._ALPHANUMERIC_TABLE[pair[1]]
                return format(val, '011b')
            else:
                val = self._ALPHANUMERIC_TABLE[pair[0]]
                return format(val, '06b')

        def split_pairs(s: str):
            pairs = []
            i = 0
            while i < len(s):
                if i + 1 < len(s):
                    pairs.append(s[i] + s[i + 1])
                    i += 2
                else:
                    pairs.append(s[i])
                    i += 1
            return pairs

        character_len = len(s)

        res = reduce(lambda acc, pair: acc + encode_pair(pair), split_pairs(s), '')

        return character_len,res, "alphanumeric"

    def bytes(self, s: str) -> tuple:
        hex_values = [format(ord(i), "08b") for i in s]
        characters_count = len(hex_values)

        output = ""
        for value in hex_values:
            output += " " + value
        return characters_count, output.strip(), "bytes"

    def kanji(self,s:str) -> tuple:
        s = [i.encode("shift_jis").hex() for i in s.split(" ")]

        result = []

        for index, element in enumerate(s):
            if len(element)>4:
                temp_el = s.pop(index)
                for i in range(0, len(element), 4):
                    s.insert(index+i, temp_el[i:i+4])

        character_count = len(s)
        for string in s:
            for k,v in self._RANGES_KANJI.items():
                if int(string,16)>k[0] and int(string,16)<k[1]:
                    result.append(int(string,16)- v)

        list_with_new_hex = list(map(lambda x: f"0x{x:04x}", result))

        most_least_significant_bytes = []

        for x in list_with_new_hex:
            most_least_significant_bytes.append((f'0x{x[2:4]}',f'0x{x[4:6]}'))

        output = ''

        for y in most_least_significant_bytes:
            result_int = ((int(y[0], 16) * self._KANJI_MULTIPLIER  + int(y[1], 16)))
            result_binary = format(result_int,'013b')
            output += result_binary

        return character_count,output,"kanji"