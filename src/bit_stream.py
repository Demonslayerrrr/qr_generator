from encode import Encoder

class BitStreamSender:
    def __init__(self):
        self.indicators: dict = {"numeric":"0001",
                            "alphanumeric":"0010",
                            "byte": "0100",
                            "kanji": "1000"}
        self.character_count_indicator_table: dict[range:dict] = {range(1,9):{"numeric":10,"alphanumeric":9,"byte":8,"kanji":8},
                                                             range(10-26):{"numeric":12,"alphanumeric":11,"byte":16,"kanji":10},
                                                             range(27-40):{"numeric":14,"alphanumeric":13,"byte":16,"kanji":12}}

        self.terminator = "0000"
    
    def send_bit_stream(self, mode:str, character_count:int, encoded:str):
        return self.indicators[mode]+ " " + format(character_count,"09b") + " " + encoded + " " + self.terminator
    

a = BitStreamSender()
b = Encoder()

result = b.bytes_encode("HEllo world!")

print(a.send_bit_stream(result[2], result[0], result[1]))