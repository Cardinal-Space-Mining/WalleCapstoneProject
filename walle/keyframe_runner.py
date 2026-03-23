from dataclasses import dataclass
from typing import Callable, Any
from collections import deque
import time


@dataclass(slots=True)
class KeyframeStep:
    exec_time_sec: float
    exec_step: Callable[[], Any]


@dataclass(slots=True)
class KeyframeSeq:
    start_time: float
    steps: deque[KeyframeStep]

    @staticmethod
    def from_steps_staggered(
        steps: list[Callable[[], Any]], dt: float
    ) -> "KeyframeSeq":
        return KeyframeSeq(
            time.monotonic(),
            deque(KeyframeStep(dt * i, step) for i, step in enumerate(steps)),
        )

    def update(self):
        while not self.finished():
            elapsed_time = time.monotonic() - self.start_time
            first = self.steps[0]

            if elapsed_time >= first.exec_time_sec:
                first.exec_step()
                self.steps.popleft()
            else:
                break

    def finished(self) -> bool:
        return not self.steps

    def sleep_to_next(self):
        if self.finished():
            return

        first = self.steps[0]
        sleep_time = first.exec_time_sec - (time.monotonic() - self.start_time)

        if sleep_time > 0:
            time.sleep(sleep_time)

    def restart(self):
        self.start_time = time.monotonic()


@dataclass(slots=True)
class KeyframeSeqBuilder:
    steps: deque[KeyframeStep]

    def __init__(self) -> None:
        self.steps = deque()

    def __get_last_time(self) -> float:
        if self.steps:
            return self.steps[-1].exec_time_sec
        else:
            return 0

    def append_step(self, dt: float, cb: Callable[[], Any]):
        self.steps.append(KeyframeStep(dt + self.__get_last_time(), cb))

    def build(self) -> KeyframeSeq:
        tmp = self.steps
        self.steps = deque()
        return KeyframeSeq(time.monotonic(), tmp)


def main():
    steps = [lambda: print("Hello1"), lambda: print("Hello2"), lambda: print("Hello3")]

    runner = KeyframeSeq.from_steps_staggered(steps, 0.25)

    while not runner.finished():
        runner.update()
        runner.sleep_to_next()

    builder = KeyframeSeqBuilder()
    builder.append_step(0, lambda: print(1))
    builder.append_step(0.2, lambda: print(2))
    builder.append_step(0.7, lambda: print(3))

    runner = builder.build()

    while not runner.finished():
        runner.update()
        runner.sleep_to_next()


if __name__ == "__main__":
    main()
