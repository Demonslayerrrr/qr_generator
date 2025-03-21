class BitStreamSender:
    def __init__(self) -> None:
        self.indicators: dict = {
            "numeric": "0001",
            "alphanumeric": "0010",
            "byte": "0100",
            "kanji": "1000"
        }
        self.character_count_indicator_table: dict = {
            range(1, 9): {"numeric": 10, "alphanumeric": 9, "byte": 8, "kanji": 8},
            range(10, 27): {"numeric": 12, "alphanumeric": 11, "byte": 16, "kanji": 10},
            range(27, 41): {"numeric": 14, "alphanumeric": 13, "byte": 16, "kanji": 12}
        }
        self.terminator = "0000"
    
    def send_bit_stream(self, mode: str, character_count: int, encoded: str) -> str:
        bytes_number_for_character_count = None
        for k, v in self.character_count_indicator_table.items():
            if character_count in k:  
                bytes_number_for_character_count = v[mode]


        if bytes_number_for_character_count is None:
            raise ValueError()
        
        
        return self.indicators[mode] + " " + format(character_count, f"0{bytes_number_for_character_count}b") + " " + encoded + " " + self.terminator
    

# print(BitStreamSender().send_bit_stream('byte',11, '01001000 01100101 01101100 01101100 01101111 01110111 01101111 01110010 01101100 01100100 00100001'))