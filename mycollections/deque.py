class Deque:
    def __init__(self, initial_contents, max_size):
       self.content = initial_contents or []
       self.max_size = max_size

    def __iter__(self):
        return self.content.__iter__()

    def __len__(self):
        return len(self.content)

    def append(self, value):
        self.content.append(value)
        if len(self.content) > self.max_size:
            self.content = self.content[1:]
