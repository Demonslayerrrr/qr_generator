unicode_string = "茗荷"

class Encoder:
    def __init__(self):
        self._RANGES_KANJI= {(0x8140, 0x9FFC):0x8140, (0xE040, 0xEBBF):0xC140}
    def kanji_encode(self,s:str) -> bytes:
        s = s.encode("shift_jis").hex()
        l = []
        for i in range(0,len(s),4):
            l.append(s[i:i+4])
        return

        # for k,v in RANGES_KANJI.items():
        #     if int(a,16)>k[0] and int(a,16)<k[1]:
        #         result = int(a,16)- v

        # print(hex(result))

encoder = Encoder()

print(encoder.kanji_encode(unicode_string))