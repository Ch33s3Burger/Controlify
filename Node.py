class Node:

    def __init__(self, word, command=None):
        self.word = word
        self.command = command

        self.child = []

    def get_command(self):
        return self.command

    def get_child(self, next_word):
        return next((x for x in self.child if x.word == next_word), None)