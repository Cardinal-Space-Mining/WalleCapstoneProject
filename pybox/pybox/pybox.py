import pygame
from multiprocessing import Process, Value, Lock, Event, Queue
from threading import Thread

class UltimateC:
    def __init__(self, controller_type = None) -> None:
        self._stop_flag = Event()

        self.l_joy_x = Value('d', 0)
        self.l_joy_y = Value('d', 0)
        self.r_joy_x = Value('d', 0)
        self.r_joy_y = Value('d', 0)
        self.d_pad_x = Value('d', 0)
        self.d_pad_y = Value('d', 0)
        self.l_trigger = Value('d', 0)
        self.r_trigger = Value('d', 0)
        self.l_bumper = Value('d', 0)
        self.r_bumper = Value('d', 0)
        self.select = Value('d', 0)
        self.start = Value('d', 0)
        self.r_joy_button = Value('d', 0)
        self.l_joy_button = Value('d', 0)
        self.a_button = Value('d', 0)
        self.b_button = Value('d', 0)
        self.x_button = Value('d', 0)
        self.y_button = Value('d', 0)

        pygame.init()
        pygame.joystick.init()
        print('waiting for controller')
        while True:
            try:
                pygame.event.get()
                _controller = pygame.joystick.Joystick(0)
                break
            except:
                pass
        _controller.init()
        print('controller connected')
        
        self._listen_process = Process(target=self._ultimate_c_listen)
        self._val_lock = Lock()
        self._listen_process.start()

    def __del__(self):
        self._stop_flag.set()

    def _ultimate_c_listen(self):
        while not self._stop_flag.is_set():
            for event in pygame.event.get():
                with self._val_lock:
                    if event.type == pygame.JOYAXISMOTION:
                        if event.dict['axis'] == 0:
                            self.l_joy_x.value = round(event.dict['value'], 3)
                        if event.dict['axis'] == 1:
                            self.l_joy_y.value = round(event.dict['value'] * -1, 3)
                        if event.dict['axis'] == 2:
                            self.r_joy_x.value = round(event.dict['value'], 3)
                        if event.dict['axis'] == 3:
                            self.r_joy_y.value = round(event.dict['value'] * -1, 3)
                        if event.dict['axis'] == 4:
                            self.r_trigger.value = round((event.dict['value'] + 1) / 2, 3)
                        if event.dict['axis'] == 5:
                            self.l_trigger.value = round((event.dict['value'] + 1) / 2, 3)
                    if event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:
                        if event.dict['button'] == 0:
                            if self.a_button.value == 0:
                                self.a_button.value = 1
                            else:
                                self.a_button.value = 0
                        if event.dict['button'] == 1:
                            if self.b_button.value == 0:
                                self.b_button.value = 1
                            else:
                                self.b_button.value = 0
                        if event.dict['button'] == 3:
                            if self.x_button.value == 0:
                                self.x_button.value = 1
                            else:
                                self.x_button.value = 0
                        if event.dict['button'] == 4:
                            if self.y_button.value == 0:
                                self.y_button.value = 1
                            else:
                                self.y_button.value = 0
                        if event.dict['button'] == 6:
                            if self.l_bumper.value == 0:
                                self.l_bumper.value = 1
                            else:
                                self.l_bumper.value = 0
                        if event.dict['button'] == 7:
                            if self.r_bumper.value == 0:
                                self.r_bumper.value = 1
                            else:
                                self.r_bumper.value = 0
                        if event.dict['button'] == 10:
                            if self.select.value == 0:
                                self.select.value = 1
                            else:
                                self.select.value = 0
                        if event.dict['button'] == 11:
                            if self.start.value == 0:
                                self.start.value = 1
                            else:
                                self.start.value = 0
                        if event.dict['button'] == 13:
                            if self.l_joy_button.value == 0:
                                self.l_joy_button.value = 1
                            else:
                                self.l_joy_button.value = 0
                        if event.dict['button'] == 14:
                            if self.r_joy_button.value == 0:
                                self.r_joy_button.value = 1
                            else:
                                self.r_joy_button.value = 0
                    if event.type == pygame.JOYHATMOTION:
                        self.d_pad_x.value = event.dict['value'][0]
                        self.d_pad_y.value = event.dict['value'][1]
                    if event.type == pygame.JOYDEVICEREMOVED:
                        self.l_joy_x.value = 0
                        self.l_joy_y.value = 0
                        self.r_joy_x.value = 0
                        self.r_joy_y.value = 0
                        self.d_pad_x.value = 0
                        self.d_pad_y.value = 0
                        self.l_trigger.value = 0
                        self.r_trigger.value = 0
                        self.l_bumper.value = 0
                        self.r_bumper.value = 0
                        self.select.value = 0
                        self.start.value = 0
                        self.r_joy_button.value = 0
                        self.l_joy_button.value = 0
                        self.a_button.value = 0
                        self.b_button.value = 0
                        self.x_button.value = 0
                        self.y_button.value = 0

                        print('controller lost, attempting reconnect...')
                        while True:
                            try:
                                pygame.event.get()
                                _controller = pygame.joystick.Joystick(0)
                                break
                            except:
                                pass
                        _controller.init()
                        print('controller connected')

    def get_l_joy_x(self):
            return self.l_joy_x.value

    def get_l_joy_y(self):
            return self.l_joy_y.value

    def get_r_joy_x(self):
            return self.r_joy_x.value

    def get_r_joy_y(self):
            return self.r_joy_y.value

    def get_d_pad_x(self):
            return self.d_pad_x.value

    def get_d_pad_y(self):
            return self.d_pad_y.value

    def get_l_trigger(self):
            return self.l_trigger.value

    def get_r_trigger(self):
            return self.r_trigger.value

    def get_l_bumper(self):
            return self.l_bumper.value

    def get_r_bumper(self):
            return self.r_bumper.value

    def get_select(self):
            return self.select.value

    def get_start(self):
            return self.start.value

    def get_r_joy_button(self):
            return self.r_joy_button.value

    def get_l_joy_button(self):
            return self.l_joy_button.value

    def get_a_button(self):
            return self.a_button.value

    def get_b_button(self):
            return self.b_button.value

    def get_x_button(self):
            return self.x_button.value

    def get_y_button(self):
            return self.y_button.value