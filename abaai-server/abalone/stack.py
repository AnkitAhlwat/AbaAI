class Stack:
    def __init__(self, initial_items=None):
        if initial_items is None:
            self._items = []
        else:
            self._items = initial_items

    @property
    def items(self):
        return self._items

    def is_empty(self):
        return self._items == []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
        else:
            print("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self._items[-1]
        else:
            print("Stack is empty")

    def clear_stack(self):
        self._items = []

    def size(self):
        return len(self._items)

    def to_json(self):
        return [item.to_json() for item in self._items]
