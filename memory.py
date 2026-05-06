class SimpleMemory:
    # The __init__ dunder is the constructor method to initialize new objects of the class, in this case, empty items list.

    def __init__(self):
        self.memory = []

    def access(self, offset, size):
        return self.memory[offset : offset + size]

    def load(self, offset):
        return self.access(offset, 32)

    def store(self, offset, value):
        self.memory[offset : offset + len(value)] = value


# mem = SimpleMemory()
# mem.memory = [0, 0, 0, 10, 20, 30, 0, 0]

# mem.load(3)  # reads 32 bytes starting at address 3
# mem.access(3, 3)  # reads exactly 3 bytes → [10, 20, 30]
# mem.store(3, [99])  # overwrites address 3 with 99
# print(mem.memory)  # memory is now [0, 0, 0, 99, 20, 30, 0, 0]


class Memory(SimpleMemory):
    def store(self, offset, value):
        memory_expansion_cost = 0

        if len(self.memory) <= offset + len(value):

            expansion_size = 0

            # initialize memory with 32 zeros if it is empty
            if len(self.memory) == 0:
                expansion_size = 32
                self.memory = [0x00 for _ in range(32)]

            # extend memory more if needed
            if len(self.memory) < offset + len(value):
                expansion_size += offset + len(value) - len(self.memory)
                self.memory.extend([0x00] * expansion_size)

            memory_expansion_cost = expansion_size**2  # simplified!

        super().store(offset, value)
        return memory_expansion_cost


memory = Memory()
memory.store(0, [0x01, 0x02, 0x03, 0x04])
print(memory.load(0))
