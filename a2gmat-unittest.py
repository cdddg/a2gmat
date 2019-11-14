import os
import subprocess
from moviepy.editor import VideoFileClip

class bcolors:
    HEADER = '\033[99m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    for dirPath, dirNames, fileNames in os.walk(A2GMAT):
        if dirPath != A2GMAT and dirNames == []:
            print(bcolors.HEADER + dirPath)
            minute, second = os.path.basename(dirPath).split(' (')[1].split(')')[0].split(':')
            totals = int(minute) * 60 + int(second)

            totals_int = 0
            totals_float = 0

            for f in fileNames:
                if os.path.splitext(f)[1].lower() in ['.mov', '.mp4']:
                    f = os.path.join(dirPath, f)
                    duration = VideoFileClip(f).duration
                    totals_int += int(duration)
                    totals_float += float(duration)

            message = f'(totals:{totals}, totals_int:{totals_int}, totals_float:{totals_float})'
            if totals > totals_int:
                print(bcolors.FAIL + 'True  ' + message)
            else:
                print(bcolors.OKGREEN + 'False ' + message)

if __name__ == '__main__':
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    A2GMAT = os.path.join(SCRIPT_FOLDER, 'a2gmat')
    main()
