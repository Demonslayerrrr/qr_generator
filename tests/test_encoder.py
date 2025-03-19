from src.encode import Encoder
from pytest import fixture

@fixture
def encoder() -> Encoder:
    encoder = Encoder()
    return encoder

def test_numeric_encoder_returns_binary(encoder:Encoder) -> None:
    string = "867 530 9"
    assert all(i in '01' for i in encoder.numeric(string)[1].replace(" ",""))

def test_numeric_encoder_output_is_correct(encoder:Encoder) -> None:
    string = "867 530 9"
    assert encoder.numeric(string)[1] == "1101100011 1000010010 1001"

def test_alphanumeric_encoder_returns_binary(encoder:Encoder) -> None:
    string = "HELLO WORLD"
    assert all(i in '01' for i in encoder.alphanumeric(string)[1].replace(" ", ""))

def test_alphanumeric_encoder_output_is_correct_when_character_number_is_even(encoder:Encoder) -> None:
    string = "HELLO WORLD"
    assert encoder.alphanumeric(string)[1] == '01100001011 01111000110 10001011000 10001010011 01110111110'

def test_alphanumeric_encoder_output_is_correct_when_character_number_is_odd(encoder:Encoder) -> None:
    string = "HELLO WOORLD"
    assert encoder.alphanumeric(string)[1] == '01100001011 01111000110 10001011000 10001010000 10011010100 001101'

def test_kanji_encoder_returns_binary(encoder:Encoder) -> None:
    string = "茗荷"
    assert all(i in '01' for i in encoder.kanji(string)[1])

def test_kanji_encoder_output_is_correct(encoder:Encoder) -> None:
    string = "茗 荷"
    assert encoder.kanji(string)[1] == '11010101010100011010010111'