from encode import Encoder
from bit_stream import BitStreamSender
from reed_solomon import ReedSolomon
from error_correction import ErrorCorrector
from qr_rendering import QRCodeEncoder
import re

def is_kanji_compatible(s: str) -> bool:
    try:
        sjis_encoded = s.encode("shift_jis")
    except UnicodeEncodeError:
        return False

    i = 0
    while i < len(sjis_encoded):
        if i + 1 >= len(sjis_encoded):
            return False
        byte1 = sjis_encoded[i]
        byte2 = sjis_encoded[i + 1]
        pair = (byte1 << 8) | byte2
        if not ((0x8140 <= pair <= 0x9FFC) or (0xE040 <= pair <= 0xEBBF)):
            return False
        i += 2
    return True


def detect_mode(msg: str) -> str:
    if msg.isdigit():
        return "numeric"

    if re.fullmatch(r'[0-9A-Z $%*+\-./:]+', msg):
        return "alphanumeric"

    if is_kanji_compatible(msg):
        return "kanji"

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
