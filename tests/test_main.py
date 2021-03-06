import pytest
import vgc


def test_setup():
    assert 1 + 1 == 2

def test_buffer():
    """ test for type Buffer implementation """
    buf = vgc.buffer.Buffer()
    lst = [0,1,2,3]
    assert buf == []

    for i in range(4):
        buf.push(i)
    assert buf == lst

    for _ in range(len(buf)):
        buf.pop()
    assert buf == []

    for i in range(4):
        buf += [i]
    assert buf == lst

    for _ in range(len(buf)):
        buf.pop()
    assert buf == []
