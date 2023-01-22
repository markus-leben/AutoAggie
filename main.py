import pyautogui  # you must have cv2 installed
import keyboard  # to check for the escape key you must run as admin/root
from sys import platform
import os
import PIL.ImageGrab
import time
import json

# TODO: Implement basic logic on more impactful locations

with open("settings.json") as settings:
    SETTINGS = json.load(settings)


def correctxy(gui_tuple):
    # should refactor for better use on input and output
    if platform == "darwin":
        return gui_tuple[0] / 2, gui_tuple[1] / 2
    else:
        return gui_tuple[0], gui_tuple[1]


def correctxy_otherdirection(gui_tuple):
    # should refactor for better use on input and output
    if platform == "darwin":
        return gui_tuple[0] / 2, gui_tuple[1] / 2
    else:
        return gui_tuple[0], gui_tuple[1]


def locate_from_settings(settings_str):
    # functionalizing this to save a bit of sanity.
    return pyautogui.locateCenterOnScreen(SETTINGS[settings_str]['path'],
                                          confidence=SETTINGS["confidence"],
                                          region=(SETTINGS[settings_str]['left'],
                                                  SETTINGS[settings_str]['top'],
                                                  SETTINGS[settings_str]['width'],
                                                  SETTINGS[settings_str]['height']))


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
        print("Current unflipped cards: %s" % self.check_unflipped())
        for i in state_arr:
            # print("    checking %s" % i["img_path"])
            try:
                # print((i['left'], i['top'], i['width'], i['height']))
                correctxy(locate_from_settings(i["setting_name"]))
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
                # print("    %s" % e)

    def attempt_action(self):
        if self.screen == "play_screen":
            time.sleep(.5)
            try:
                x, y = correctxy(locate_from_settings("playbutton"))

                pyautogui.click(x, y, clicks=2, interval=0.25)
            except:
                pass
        elif self.screen == "turnfinished":
            print("Clicking end turn")
            try:
                x, y = correctxy(locate_from_settings("endturnlit"))
                pyautogui.click(x, y)
                # pyautogui.moveTo(150, 150)
                return
            except Exception as e:
                print(e)
                print('failed to find end turn button')
        elif self.screen == "awsnap":
            print("Attempting to exit error screen")
            try:
                x, y = correctxy(locate_from_settings("somethingwrong"))
                pyautogui.click(x, y)
                # pyautogui.moveTo(150, 150)
                self.screen = "play_screen"
                return
            except Exception as e:
                print(e)
                print('failed to exit')
        elif self.screen == "retreatconfirm":
            print('confirming retreat')
            try:
                x, y = correctxy(locate_from_settings("retreatnow"))
                pyautogui.click(x, y)
                return
            except:
                pass

        elif self.screen == "collectrewards":
            try:
                x, y = correctxy(locate_from_settings("collectrewards"))
                pyautogui.click(x, y)
                self.screen = "nextscreen"
                return
            except:
                pass
        elif self.screen == "nextscreen":

            try:
                x, y = correctxy(locate_from_settings("next"))
                time.sleep(1)
                pyautogui.click(x, y)
                self.screen = "beginning_state"
                return
            except:
                pass
        elif self.screen == "playingcards":
            if not self.turn_increased:
                self.turn += 1
                self.turn_increased = True
            time.sleep(1.0)
            if (self.turn > 3 and self.check_win_count() >= 2) or self.turn > 4:
                if (self.check_win_count() >= 2) and self.check_unflipped() != 0:
                    print("skipping due to %s unflipped cards" % self.check_unflipped())
                    return
                print('retreating')
                try:
                    x, y = correctxy(locate_from_settings("retreatbutton"))
                    pyautogui.click(x, y)
                    self.screen = "retreatconfirm"
                    return
                except:
                    pass
        elif self.screen == "retreatnow":
            print('retreating')
            try:
                x, y = correctxy(locate_from_settings("retreatbutton"))
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
        pixel_coords = [(SETTINGS["lanepixels"][0][0], SETTINGS["lanepixels"][0][1]),
                        (SETTINGS["lanepixels"][1][0], SETTINGS["lanepixels"][1][1]),
                        (SETTINGS["lanepixels"][2][0], SETTINGS["lanepixels"][2][1])]
        # pixel_coords = [(314, 559), (487, 548), (661, 560)]
        for i in pixel_coords:
            x, y = correctxy_otherdirection(i)
            if len(image.load()[x, y]) == 4:
                red, green, blue, transparent = image.load()[x, y]
            else:
                red, green, blue = image.load()[x, y]

            if (red > 230) and (100 < green < 220) and (blue < 100):
                pixel_wins += 1
            print("    r: %s g: %s b: %s" % (red, green, blue))

        print("    wins: %s" % pixel_wins)
        return pixel_wins

    def check_unflipped(self):
        return len(list(pyautogui.locateAll('images/snapback.png', pyautogui.screenshot(region=(200, 500, 600, 300)),
                                            confidence=.85)))

    def generate_state_checks(self):
        return_state_arr = []
        return_state_arr.append({"screen": "awsnap",
                                 "turn": "n/a",
                                 "setting_name": "somethingwrong"
                                 })
        if self.screen in ["playingcards", "play_screen"]:
            return_state_arr.append({"screen": "turnfinished",
                                     "turn": "n/a",
                                     "setting_name": "endturnlit"})
        if self.screen == "turnfinished":
            return_state_arr.append({"screen": "playingcards",
                                     "turn": "n/a",
                                     "setting_name": "playing"})
            return_state_arr.append({"screen": "retreatnow",
                                     "turn": "n/a",
                                     "setting_name": "glitchwait"})
        if self.screen == "beginning_state":
            return_state_arr.append({"screen": "play_screen",
                                     "turn": 1,
                                     "setting_name": "playbutton"
                                     })
        if self.screen not in ["nextscreen"]:
            return_state_arr.append({"screen": "collectrewards",
                                     "turn": self.turn,
                                     "setting_name": "collectrewards"})

        return return_state_arr


def main():
    game = GameState()
    while True:
        # if keyboard.is_pressed('esc'):
        #     print('escaping')
        #     break
        game.check_screen()
        # game.check_win_count()
        game.attempt_action()


if __name__ == '__main__':
    main()
