class Buffer:
    """docstring for Buffer."""

    def __init__(self):
        self._buffer = []

    def push(self, item):
        """ add to buffer  """
        self._buffer.append(item)

    def pop(self):
        """ remove from buffer and return """
        val = self._buffer[0]
        self._buffer = self._buffer[1::]
        return val

    def __len__(self):
        return len(self._buffer)

    def __repr__(self):
        return self._buffer

    def __str__(self):
        return f"{self._buffer}"

    def __eq__(self, other):
        return self._buffer == other
