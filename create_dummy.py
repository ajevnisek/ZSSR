import sys
import time
import subprocess


START_SLEEP_TIME = 10
END_SLEEP_TIME = 3


def main(path):
    print(f"Going for {START_SLEEP_TIME} seconds nap")
    time.sleep(START_SLEEP_TIME)
    print(f"Creating {path}/DUMMY.txt")
    subprocess.call(["touch", f"{path}/DUMMY.txt"])
    print(f"Going for {END_SLEEP_TIME} seconds sleep before death")
    time.sleep(END_SLEEP_TIME)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else None
    main(path)