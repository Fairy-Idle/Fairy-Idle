from src.chapter import Chapter
import unittest


class TestChapterMethods(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.chapter_0 = Chapter("00 - Tutorial")

    def test_load_characters(self) -> None:
        characters = {
            "??? (Rial)": {
                "Appearance": "images/rial_mask.png",
                "Color": "(255, 255, 0)"
            },
            "Rial": {
                "Appearance": "images/rial.png",
                "Color": "(255, 255, 0)"
            },
            "??? (Viol)": {
                "Appearance": "images/viol.png",
                "Color": "(143, 0, 255)"
            }
        }
        self.assertEqual(self.chapter_0.characters, characters)

    def test_load_dialogue(self) -> None:
        dialogue = [
            "Enter \"??? (Rial)\" (40, 200)",
            "??? (Rial): Hello {self.player.name}, and welcome to Fairy Idle!",
            "??? (Rial): My name is Rial and I'll be your guide!",
            "Replace \"??? (Rial)\" with \"Rial\"",
            "Rial: I hope you rested well, the journey was a *bit* bumpy.",
            "Enter \"??? (Viol)\" (740, 200)",
            "??? (Viol): Yeah, I was honestly surprised you didn't wake up halfway through...",
            "setattr(self, \"vn_pos\", (0, -100))",
            "Rial: Test!",
            "Exit \"??? (Viol)\"",
            "Exit \"Rial\"",
            "setattr(self, \"vn_pos\", (0, 0))"
        ]
        self.assertEqual(self.chapter_0.dialogue, dialogue)
