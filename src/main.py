import pygame
from chapter import Chapter
from entity import Entity
from text import Text
from player import Player


DIALOGUE_POS: tuple = (40, 640)
NAME_POS: tuple = (40, 600)


class App:
    def __init__(self) -> None:
        pygame.init()

        # region Variables
        pygame.display.set_caption("Fairy Idle")
        self.screen: pygame.Surface = pygame.display.set_mode((1280, 720))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.fonts: dict = dict()
        self.fonts[("Times New Roman", 28)] = pygame.font.SysFont("Times New Roman", 28)

        self.chapter: Chapter
        self.chapter_events: list = list()
        self.event_index: int = 0
        self.rendered_characters: dict = dict()
        self.rendered_names: dict = dict()
        self.rendered_dialogue: list = list()
        self.current_dialogue: Text

        self.player = Player("Sacred")
        # endregion

        self.load_chapter("00 - Tutorial")

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        App.quit()
                    case pygame.KEYDOWN:
                        self.keydown_callback(event)
                    case pygame.KEYUP:
                        self.keyup_callback(event)
                    case pygame.MOUSEBUTTONDOWN:
                        self.mousebuttondown_callback(event)

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        for name in self.rendered_names.values():
            name.draw(self.screen)
        for character in self.rendered_characters.values():
            character.draw(self.screen)
        self.current_dialogue.draw(self.screen)

    def load_chapter(self, chapter_name) -> None:
        self.chapter = Chapter(chapter_name)
        self.render_characters()
        self.render_dialogue()
        self.progress_chapter()

    def render_characters(self) -> None:
        self.rendered_characters.clear()
        for character in self.chapter.characters:
            if character in self.rendered_characters:
                continue
            character_appearance = self.chapter.characters[character]["Appearance"]
            self.rendered_characters[character] = Entity((0, 0), character_appearance, width=512, height=512)
            self.rendered_characters[character].visible = False
            name_text = character[:character.find("(") - 1] if character.find("(") != -1 else character
            name_font = self.fonts[("Times New Roman", 28)]
            name_color = (255, 255, 0)
            self.rendered_names[character] = Text(NAME_POS, name_font, name_text, name_color, border=True)
            self.rendered_names[character].visible = False

    def render_dialogue(self) -> None:
        self.chapter_events.clear()
        self.rendered_dialogue.clear()
        for line in self.chapter.dialogue:
            words = line.split()
            match words[0]:
                case "Enter":
                    if "\"" in words[1]:
                        words = " ".join(words[1:])
                        start = words.find("\"")
                        end = words.find("\"", start + 1)
                        character, x, y = words[start + 1:end], *words[end + 1:].strip().split()
                        x, y = x[1:-1], y[:-1]
                    else:
                        character, x, y = words[1], words[2][1:-1], words[3][:-1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.enter_event, character, x, y))
                case "Replace":
                    if "\"" in words[1] or "\"" in words[3]:
                        words = " ".join(words[1:])
                        old_character, new_character = str(), str()
                        while "\"" in words:
                            start = words.find("\"")
                            end = words.find("\"", start + 1)
                            character = words[start + 1:end]
                            words = words[end + 1:]
                            if len(old_character) == 0:
                                old_character = character
                            else:
                                new_character = character
                        if len(words) > 0:
                            new_character = words.split()[-1]
                    else:
                        old_character, new_character = words[1], words[3]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.rendered_characters[new_character].pos = self.rendered_characters[old_character].pos
                    self.rendered_characters[new_character].visible = False
                    self.chapter_events.append((self.replace_event, old_character, new_character))
                case "Exit":
                    if "\"" in words[1]:
                        start = words[1].find("\"")
                        end = words[1].find("\"", start + 1)
                        character = words[1][start + 1:end]
                    else:
                        character = words[1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.exit_event, character))
                case _:
                    dialogue_font = self.fonts[("Times New Roman", 28)]
                    character, dialogue = line.split(": ")
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.show_name_event, character))
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.focus_event, character))
                    dialogue_color = (255, 255, 0)
                    rendered_line = Text(DIALOGUE_POS, dialogue_font, dialogue, dialogue_color, width=1200, border=True)
                    self.rendered_dialogue.append(rendered_line)
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.unfocus_event, character))

    def progress_chapter(self) -> None:
        while isinstance(self.rendered_dialogue[self.event_index], int):
            command, *args = self.chapter_events[self.rendered_dialogue[self.event_index]]
            command(*args)
            self.event_index += 1
            self.event_index %= len(self.rendered_dialogue)
        self.current_dialogue = self.rendered_dialogue[self.event_index]
        self.format_dialogue()
        self.current_dialogue.visible = True
        self.event_index += 1
        self.event_index %= len(self.rendered_dialogue)

    def format_dialogue(self) -> None:
        if "{" not in self.current_dialogue.text:
            return
        text = self.current_dialogue.text
        start = text.find("{")
        end = text.find("}")
        text = f"{text[:start]}{eval(text[start + 1:end])}{text[end + 1:]}"
        self.current_dialogue.render_text(text)

    # region Dialogue Event Methods
    def show_name_event(self, character) -> None:
        if self.rendered_names[character].visible:
            return
        for name in self.rendered_names:
            self.rendered_names[name].visible = False
        self.rendered_names[character].visible = True

    def focus_event(self, character) -> None:
        self.rendered_characters[character].focused = True

    def unfocus_event(self, character) -> None:
        self.rendered_characters[character].focused = False

    def enter_event(self, character, x, y) -> None:
        self.rendered_characters[character].pos = (int(x), int(y))
        self.rendered_characters[character].visible = True

    def replace_event(self, old_character, new_character) -> None:
        self.rendered_characters[new_character].pos = self.rendered_characters[old_character].pos
        self.rendered_characters[new_character].visible = True
        self.rendered_characters[old_character].visible = False

    def exit_event(self, character) -> None:
        self.rendered_characters[character].visible = False
    # endregion

    # region Callback Methods
    def keydown_callback(self, event) -> None:
        match event.key:
            case pygame.K_ESCAPE:
                App.quit()
            case pygame.K_e:
                self.current_dialogue.visible = False

    def keyup_callback(self, event) -> None:
        match event.key:
            case pygame.K_e:
                self.current_dialogue.visible = True

    def mousebuttondown_callback(self, event) -> None:
        self.progress_chapter()
    # endregion

    @staticmethod
    def quit() -> None:
        pygame.quit()
        quit()


if __name__ == "__main__":
    App()
