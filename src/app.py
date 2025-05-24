from encode import Encoder
from bit_stream import BitStreamSender
from reed_solomon import ReedSolomon
from error_correction import ErrorCorrector
from qr_rendering import QRCodeEncoder
import re


def detect_mode(msg: str) -> str:
    if msg.isdigit():
        return "numeric"
    
    if re.fullmatch(r'[0-9A-Z $%*+\-./:]+', msg):
        return "alphanumeric"
    
    return "bytes"

if __name__ == "__main__":
    message = input("Message: ").strip()

    mode = detect_mode(message)

    print(mode)
    encoder = Encoder() 
    char_count,encoded_message,mode = getattr(encoder,mode)(message)

    bit_stream_sender = BitStreamSender(char_count,encoded_message,mode)

    bit_stream = bit_stream_sender.build_bit_stream()

    print(bit_stream,len(bit_stream))
    reed_solomon = ReedSolomon()
    error_corrector = ErrorCorrector(bit_stream,bit_stream_sender.version,bit_stream_sender.ec_level)

    interleave_blocks = error_corrector.generate_interleave_blocks()


    qr_renderer = QRCodeEncoder(bit_stream_sender.version,bit_stream_sender.ec_level,interleave_blocks)

    qr_renderer.visualize()
