class Chapter:
    def __init__(self, name) -> None:
        self.name: str = name
        self.progress: int = int()
        self.setting: str = str()
        self.characters: dict = self.load_characters()
        self.dialogue: dict = self.load_dialogue()

    def load_characters(self) -> dict:
        characters = dict()
        with open(f"Chapters/{self.name}/Characters.txt") as characters_txt:
            lines = characters_txt.read().split("\n")
            for line in lines:
                if " " * 4 not in line:
                    character = line[:-1]
                    characters[character] = dict()
                    continue
                attribute, value = line.strip().split(": ")
                characters[character][attribute] = value
        return characters

    def load_dialogue(self) -> dict:
        dialogue = dict()
        with open(f"Chapters/{self.name}/Dialogue.txt") as dialogue_txt:
            lines = dialogue_txt.read().split("\n")
            for line in lines:
                character, dialogue_line = line.split(": ")
                if character not in dialogue:
                    dialogue[character] = list()
                dialogue[character].append(dialogue_line)
        return dialogue
