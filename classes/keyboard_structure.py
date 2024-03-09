import os
import copy
import cv2 as cv
import numpy as np

from helpers import *
from classes.button import Button
from classes.hand import Hand
from PIL import ImageFont, ImageDraw, Image

bengali_to_english = {
    '১': '1',
    '২': '2',
    '৩': '3',
    '৪': '4',
    '৫': '5',
    '৬': '6',
    '৭': '7',
    'ঁ' : '&',
    '৮': '8',
    '৯': '9',
    '০': '0',
    'ঙ': 'q',
    'ং': 'Q',
    'য': 'w',
    'য়': 'W',
    'ড': 'e',
    'ঢ': 'E',
    'প': 'r',
    'ফ': 'R',
    'ট': 't',
    'ঠ': 'T',
    'চ': 'y',
    'ছ': 'Y',
    'জ': 'u',
    'ঝ': 'U',
    'হ': 'i',
    'ঞ': 'I',
    'গ': 'o',
    'ঘ': 'O',
    'ড়': 'p',
    'ঢ়': 'P',
    'ৎ': '\\',
    'ঃ': '|',
    'ৃ': 'a',
   'র্' : 'A',
    'ু': 's',
    'ূ': 'S',
    'ি': 'd',
    'ী': 'D',
    'া': 'f',
    'অ': 'F',
    'আ': 'Ff',
    '্': 'g',
    '।': 'G',
    'ব': 'h',
    'ভ': 'H',
    'ক': 'j',
    'খ': 'J',
    'ত': 'k',
    'থ': 'K',
    'দ': 'l',
    'ধ': 'L',
    '্র': 'z',
    '্য': 'Z',
    'ও': 'x',
    'ৗ': 'X',
    'ে': 'c',
    'ৈ': 'C',
    'এ': 'gc',
    'ঐ': 'gC',
    'ঔ': 'gX',
    'ই' : 'gd',
    'ঈ' : 'gD',
    'উ' : 'gs',
    'ঊ' : 'gS',
    'ঋ': 'ga',
    'ো': 'cf',
    'ৌ': 'cX',
    'র' : 'v',
    'ল' : 'V',
    'ন' : 'b',
    'ণ' : 'B',
    'স' : 'n',
    'ষ' : 'N',
    'ম' : 'm',
    'শ' : 'M',
    '‘' : '`',
    '“' : '~',
    '”' : '"',
    '’' : '\'',
    ' ' : ' ',
}


class KeyboardStructure:
    def __init__(self, name, width, height, buttons, hands):
        self.name = name
        self.width = width
        self.height = height

        self.buttons = list()
        for button in buttons:
            self.buttons.append(Button(
                id=button['id'],
                location=button['location'],
                size=button['size']
            ))

        self.buttons = sorted(self.buttons, key=lambda button: button.id)

        self._check_buttons_overlapping()

        self.hands = list()
        for hand in hands:
            self.hands.append(Hand(fingers=hand['fingers']))

    def smallest_distance_from_button_to_finger(self, button_id):
        minimum_distance_value = float('inf')

        for i, hand in enumerate(self.hands):
            for j, finger in enumerate(hand.fingers):
                temp_minimum_distance = finger.location.euclidean_distance(self.buttons[button_id].location)
                minimum_distance_value = min(minimum_distance_value, temp_minimum_distance)

        return minimum_distance_value

    def visualize(
        self,
        dirpath,
        characters_placement=None,
        show_hands=True,
        save=False
    ):
        if characters_placement is None:
            characters_placement = [''] * len(self.buttons)

        img = np.ones((cm2px(self.height), cm2px(self.width), 3), np.uint8)
        for i in range(cm2px(self.height)):
            for j in range(cm2px(self.width)):
                img[i][j] = [141, 140, 127]

        for button in self.buttons:
            cv.rectangle(
                img=img,
                pt1=cm2px((button.top_left.x, button.top_left.y)),
                pt2=cm2px((button.bottom_right.x, button.bottom_right.y)),
                color=(80, 62, 44),
                thickness=-1
            )

        if show_hands:
            for hand in self.hands:
                hand_color = random_color()
                for finger in hand.fingers:
                    cv.circle(
                        img=img,
                        center=cm2px((finger.location.x, finger.location.y)),
                        radius=cm2px(0.5),
                        color=hand_color,
                        thickness=-1
                    )
        english_to_bengali = {v: k  for k, v in bengali_to_english.items() if len(v) == 1}
        print(english_to_bengali)
        fontpath = "./sol.ttf"     
        font = ImageFont.truetype(fontpath, 20, encoding='unic')
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)

        for button, character in zip(self.buttons, characters_placement):
            pos = cm2px((button.text_origin.x, button.text_origin.y))
            pos = (pos[0] + 13, pos[1] - 35)
            draw.text((pos[0], pos[1] + 20),  english_to_bengali[character] if character in english_to_bengali else character, font = font, fill = (0,0,255,0))
            if character in english_to_bengali and character.upper() != character:
                draw.text(pos,  english_to_bengali[character.upper()] if character in english_to_bengali else character, font = font, fill = (0,0,255,0))
            cv.putText(
                img=img,
                text=character,
                org=cm2px((button.text_origin.x, button.text_origin.y)),
                fontFace=cv.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(241, 240, 236),
                thickness=2
            )
        
        # draw.text((500, 100),  'অ', font = font, fill = (0,0,255,0))
        img = np.array(img_pil)

        cv.imshow(self.name, img)
        cv.waitKey(0)

        if save:
            print(self.name)
            cv.imwrite(os.path.join(dirpath, self.name + '.png'), img)

    def _check_buttons_overlapping(self):
        for i in range(len(self.buttons)):
            for j in range(i + 1, len(self.buttons)):
                if self.buttons[i].is_overlapping(self.buttons[j]):
                    warning_log('buttons %s and %s are overlapped' % (i + 1, j + 1))

    def __str__(self):
        text = '%s Configurations\n' % self.name
        text += '- Width: %scm\n' % self.width
        text += '- Height: %scm\n' % self.height
        text += '- Number of Buttons: %s\n' % len(self.buttons)
        text += '- Number of Hands: %s' % len(self.hands)
        return text
