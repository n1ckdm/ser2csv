import re
import time
import typer
import serial

from typing import List, Tuple
from pytest_mock import MockerFixture


def parse_response(resp: bytes) -> int:
    print(resp.decode())
    match = re.match(r"T: . (\d+) N", resp.decode())
    if match:
        return int(match.group(1))
    else:
        return None


def record_loop(serial: serial.Serial, time_secs: int, delta_t: float) -> Tuple[List[float], List[int]]:
    start = time.perf_counter()
    now = time.perf_counter()
    data = []
    times = []
    while (now - start) < time_secs:
        serial.write(b'l')
        resp = serial.readline()
        print(now - start)
        if (force := parse_response(resp)) is not None:
            print(force)
            data.append(force)
            times.append(now - start)

        time.sleep(delta_t)
        now = time.perf_counter()

    return times, data


def main(port: str, time_secs: int = 5, delta_t: float = 0.1, baudrate: int = 9600):
    with serial.Serial() as ser:
        ser.baudrate = baudrate
        ser.port = port
        ser.open()

        times, data = record_loop(ser, time_secs, delta_t)

        with open('results.csv') as f:
            for t, f in zip(times, data):
                f.write(f"{t},{f}")


def test_parse_response():
    assert  parse_response(b'T: + 38 N') == 38


def test_loop(mocker: MockerFixture):
    mocker.patch('serial.Serial.readline')
    mocker.patch('serial.Serial.write')

    class Serial:
        def readline(self):
            return b'T: + 38 N'
        def write(self, _):
            return None

    ser = Serial()

    times, data = record_loop(ser, 1, 0.1)
    assert len(data) == 10
    assert len(times) == 10
    assert data[0] == 38

    times, data = record_loop(ser, 1, 0.2)
    assert len(data) == 5
    assert len(times) == 5
    assert data[0] == 38

    times, data = record_loop(ser, 0.5, 0.1)
    assert len(data) == 5
    assert len(times) == 5
    assert data[0] == 38


if __name__ == "__main__":
    typer.run(main)