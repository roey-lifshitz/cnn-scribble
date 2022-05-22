from typing import Optional, Tuple, Dict
from UI.base import UI
from UI.text_box import TextBox
import pygame


class ChatBox(UI):
    """
    Static input box
    """

    def __init__(self, rect, amount,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 **kwargs: Optional[Dict]) -> None:
        super().__init__(rect, kwargs)

        self.color = color
        self.font = pygame.font.SysFont(self.font, self.font_size)

        self.text_boxes = []
        self.counter = 0

        self.amount = amount

        # Initialize all text boxes in chat box
        text_height = self.height // amount

        for i in range(amount):

            text_box = TextBox((self.x, self.y + i * text_height, self.width, text_height), align_left=True, has_border=False)
            self.text_boxes.append(text_box)


    def draw(self, screen, dt):
        """
        Draws input box, text and focus bar
        :param screen:
        :return:
        """
        super().draw(screen, self.color)

        for box in self.text_boxes:
            box.draw(screen, dt)


    def handle_event(self, event: pygame.event) -> None:
        """
        Updates the input box every frame
        :param event: current user event
        :return: None
        """
        pass

    def append_text(self, text: str) -> None:
        if self.counter < self.amount:
            self.text_boxes[self.counter].text = text;
            self.counter += 1;
        else:

            head = 0;
            for next in range(1, self.amount):
                self.text_boxes[head].text = self.text_boxes[next].text;
                head = next
            self.text_boxes[head].text = text





