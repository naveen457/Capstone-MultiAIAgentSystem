class MemoryManager:

    def __init__(self):
        self.history = []

    def add(self, item):
        self.history.append(item)

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()
