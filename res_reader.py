import webbrowser
import argparse
import datetime
import pathlib

# Let's find the newest file matching the name pattern we've chosen for
newest_set = None
for file in pathlib.Path("var").iterdir():
    try:
        time_ = datetime.datetime.strptime(file.name.strip("re_").strip(".txt"), "%Y-%m-%d_%H:%M")
    except ValueError:  # Got a file with unexpected name
        continue
    newest_set = file
    break

for file in pathlib.Path("var").iterdir():
    try:
        time_ = datetime.datetime.strptime(file.name.strip("re_").strip(".txt"), "%Y-%m-%d_%H:%M")
    except ValueError:  # Got a file with unexpected name
        continue
    if datetime.datetime.strptime(file.name.strip("re_").strip(".txt"), "%Y-%m-%d_%H:%M") > datetime.datetime.strptime(newest_set.name.strip("re_").strip(".txt"), "%Y-%m-%d_%H:%M"):
        newest_set = file

parser = argparse.ArgumentParser(description='Waiting for the file with links to open.')
parser.add_argument('path', help='File fool path. Crtl+Shift+C from Intellij IDE to copy path.',
                    nargs="?",
                    default=newest_set)
args = parser.parse_args()
with open(args.path, "r") as f:
    lines = f.readlines()
    for ln in lines:
        webbrowser.open(ln.strip())
