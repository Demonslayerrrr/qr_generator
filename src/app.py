from encode import Encoder
from bit_stream import BitStreamSender
from reed_solomon import ReedSolomon
from error_correction import ErrorCorrector
from qr_rendering import QRCodeEncoder


if __name__ == "__main__":
    message_and_mode = input("Message,mode: ").split(" ")

    message,mode = "".join(message_and_mode[0:-1]), message_and_mode[-1]
    version= input("Version(for example 5 L): ").split(" ")
    version_number,error_correction_level = version[0], version[1]
    print("".join(message))
    encoder = Encoder() 
    char_count,encoded_message,mode = getattr(encoder,mode)(message)

    bit_stream_sender = BitStreamSender()

    bit_stream = bit_stream_sender.send_bit_stream(mode,char_count,encoded_message)

    reed_solomon = ReedSolomon()
    error_corrector = ErrorCorrector(bit_stream,int(version_number), error_correction_level)

    interleave_blocks = error_corrector.generate_interleave_blocks()
    print(interleave_blocks)
    qr_renderer = QRCodeEncoder()