from pytest import fixture, raises
from src.bit_stream import BitStreamSender
from src.encode import Encoder

@fixture
def bit_stream() -> BitStreamSender:
    bit_stream = BitStreamSender()
    return bit_stream

@fixture
def encoder() -> Encoder:
    encoder = Encoder()
    return encoder

def test_bytes_output_stream_is_correct(bit_stream: BitStreamSender, encoder: Encoder) -> None:
    expected_output = "0100 0000000000001011 01001000 01100101 01101100 01101100 01101111 01110111 01101111 01110010 01101100 01100100 00100001 0000"
    r = encoder.bytes("Hello world!")
    assert expected_output == bit_stream.send_bit_stream(r[2],r[0],r[1])

def test_bytes_invalid_character_count(bit_stream: BitStreamSender, encoder: Encoder) -> None:# for coverage purposes
    r = encoder.bytes("Hello world!")
    with raises(ValueError):
        bit_stream.send_bit_stream()

def test_alphanumeric_output_is_correct(bit_stream: BitStreamSender, encoder: Encoder) -> None:
    expected_output = "0010 00000001010 01100001011 01111000110 10001011000 10001010011 01110111110 0000"
    r = encoder.alphanumeric("HELLO WORLD")
    assert expected_output == bit_stream.send_bit_stream(r[2], r[0], r[1])

def test_alphanumeric_invalid_character_count(bit_stream: BitStreamSender, encoder: Encoder) -> None:# for coverage purposes
    r = encoder.alphanumeric("HELLO WORLD")
    with raises(ValueError):
        bit_stream.send_bit_stream(r[2],-1,r[1])

def test_numeric_output_is_correct(bit_stream: BitStreamSender, encoder: Encoder) -> None:
    expected_output = "0001 000000001101 110010101010 101110100110 10011101111101 0000"
    r = encoder.numeric("3242 2982 10109")
    assert expected_output == bit_stream.send_bit_stream(r[2], r[0], r[1])

def test_numeric_invalid_character_count(bit_stream: BitStreamSender, encoder: Encoder) -> None:# for coverage purposes
    r = encoder.alphanumeric("3242 2982 10109")
    with raises(ValueError):
        bit_stream.send_bit_stream(r[2],-1,r[1])

def test_kanji_output_is_correct(bit_stream: BitStreamSender, encoder: Encoder) -> None:
    excepted_output = "1000 00000010 01001010101100100101010111 0000"
    r = encoder.kanji("獄 漉")
    assert excepted_output == bit_stream.send_bit_stream(r[2], r[0], r[1])

def test_kanji_invalid_character_count(bit_stream: BitStreamSender, encoder: Encoder) -> None:# for coverage purposes
    r = encoder.kanji("獄 漉")
    with raises(ValueError):
        bit_stream.send_bit_stream(r[2],-1,r[1])