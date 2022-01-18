import json

from Node import Node
from controller.spotify.Controlify import start_playback, pause_playback, next_track, previous_track


class Translator:

    def __init__(self):
        self.tree = self.create_tree()

    def create_tree(self):
        root = Node('')
        with open('C:/Users/Benno/PycharmProjects/Controlify/config/translator_config.json') as translator_config:
            data = json.load(translator_config)
            self.recursive(root, data)
        return root

    def recursive(self, node, data):
        for data_point in data:
            if data_point != 'command':
                if 'command' in data[data_point]:
                    new_node = Node(data_point, data[data_point]['command'])
                    self.recursive(new_node, data[data_point])
                    node.child.append(new_node)

    def evaluate_text(self, text):
        if text is not None and text != '':
            evaluation_tree = None
            for word in text.split(' '):
                if evaluation_tree is None:
                    evaluation_tree = self.tree.get_child(word)
                else:
                    evaluation_tree = evaluation_tree.get_child(word)
                if evaluation_tree is None:
                    return
            try:
                eval(evaluation_tree.get_command())
            except NameError:
                print(f"The configured command: {evaluation_tree.get_command()} in 'translator_config.json' is not imported")


if __name__ == '__main__':
    translator = Translator()
    translator.evaluate_text("stop music")