import json
import falcon
import pyautogui
from AppKit import NSScreen

SECOND_SCREEN_ABOVE_PRIMARY = True


def screenSizes():
    ss = []
    for screen in NSScreen.screens():
        w = screen.frame().size.width
        h = screen.frame().size.height
        ss.append((w, h))
    return ss


def focusPoints():
    ss = screenSizes()
    sp = ss[0]
    se = ss[1]
    if SECOND_SCREEN_ABOVE_PRIMARY:
        se = (se[0], -se[1])
    posmap = {
        "priL": (sp[0] // 4, sp[1] // 2),
        "priR": (sp[0] // 4 * 3, sp[1] // 2),
        "extL": (se[0] // 4, se[1] // 2),
        "extR": (se[0] // 4 * 3, se[1] // 2),
    }
    return posmap


class MoveToScreen:
    def __init__(self, posmap):
        self.pos = posmap

    def on_get(self, req, resp, screen_pos):
        if screen_pos in self.pos:
            x, y = self.pos[screen_pos]
            pyautogui.click(x, y)
            resp.text = json.dumps(
                f"moved to screen position: {screen_pos}, position: ({x}, {y})"
            )
            resp.status = falcon.HTTP_200
        else:
            resp.text = json.dumps(f"invalid screen position: {screen_pos}")
            resp.status = falcon.HTTP_200


application = falcon.App()
screen = MoveToScreen(focusPoints())
application.add_route("/movetoscreen/{screen_pos}", screen)
