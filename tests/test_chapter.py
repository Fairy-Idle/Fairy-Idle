from src.chapter import Chapter
import unittest


class TestChapterMethods(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.chapter_0 = Chapter("00 - Tutorial")

    def test_load_characters(self):
        characters = {
            "??? (Rial)": {
                "Appearance": "rial_mask.png"
            },
            "Rial": {
                "Appearance": "rial.png"
            }
        }
        self.assertEqual(self.chapter_0.characters, characters)

    def test_load_dialogue(self):
        dialogue = {
            "??? (Rial)": ["Hello, {self.player.name}, and welcome to Fairy Idle!", "My name is a Rial and I'll be your guide!"],
            "Rial": ["I hope you rested well, the journey was a *bit* bumpy."]
        }
        self.assertEqual(self.chapter_0.dialogue, dialogue)
