from src.encode import Encoder
from pytest import fixture

@fixture
def encoder() -> Encoder:
    encoder = Encoder()
    return encoder

def test_kanji_encoder_returns_bytes(encoder:Encoder) -> None:
    string = "茗荷"
    assert encoder.kanji_encode(string) !=None

