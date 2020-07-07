class Deque:
    def __init__(self, initial_contents, max_size):
       self.content = initial_contents or []
       self.max_size = max_size

    def __iter__(self):
        return iter(self.content)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        if index + 1 > self.__len__():
            raise IndexError

        return self.content[index]

    def append(self, value):
        self.content.append(value)
        if len(self.content) > self.max_size:
            self.content = self.content[1:]
