unicode_string = "茗荷"

class Encoder:
    def __init__(self):
        self._RANGES_KANJI= {(0x8140, 0x9FFC):0x8140, (0xE040, 0xEBBF):0xC140}
    def kanji_encode(self,s:str) -> bytes:
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

        print(list_with_new_hex)
        most_least_significant_bytes = []

        for x in list_with_new_hex:
            most_least_significant_bytes.append((f'0x{x[2:4]}',f'0x{x[4:6]}'))

        print(most_least_significant_bytes)
        output = []

        for y in most_least_significant_bytes:
            byte_value = ((int(y[0], 16) * 0xC0) + int(y[1], 16)) % 256
            output.append(f'{byte_value:08b}')

        return output 

encoder = Encoder()

print(encoder.kanji_encode(unicode_string))