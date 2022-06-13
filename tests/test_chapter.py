from src.chapter import Chapter
import unittest


class TestChapterMethods(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.chapter_0 = Chapter("00 - Tutorial")

    def test_load_characters(self) -> None:
        characters = {
            "??? (Rial)": {
                "Appearance": "images/rial_mask_2.png"
            },
            "Rial": {
                "Appearance": "images/rial.png"
            }
        }
        self.assertEqual(self.chapter_0.characters, characters)

    def test_load_dialogue(self) -> None:
        dialogue = [
            "??? (Rial): Hello, {self.player.name}, and welcome to Fairy Idle!",
            "??? (Rial): My name is Rial and I'll be your guide!",
            "Rial: I hope you rested well, the journey was a *bit* bumpy."
        ]
        self.assertEqual(self.chapter_0.dialogue, dialogue)
