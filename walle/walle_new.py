from adafruit_servokit import ServoKit, ContinuousServo, Servo


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
    def angle(self) -> float | None:
        return self.servo.angle

    @angle.setter
    def angle(self, value):
        value = max(self.min_angle, min(self.max_angle, value))
        self.servo.angle = value


class Walle:
    _kit: ServoKit

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

    def __init__(self, kit: ServoKit) -> None:
        self._kit = kit
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
