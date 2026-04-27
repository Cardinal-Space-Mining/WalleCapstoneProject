from adafruit_servokit import ServoKit, ContinuousServo, Servo

from pybox import UltimateC

import math

import os
import atexit

import pygame

__audio_dir__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")


class LimitedServo:
    __slots__ = ("servo", "min_angle", "max_angle")
    servo: Servo
    min_angle: float
    max_angle: float

    def __init__(self, servo, min_angle=90, max_angle=175):
        self.servo = servo
        self.min_angle = min_angle
        self.max_angle = max_angle

    @property
    def angle(self) -> float:
        angle = self.servo.angle
        return angle if angle is not None else 0.0

    @angle.setter
    def angle(self, value):
        value = max(self.min_angle, min(self.max_angle, value))
        self.servo.angle = value

    def set_to_percent(self, percent):
        """Sets the servo position to a percentage of its range between its max and min values. Eg, ``.3`` is 30% of the way from min to max

        Keyword arguments:

        ``percent`` -- must be within ``[0,1]``

        """
        angle = self.min_angle + ((self.max_angle - self.min_angle) * percent)
        self.angle = angle


class Walle:
    __slots__ = (
        "_kit",
        "_not_a",
        "_not_b",
        "_not_x",
        "_not_y",
        "_audioA",
        "_audioX",
        "_audioY",
        "_audioB",
    )
    _kit: ServoKit
    _not_a: bool
    _not_b: bool
    _not_x: bool
    _not_y: bool

    _def_servo_pos = (0, 0, 150, 150, 60, 110, 120, 50, 60, 135, 132, 110, 90, 150, 110)
    _mins = (0, 0, 40, 130, 0, 60, 50, 50, 20, 0, 48, 48, 0, 95, 45, 0)
    # Down to 0
    _maxs = (
        0,
        0,
        150,
        160,
        180,
        120,
        180,
        130,
        180,
        180,
        180,
        180,
        180,
        150,
        180,
        0,
    )

    _audioA_path = os.path.join(__audio_dir__, "eve.mp3")
    _audioX_path = os.path.join(__audio_dir__, "Wa...Wall-e.mp3")
    _audioY_path = os.path.join(__audio_dir__, "Aaaaah !.mp3")
    _audioB_path = os.path.join(__audio_dir__, "Ohooo !.mp3")

    def __init__(self, kit: ServoKit) -> None:
        self._kit = kit
        self._not_a = True
        self._not_b = True
        self._not_x = True
        self._not_y = True
        self.reset_servos()
        self._audioA = pygame.mixer.Sound(Walle._audioA_path)
        self._audioX = pygame.mixer.Sound(Walle._audioX_path)
        self._audioY = pygame.mixer.Sound(Walle._audioY_path)
        self._audioB = pygame.mixer.Sound(Walle._audioB_path)

    def reset_servos(self):
        self.ltrack.throttle = 0
        self.rtrack.throttle = 0

        for i in range(2, len(Walle._def_servo_pos)):
            self._kit.servo[i].angle = Walle._def_servo_pos[i]

    @property
    def ltrack(self) -> ContinuousServo:
        return self._kit.continuous_servo[0]

    @property
    def rtrack(self) -> ContinuousServo:
        return self._kit.continuous_servo[1]

    @property
    def lshoulder(self) -> LimitedServo:
        idx = 2
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def lelbow(self) -> LimitedServo:
        idx = 3
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def lwrist(self) -> LimitedServo:
        idx = 4
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def lthumb(self) -> LimitedServo:
        idx = 5
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def lfingers(self) -> LimitedServo:
        idx = 6
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def rshoulder(self) -> LimitedServo:
        idx = 7
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def relbow(self) -> LimitedServo:
        idx = 8
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def rwrist(self) -> LimitedServo:
        idx = 9
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def rthumb(self) -> LimitedServo:
        idx = 10
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def rfingers(self) -> LimitedServo:
        idx = 11
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def headpan(self) -> LimitedServo:
        idx = 12
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def headtilt(self) -> LimitedServo:
        idx = 13
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @property
    def eyes(self) -> LimitedServo:
        idx = 14
        return LimitedServo(self._kit.servo[idx], Walle._mins[idx], Walle._maxs[idx])

    @staticmethod
    def _motor_pwr(ctrler_x: float, ctrler_y: float) -> tuple[float, float]:
        m = math.hypot(ctrler_x, ctrler_y) / math.sqrt(2)
        if m < 0.1:
            return (0.0, 0.0)
        theta = math.atan2(ctrler_x, ctrler_y)
        pi_div_4 = math.pi / 4
        m_a = math.cos(theta - pi_div_4) * m
        m_b = math.cos(theta + pi_div_4) * m
        return m_a, m_b

    def _handle_track_ctrl(self, controller: UltimateC):
        motor_a, motor_b = Walle._motor_pwr(
            -controller.get_l_joy_x(), controller.get_l_joy_y()
        )
        self.ltrack.throttle = -motor_a
        self.rtrack.throttle = motor_b

    def _handle_audio(self, controller: UltimateC):
        # Audio A
        if controller.get_a_button() == 1 and self._not_a:
            self._audioA.play()
            # print("Audio A")
            self._not_a = False
        if controller.get_a_button() != 1:
            self._not_a = True

        # Audio B
        if controller.get_b_button() == 1 and self._not_b:
            self._audioB.play()
            # print("Audio B")
            self._not_b = False
        if controller.get_b_button() != 1:
            self._not_b = True

        # Audio X
        if controller.get_x_button() == 1 and self._not_x:
            self._audioX.play()
            # print("Audio X")
            self._not_x = False
        if controller.get_x_button() != 1:
            self._not_x = True

        # Audio Y
        if controller.get_y_button() == 1 and self._not_y:
            self._audioY.play()
            # print("Audio Y")
            self._not_y = False
        if controller.get_y_button() != 1:
            self._not_y = True

    def _handle_shoulders(self, controller: UltimateC):
        if controller.get_l_bumper() == 1:
            shoulder_speed = 0.5
            joystick_y = controller.get_r_joy_y()
            self.lshoulder.angle -= shoulder_speed * joystick_y
            self.rshoulder.angle += shoulder_speed * joystick_y

    def _handle_elbows(self, controller: UltimateC):
        if controller.get_l_bumper() == 1:
            elbow_speed = 0.25
            joystick_x = controller.get_r_joy_x()
            self.lelbow.angle -= elbow_speed * joystick_x
            self.relbow.angle += elbow_speed * joystick_x

    def _handle_wrists(self, controller: UltimateC):
        wrist_speed = 3.0
        if controller.get_start() == 1:
            self.lwrist.angle += wrist_speed
            self.rwrist.angle -= wrist_speed
        if controller.get_select() == 1:
            self.lwrist.angle -= wrist_speed
            self.rwrist.angle += wrist_speed

    def _handle_hands(self, controller: UltimateC):
        l_percent = controller.get_l_trigger()
        self.lthumb.set_to_percent(l_percent)
        self.lfingers.set_to_percent(l_percent)

        r_percent = controller.get_r_trigger()
        self.rthumb.set_to_percent(r_percent)
        self.rfingers.set_to_percent(r_percent)

    def _handle_neck(self, controller: UltimateC):
        headPan_speed = 1.0
        headTilt_speed = 1.0
        if controller.get_l_bumper() == 0:
            # print(f"D_neck: {controller.get_r_joy_x() * headPan_speed}")
            d_neck = controller.get_r_joy_x() * headPan_speed
            if abs(d_neck )< 0.01:
                d_neck = 0
            self.headpan.angle += d_neck
            self.headtilt.angle += controller.get_r_joy_y() * headTilt_speed

    def _handle_eyes(self, controller: UltimateC):
        if controller.get_r_joy_button() == 0:
            self.eyes.angle = self.eyes.max_angle
        else:
            self.eyes.angle = self.eyes.min_angle

    def rest(self):
        for x in range(2, len(self._kit.servo)):
            try:
                self._kit.servo[x].angle = None
            except ValueError as e:
                pass

    def update(self, controller: UltimateC):
        self._handle_track_ctrl(controller)
        self._handle_shoulders(controller)
        self._handle_elbows(controller)
        self._handle_wrists(controller)
        self._handle_hands(controller)
        self._handle_neck(controller)
        self._handle_eyes(controller)
        self._handle_audio(controller)


def main():
    pygame.init()
    pygame.joystick.init()
    pygame.mixer.init(buffer=4096)  # Increase buff size so underruns don't occur

    walle = Walle(ServoKit(channels=16))
    atexit.register(walle.rest)

    with UltimateC() as controller:
        try:
            while True:
                for event in pygame.event.get():
                    controller.handle_pygame_evt(event)
                walle.update(controller)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
