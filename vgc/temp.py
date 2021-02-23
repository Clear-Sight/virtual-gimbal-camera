import buffer

buf = buffer.Buffer()
lst = [0,1,2,3]
assert buf == []

for i in range(4):
    buf.push(i)

assert buf == lst

for _ in range(len(buf)):
    buf.pop()
assert buf == []
