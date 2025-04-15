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
    
    try:
        msg.encode('shift_jis')
        return "kanji"
    except UnicodeEncodeError:
        pass

    return "bytes"

if __name__ == "__main__":
    message = input("Message: ").strip()

    mode = detect_mode(message)

    encoder = Encoder() 
    char_count,encoded_message,mode = getattr(encoder,mode)(message)

    bit_stream_sender = BitStreamSender()

    bit_stream = bit_stream_sender.send_bit_stream(mode,char_count,encoded_message)

    reed_solomon = ReedSolomon()
    error_corrector = ErrorCorrector(bit_stream)

    interleave_blocks = error_corrector.generate_interleave_blocks()

    version_number,error_correction_level = error_corrector.choose_qr_version_and_level()

    qr_renderer = QRCodeEncoder(version_number,error_correction_level,interleave_blocks)

    qr_renderer.visualize()
