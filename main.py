import pyautogui  # you must have cv2 installed
import keyboard  # to check for the escape key you must run as admin/root
from sys import platform
import PIL.ImageGrab

# TODO: Implement basic logic on more impactful locations


def correctxy(gui_tuple):
    # should refactor for better use on input and output
    if platform == "darwin":
        return gui_tuple[0]/2, gui_tuple[1]/2
    else:
        return gui_tuple[0], gui_tuple[1]


class GameState:
    def __init__(self):
        self.screen = "beginning_state"
        self.turn = 0
        self.turn_increased = False
        print("in pregame screen")

    def check_screen(self):
        state_arr = self.generate_state_checks()
        print("Current screen: %s" % self.screen)
        print("Current turn: %s" % self.turn)
        for i in state_arr:
            print("    checking %s" % i["img_path"])
            try:
                correctxy(pyautogui.locateCenterOnScreen(i["img_path"],
                                                         confidence=0.95,
                                                         region=(i['left'], i['top'], i['width'], i['height'])))
                self.screen = i['screen']
                if self.screen != 'playingcards':
                    self.turn_increased = False
                print('screen set')
                if isinstance(i['turn'], int):
                    self.turn = i['turn']
                print("    Setting screen to: %s" % self.screen)
                print("    Setting turn to: %s" % self.turn)
                break
            except Exception as e:
                pass
                # print(e)

    def attempt_action(self):
        action_confidence = 0.90
        if self.screen == "play_screen":
            try:
                x, y = correctxy(pyautogui.locateCenterOnScreen('images/playbutton.png',
                                                                confidence=action_confidence,
                                                                region=(380, 1260, 420, 200)))
                pyautogui.click(x, y, clicks=2, interval=0.25)
            except:
                pass
        elif self.screen == "turnfinished":
            print("Clicking end turn")
            try:
                x, y = correctxy(pyautogui.locateCenterOnScreen('images/endturnlit.png',
                                                                confidence=action_confidence,
                                                                region=(800, 1440, 400, 260)))
                pyautogui.click(x, y)
                # pyautogui.moveTo(150, 150)
                return
            except:
                print('failed to find end turn button')
        elif self.screen == "retreatconfirm":
                print('confirming retreat')
                try:
                    x, y = correctxy(pyautogui.locateCenterOnScreen(('images/retreatnow.png'),
                                                                    confidence=action_confidence,
                                                                    region=(260, 1200, 340, 140)))
                    pyautogui.click(x, y)
                    return
                except:
                    pass

        elif self.screen == "collectrewards":
            try:
                x, y = correctxy(pyautogui.locateCenterOnScreen('images/collectrewards.png',
                                                                confidence= action_confidence))
                pyautogui.click(x, y)
                self.screen = "nextscreen"
                return
            except:
                pass
        elif self.screen == "nextscreen":
            try:
                x, y = correctxy(pyautogui.locateCenterOnScreen(('images/next.png'),
                                                                confidence= action_confidence))
                pyautogui.click(x, y)
                self.screen = "beginning_state"
                return
            except:
                pass
        elif self.screen == "playingcards":
            if not self.turn_increased:
                self.turn += 1
                self.turn_increased = True
            if self.turn > 3 and self.check_win_count() >= 2:
                print('retreating')
                try:
                    x, y = correctxy(pyautogui.locateCenterOnScreen(('images/retreatbutton.png'),
                                                                    confidence=action_confidence,
                                                                    region=(0, 1500, 300, 200)))
                    pyautogui.click(x, y)
                    self.screen = "retreatconfirm"
                    return
                except:
                    pass

    def check_win_count(self):
        if self.screen != "play_screen":
            pass

        image = PIL.ImageGrab.grab()

        pixel_wins = 0
        pixel_coords = [[159, 466], [296, 458], [432, 466]]
        for i in pixel_coords:
            x = i[0]
            y = i[1]
            red, green, blue, transparent = image.load()[x*2, y*2]

            if (red > 230) and (green > 100 and green < 200) and (blue < 100):
                pixel_wins += 1
            print("    r: %s g: %s b: %s" % (red, green, blue))
        print("    wins: %s" % pixel_wins)
        return pixel_wins

    def generate_state_checks(self):
        return_state_arr = []
        # add logic for these two later
        if self.screen in ["playingcards", "play_screen"]:
            return_state_arr.append({"screen": "turnfinished",
                                     "turn": "n/a",
                                     "img_path": 'images/endturnlit.png',
                                     "left": 800,
                                     "top": 1440,
                                     "width": 400,
                                     "height": 260, })
        if self.screen == "turnfinished":
            return_state_arr.append({"screen": "playingcards",
                                     "turn": "n/a",
                                     "img_path": 'images/playing.png',
                                     "left": 800,
                                     "top": 1440,
                                     "width": 400,
                                     "height": 260, })
        if self.screen == "beginning_state":
            return_state_arr.append({"screen": "play_screen",
                                     "turn": 1,
                                     "img_path": 'images/playbutton.png',
                                     "left": 0,
                                     "top": 1200,
                                     "width": 1200,
                                     "height": 1800, })

        return_state_arr.append({"screen": "collectrewards",
                                 "turn": self.turn,
                                 "img_path": 'images/collectrewards.png',
                                 "left": 800,
                                 "top": 1440,
                                 "width": 400,
                                 "height": 260, })

        return return_state_arr


if __name__ == '__main__':
    game = GameState()
    while True:
        # if keyboard.is_pressed('esc'):
        #     print('escaping')
        #     break
        game.check_screen()
        # game.check_win_count()
        game.attempt_action()