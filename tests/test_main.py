import pytest
import vgc

def test_setup():
    pass

def test_buffer():
    """ test for type Buffer """
    buf = vgc.buffer.Buffer()
    lst = [0,1,2,3]
    assert buf == []

    for i in range(3):
        buf.push(i)
    assert buf == lst

    for _ in range(len(buf)):
        buf.pop()
    assert buf == []
