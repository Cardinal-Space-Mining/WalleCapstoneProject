import pygame
from threading import Thread, Lock, Event


class UltimateC:
    __slots__ = (
        "_stop_flag",
        "_val_lock",
        "_thread",
        "l_joy_x",
        "l_joy_y",
        "r_joy_x",
        "r_joy_y",
        "d_pad_x",
        "d_pad_y",
        "l_trigger",
        "r_trigger",
        "l_bumper",
        "r_bumper",
        "select",
        "start",
        "r_joy_button",
        "l_joy_button",
        "a_button",
        "b_button",
        "x_button",
        "y_button",
        "_controller"
    )

    def __init__(self, controller_type=None) -> None:
        self._stop_flag = Event()
        self._val_lock = Lock()
        self._thread = None
        self.l_joy_x = 0.0
        self.l_joy_y = 0.0
        self.r_joy_x = 0.0
        self.r_joy_y = 0.0
        self.d_pad_x = 0.0
        self.d_pad_y = 0.0
        self.l_trigger = 0.0
        self.r_trigger = 0.0
        self.l_bumper = 0.0
        self.r_bumper = 0.0
        self.select = 0.0
        self.start = 0.0
        self.r_joy_button = 0.0
        self.l_joy_button = 0.0
        self.a_button = 0.0
        self.b_button = 0.0
        self.x_button = 0.0
        self.y_button = 0.0
        self._controller = None

    def __enter__(self):
        print("waiting for controller")
        while True:
            try:
                pygame.event.get()
                self._controller = pygame.joystick.Joystick(0)
                break
            except:
                pass

        self._controller.init()
        print("controller connected")

        self._thread = Thread(target=self._ultimate_c_listen)  # , daemon=True)
        self._thread.start()

        return self  # required for "as" usage

    def __exit__(self, exc_type, exc, tb):
        self._stop_flag.set()
        if self._thread is not None:
            self._thread.join()

    def _ultimate_c_listen(self):
        while not self._stop_flag.is_set():
            for event in pygame.event.get():
                with self._val_lock:
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis == 0:
                            self.l_joy_x = round(event.value, 3)
                        elif event.axis == 1:
                            self.l_joy_y = round(-event.value, 3)
                        elif event.axis == 2:
                            self.r_joy_x = round(event.value, 3)
                        elif event.axis == 3:
                            self.r_joy_y = round(-event.value, 3)
                        elif event.axis == 4:
                            self.r_trigger = round((event.value + 1) / 2, 3)
                        elif event.axis == 5:
                            self.l_trigger = round((event.value + 1) / 2, 3)

                    elif event.type in (pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN):

                        def toggle(attr):
                            setattr(self, attr, 1 - getattr(self, attr))

                        mapping = {
                            0: "a_button",
                            1: "b_button",
                            3: "x_button",
                            4: "y_button",
                            6: "l_bumper",
                            7: "r_bumper",
                            10: "select",
                            11: "start",
                            13: "l_joy_button",
                            14: "r_joy_button",
                        }

                        if event.button in mapping:
                            toggle(mapping[event.button])

                    elif event.type == pygame.JOYHATMOTION:
                        self.d_pad_x, self.d_pad_y = event.value

                    elif event.type == pygame.JOYDEVICEREMOVED:
                        self._reset_values()

                        print("controller lost, attempting reconnect...")
                        while True:
                            try:
                                pygame.event.get()
                                self._controller = pygame.joystick.Joystick(0)
                                break
                            except:
                                pass

                        self._controller.init()
                        print("controller connected")

    def _reset_values(self):
        self.l_joy_x = 0.0
        self.l_joy_y = 0.0
        self.r_joy_x = 0.0
        self.r_joy_y = 0.0
        self.d_pad_x = 0.0
        self.d_pad_y = 0.0
        self.l_trigger = 0.0
        self.r_trigger = 0.0
        self.l_bumper = 0.0
        self.r_bumper = 0.0
        self.select = 0.0
        self.start = 0.0
        self.r_joy_button = 0.0
        self.l_joy_button = 0.0
        self.a_button = 0.0
        self.b_button = 0.0
        self.x_button = 0.0
        self.y_button = 0.0

    # Getters
    def get_l_joy_x(self):
        return self.l_joy_x

    def get_l_joy_y(self):
        return self.l_joy_y

    def get_r_joy_x(self):
        return self.r_joy_x

    def get_r_joy_y(self):
        return self.r_joy_y

    def get_d_pad_x(self):
        return self.d_pad_x

    def get_d_pad_y(self):
        return self.d_pad_y

    def get_l_trigger(self):
        return self.l_trigger

    def get_r_trigger(self):
        return self.r_trigger

    def get_l_bumper(self):
        return self.l_bumper

    def get_r_bumper(self):
        return self.r_bumper

    def get_select(self):
        return self.select

    def get_start(self):
        return self.start

    def get_r_joy_button(self):
        return self.r_joy_button

    def get_l_joy_button(self):
        return self.l_joy_button

    def get_a_button(self):
        return self.a_button

    def get_b_button(self):
        return self.b_button

    def get_x_button(self):
        return self.x_button

    def get_y_button(self):
        return self.y_button


def main():
    pygame.init()
    pygame.joystick.init()
    try:
        with UltimateC() as controller:
            while True:
                data = {
                    "controller.get_l_joy_x()" : controller.get_l_joy_x(),
                    "controller.get_l_joy_y()" : controller.get_l_joy_y(),
                    "controller.get_l_trigger()" : controller.get_l_trigger(),
                    "controller.get_r_joy_x()" : controller.get_r_joy_x(),
                    "controller.get_r_joy_y()" : controller.get_r_joy_y(),
                    "controller.get_r_trigger()" : controller.get_r_trigger(),
                }
                # print(controller.get_a_button())
                print()
                for item in data.keys():
                    print(f"{item} : {data[item]}")
                print()
    except:
        print("Adios")


if __name__ == "__main__":
    main()
