MAXIMUM_STACK_SIZE = 1024

# You define a class using the class keyword and initialize its attributes with the special __init__() method. The self parameter represents the instance of the class.


class Stack:
    def __init__(self):
        self.items = []

    def __str__(self):
        ws = []
        for i, item in enumerate(self.items[::-1]):
            if i == 0:
                ws.append(f"{item} <first")
            elif i == len(self.items) - 1:
                ws.append(f"{item} <last")
            else:
                ws.append(str(item))
        return "\n".join(ws)

    def push(self, value):
        if len(self.items) == MAXIMUM_STACK_SIZE - 1:
            raise Exception("Stack overflow")
        self.items.append(value)

    def pop(self):
        if len(self.items) == 0:
            raise Exception("Stack underflow")
        return self.items.pop()

    @property
    def stack(self):
        return self.items.copy()


kayakys_stack = Stack()
kayakys_stack.push(1)
kayakys_stack.push(2)
kayakys_stack.push(3)
print(kayakys_stack)
