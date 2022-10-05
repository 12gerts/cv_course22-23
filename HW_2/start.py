import subprocess


def main():
    p1 = subprocess.Popen(['python', 'motion_recognition.py'])
    p2 = subprocess.Popen(['python', 'wormy.py'])
    while p1.poll() != 0 and p2.poll() != 0:
        pass
    p1.kill()
    p2.kill()


if __name__ == '__main__':
    main()
