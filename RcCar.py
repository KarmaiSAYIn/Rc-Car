import RPi.GPIO as GPIO
from pynput import keyboard, mouse
from pynput.mouse import Button
from pynput.keyboard import Key

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

MC1 = {
    "Input 1": 4,
    "Input 2": 17,
    "Input 3": 7,
    "Input 4": 18,
    }

MC2 = {
    "Input 1": 5,
    "Input 2": 6,
    "Input 3": 11,
    "Input 4": 20,
    }

class cController:
    def __init__(self):
        GPIO.setup(tuple(MC1.values()), GPIO.OUT)
        GPIO.setup(tuple(MC2.values()), GPIO.OUT)
        self.movement = {
                Key.up:    (MC1["Input 2"], MC1["Input 3"], MC2["Input 1"], MC2["Input 3"]),
                Key.down:  (MC1["Input 1"], MC1["Input 4"], MC2["Input 2"], MC2["Input 4"]),
                Key.left:  (MC1["Input 2"], MC1["Input 3"], MC2["Input 2"], MC2["Input 4"]),
                Key.right: (MC1["Input 1"], MC1["Input 4"], MC2["Input 1"], MC2["Input 3"]),
                }

        self.primary_disable_key = None

    def activate_pins(self, key = None):
        for i in self.movement.keys():
            if i != key:
                GPIO.output(self.movement[i], GPIO.LOW)

        if self.movement.has_key(key):
            GPIO.output(self.movement[key], GPIO.HIGH)

    def on_press(self, key):
        if key == Key.esc:
            return False

        if self.movement.has_key(key):
            self.activate_pins(key)

            self.primary_disable_key = key

        return True

    def on_release(self, key):
        if key == self.primary_disable_key:
            self.activate_pins()
            self.primary_disable_key = None
        elif self.primary_disable_key != None:
            self.activate_pins(self.primary_disable_key)
        else:
            self.activate_pins()

        return True

    def on_click(self, x, y, button, pressed):
        print(button)
        if button == Button.left:
            if pressed:
                self.activate_pins(Key.left)
            else:
                self.activate_pins(self.primary_disable_key)
        elif button == Button.right:
            if pressed:
                self.activate_pins(Key.right)
            else:
                self.activate_pins(self.primary_disable_key)
        elif button == Button.button8:
            if pressed:
                self.activate_pins(Key.down)
                self.primary_disable_key = Key.down
            else:
                self.activate_pins()
                self.primary_disable_key = None
        elif button == Button.button9:
            if pressed:
                self.activate_pins(Key.up)
                self.primary_disable_key = Key.up
            else:
                self.activate_pins()
                self.primary_disable_key = None

        if button == Button.middle:
            self.activate_pins()
            self.primary_disable_key = None

        return True

    def on_scroll(self, x, y, dx, dy):
        if dy > 0:
            self.activate_pins(Key.up)
            self.primary_disable_key = Key.up
        else:
            self.activate_pins(Key.down)
            self.primary_disable_key = Key.down

        return True 

controller = cController()

KeyboardControl = False

if KeyboardControl:
    with keyboard.Listener(on_press=controller.on_press, on_release=controller.on_release) as listener:
        listener.join()
else:
    with mouse.Listener(on_click=controller.on_click, on_scroll=controller.on_scroll) as listener:
        listener.join()

GPIO.cleanup()



