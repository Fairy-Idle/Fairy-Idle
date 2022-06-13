class Chapter:
    def __init__(self, name) -> None:
        self.name: str = name
        self.progress: int = int()
        self.setting: str = str()
        self.characters: dict = self.load_characters()
        self.dialogue: list = self.load_dialogue()

    def load_characters(self) -> dict:
        characters = dict()
        with open(f"chapters/{self.name}/characters.txt") as characters_txt:
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
        dialogue = list()
        with open(f"chapters/{self.name}/dialogue.txt") as dialogue_txt:
            lines = dialogue_txt.read().split("\n")
            for line in lines:
                dialogue.append(line)
        return dialogue
