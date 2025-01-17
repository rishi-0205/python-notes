from hello import hello

def test_arguement():
    assert hello("david") == "hello, david"

def test_default():
    assert hello() == "hello, world"