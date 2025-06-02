from operator import contains

from encode import Encoder
from bit_stream import BitStreamSender
from reed_solomon import ReedSolomon
from error_correction import ErrorCorrector
from qr_rendering import QRCodeEncoder
import argparse
import re

# https://github.com/GooeyAI/docs/tree/main

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

parser = argparse.ArgumentParser()
parser.add_argument("--v", action="store_true")
parser.add_argument("--color")
parser.add_argument("--style")
parser.add_argument("--image", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    message = input("Message: ").strip()

    mode = detect_mode(message)


    encoder = Encoder() 
    char_count,encoded_message,mode = getattr(encoder,mode)(message)

    bit_stream_sender = BitStreamSender(char_count,encoded_message,mode)

    bit_stream = bit_stream_sender.build_bit_stream()


    reed_solomon = ReedSolomon()
    error_corrector = ErrorCorrector(bit_stream,bit_stream_sender.version,bit_stream_sender.ec_level)

    interleave_blocks = error_corrector.generate_interleave_blocks()


    qr_renderer = QRCodeEncoder(bit_stream_sender.version,bit_stream_sender.ec_level,interleave_blocks)

    qr_renderer.visualize(color = args.color if args.color else "black", style = args.style if args.style else "squares", image = args.image if args.image else False)

    if args.v:
        print("Mode: ",mode)
        print("\n Bit stream: ",bit_stream,len(bit_stream))
        print("\n Version and EC level: ",bit_stream_sender.version,bit_stream_sender.ec_level)
        print("\n Version info string: ", qr_renderer.version_info)

