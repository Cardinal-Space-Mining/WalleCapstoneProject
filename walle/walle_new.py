from adafruit_servokit import ServoKit, ContinuousServo, Servo

from pybox import UltimateC

import math

import pygame


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
    __slots__ = ("_kit", "_not_a", "_not_b", "_not_x", "_not_y")
    _kit: ServoKit
    _not_a: bool
    _not_b: bool
    _not_x: bool
    _not_y: bool

    _def_servo_pos = (0, 0, 90, 90, 60, 93, 94, 90, 90, 120, 98, 99, 90, 90, 102)
    _mins = (0, 0, 45, 80, 0, 50, 75, 0, 65, 0, 50, 75, 0, 140, 0)  # Down to 0
    _maxs = (
        180,
        180,
        130,
        115,
        180,
        130,
        170,
        180,
        100,
        180,
        120,
        170,
        180,
        175,
        180,
    )

    _audioA = pygame.mixer.Sound("/home/pi/walle/audio/eve.mp3")
    _audioX = pygame.mixer.Sound("/home/pi/walle/audio/Wa...Wall-e.mp3")
    _audioY = pygame.mixer.Sound("/home/pi/walle/audio/Aaaaah !.mp3")
    _audioB = pygame.mixer.Sound("/home/pi/walle/audio/Ohooo !.mp3")

    def __init__(self, kit: ServoKit) -> None:
        self._kit = kit
        self._not_a = True
        self._not_b = True
        self._not_x = True
        self._not_y = True
        self.reset_servos()

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
        return self._kit.continuous_servo[0]

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
            controller.get_l_joy_x(), controller.get_l_joy_y()
        )
        self.ltrack.throttle = motor_a
        self.rtrack.throttle = -motor_b

    def _handle_audio(self, controller: UltimateC):
        # Audio A
        if controller.get_a_button() == 1 and self._not_a:
            Walle._audioA.play()
            # print("Audio A")
            self._not_a = False
        if controller.get_a_button() != 1:
            self._not_a = True

        # Audio B
        if controller.get_b_button() == 1 and self._not_b:
            Walle._audioB.play()
            # print("Audio B")
            self._not_b = False
        if controller.get_b_button() != 1:
            self._not_b = True

        # Audio X
        if controller.get_x_button() == 1 and self._not_x:
            Walle._audioX.play()
            # print("Audio X")
            self._not_x = False
        if controller.get_x_button() != 1:
            self._not_x = True

        # Audio Y
        if controller.get_y_button() == 1 and self._not_y:
            Walle._audioY.play()
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
            self.headpan.angle += controller.get_r_joy_x() * headPan_speed
            self.headtilt.angle += controller.get_r_joy_y() * headTilt_speed

    def _handle_eyes(self, controller: UltimateC):
        if controller.get_r_joy_button() == 0:
            self.eyes.angle = self.eyes.max_angle
        else:
            self.eyes.angle = self.eyes.min_angle

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
    controller = UltimateC()
    walle = Walle(ServoKit(channels=16))
    try:
        while True:
            walle.update(controller)
    except Exception as e:
        pass
    walle.reset_servos()
    controller._stop_flag.set()


if __name__ == "__main__":
    main()
