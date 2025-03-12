class Encoder:
    def __init__(self):
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

    def alphanumeric_encode(self,s:str) -> str:
        l = []
        s = s.replace(" ","")
        for i in range(0,len(s),2):
            l.append(s[i:i+2])

        results = []
        single_element = None


        if len(l[-1]) % 2 !=0:
            single_element = format(self._ALPHANUMERIC_TABLE[l.pop()],'06b')

        
        for pair in l:
            results.append(format(self._ALPHANUMERIC_TABLE[pair[0]]*self._ALPHANUMERIC_MULTIPLIER + self._ALPHANUMERIC_TABLE[pair[1]], '011b'))

        if single_element:
            results.append(single_element)

        output = ""
        for binary in results:
            output+=" "+ binary

        return output.strip()

    def kanji_encode(self,s:str) -> str:
        s = s.encode("shift_jis").hex()
        l_with_input_hex = []
        for i in range(0,len(s),4):
            l_with_input_hex.append(s[i:i+4])

        result = []
        for string in l_with_input_hex:
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

        return output 


encoder = Encoder()

print(encoder.alphanumeric_encode("HELLO WOORLD"))