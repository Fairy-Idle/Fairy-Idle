import pygame
from chapter import Chapter
from entity import Entity
from text import Text
from button import Button
from player import Player


WINDOW_SIZE: tuple[int, int] = (1280, 720)

# region Idle Variables
pass
# endregion

# region VN Variables
SPRITE_SIZE: tuple[int, int] = (512, 512)
DIALOGUE_POS: tuple[int, int] = (40, 640)
DIALOGUE_WIDTH: int = 1200
NAME_POS: tuple[int, int] = (40, 600)
# endregion


class App:
    def __init__(self) -> None:
        pygame.init()

        # region Variables
        pygame.display.set_caption("Fairy Idle")
        self.screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.fonts: dict[tuple[str, int]: pygame.font.SysFont] = dict()
        self.fonts[("Times New Roman", 28)] = pygame.font.SysFont("Times New Roman", 28)

        self.vn_surface: pygame.Surface = pygame.Surface(WINDOW_SIZE)
        self.vn_pos: tuple[int, int] = (0, 0)

        self.idle_surface: pygame.Surface = pygame.Surface(WINDOW_SIZE)
        self.idle_pos: tuple[int, int] = (0, 0)
        self.inventory_pos: tuple[int, int] = (20, 20)

        self.chapter: Chapter = None
        self.chapter_events: list[callable, str] = list()
        self.event_index: int = int()

        self.rendered_characters: dict[str: Entity] = dict()
        self.rendered_names: dict[str: Text] = dict()
        self.rendered_dialogue: list[Text] = list()
        self.current_dialogue: Text = None

        self.vn_surfaces: list[Entity | Text | Button] = list()
        self.inventory_surfaces: list[Entity | Text | Button] = list()
        self.idle_surfaces: list[Entity | Text | Button] = list()

        self.mode: str = str()
        self.player = Player("Sacred")
        # endregion

        # self.load_chapter("00 - Tutorial")
        self.load_idle()

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
        self.vn_surface.fill((0, 0, 0))
        self.idle_surface.fill((0, 0, 0))

        mode_surface, surfaces, pos = self.get_surfaces()
        for surface in surfaces:
            if surface.transitioning:
                surface.transition[0](surface, *surface.transition[1:])
            surface.draw(mode_surface)
        self.screen.blit(mode_surface, pos)

    def get_surfaces(self) -> tuple[pygame.Surface, list[Entity | Text | Button], tuple[int, int]]:
        self.vn_surfaces.clear()
        self.idle_surfaces.clear()
        match self.mode:
            case "vn":
                self.vn_surfaces.extend(self.rendered_names.values())
                self.vn_surfaces.extend(self.rendered_characters.values())
                if self.current_dialogue is not None:
                    self.vn_surfaces.append(self.current_dialogue)
                return self.vn_surface, self.vn_surfaces, self.vn_pos
            case "idle":
                self.idle_surfaces.append(self.inventory)
                self.idle_surfaces.append(self.inventory_button)
                return self.idle_surface, self.idle_surfaces, self.idle_pos

    def load_chapter(self, chapter_name) -> None:
        self.chapter = Chapter(chapter_name)
        self.mode = "vn"
        self.render_characters()
        self.render_dialogue()
        self.progress_chapter()

    def load_idle(self) -> None:
        self.mode = "idle"
        self.inventory: Text = Text(self.inventory_pos, self.fonts[("Times New Roman", 28)], "Inventory", (0, 255, 0), None, width=320, height=680, border=True, justify="center", transition=(self.smooth_translation, (-320, 20), (20, 20)), timer=0.5)
        self.inventory.visible = False
        self.inventory_button: Button = Button((20, 350), self.fonts[("Times New Roman", 28)], ">", color=(0, 255, 0), border=True, active=lambda: [setattr(self.inventory, "visible", True), self.inventory.transition[0](self.inventory, *self.inventory.transition[1:])])

    def render_characters(self) -> None:
        self.rendered_characters.clear()
        for character in self.chapter.characters:
            if character in self.rendered_characters:
                continue
            character_appearance: str = self.chapter.characters[character]["Appearance"]
            self.rendered_characters[character] = Entity((0, 0), character_appearance, *SPRITE_SIZE)
            self.rendered_characters[character].visible = False
            name_text: str = character[:character.find("(") - 1] if character.find("(") != -1 else character
            name_font: pygame.font.SysFont = self.fonts[("Times New Roman", 28)]
            # character_name = character[character.find("(") + 1:-1] if character.find("(") != -1 else character
            character_color: str = self.chapter.characters[character]["Color"].strip("(").strip(")")
            character_color = [int(value) for value in character_color.split(", ")]
            self.rendered_names[character] = Text(NAME_POS, name_font, name_text, character_color, border=True)
            self.rendered_names[character].visible = False

    def render_dialogue(self) -> None:
        self.chapter_events.clear()
        self.rendered_dialogue.clear()
        for line in self.chapter.dialogue:
            words: list[str] = line.split()
            match words[0]:
                case "Enter":
                    if "\"" in words[1]:
                        words: str = " ".join(words[1:])
                        start: int = words.find("\"")
                        end: int = words.find("\"", start + 1)
                        character, x, y = words[start + 1:end], *words[end + 1:].split()
                        x, y = x[1:-1], y[:-1]
                    else:
                        character, x, y = words[1], words[2][1:-1], words[3][:-1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.enter_event, character, x, y))
                case "Replace":
                    if "\"" in words[1] or "\"" in words[3]:
                        words: str = " ".join(words[1:])
                        old_character, new_character = str(), str()
                        while "\"" in words:
                            start: int = words.find("\"")
                            end: int = words.find("\"", start + 1)
                            character: str = words[start + 1:end]
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
                        words = " ".join(words[1:])
                        start = words.find("\"")
                        end = words.find("\"", start + 1)
                        character = words[start + 1:end]
                    else:
                        character = words[1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.exit_event, character))
                case _:
                    if ": " not in line:
                        self.rendered_dialogue.append(len(self.chapter_events))
                        self.chapter_events.append((eval, line))
                    else:
                        dialogue_font: pygame.font.SysFont = self.fonts[("Times New Roman", 28)]
                        character, dialogue = line.split(": ")
                        self.rendered_dialogue.append(len(self.chapter_events))
                        self.chapter_events.append((self.show_name_event, character))
                        self.rendered_dialogue.append(len(self.chapter_events))
                        self.chapter_events.append((self.focus_event, character))
                        character_name: str = character[character.find("(") + 1:-1] if character.find("(") != -1 else character
                        character_color: str = self.rendered_names[character].color
                        rendered_line: Text = Text(DIALOGUE_POS, dialogue_font, dialogue, character_color, width=DIALOGUE_WIDTH, border=True)
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
        text: str = self.current_dialogue.text
        start: int = text.find("{")
        end: int = text.find("}")
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

    def mousebuttondown_callback(self, event: pygame.event.Event) -> None:
        if self.chapter is not None:
            self.progress_chapter()
        for button in [entity for entity in self.idle_surfaces if isinstance(entity, Button)]:
            if 0 < event.pos[0] - button.pos[0] < button.get_width() and 0 < event.pos[1] - button.pos[1] < button.get_height():
                button.active()
    # endregion

    # region Transition Methods
    def smooth_translation(self, obj: Entity | Text | Button, start: tuple[int, int], end: tuple[int, int]) -> None:
        if not obj.transitioning:
            obj.transitioning = True
            obj.pos = start
            obj.frames = 60 * obj.timer
        elif obj.timer > 0:
            obj.timer -= self.clock.get_time() / 1000
            pos = list(obj.pos)
            pos[0] += (end[0] - start[0]) / obj.frames
            pos[1] += (end[1] - start[1]) / obj.frames
            if pos[0] > end[0] or pos[1] > end[1]:
                pos = end
            obj.pos = tuple(pos)
        else:
            obj.timer = obj.orig_timer
            obj.transitioning = False
            obj.pos = end
    # endregion

    @staticmethod
    def quit() -> None:
        pygame.quit()
        quit()


if __name__ == "__main__":
    App()
