import sys

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit()

from flask import Flask, render_template

sys.path.extend(['homecontrol']);

from memory_game import MemoryGame
from home_control import HomeControl

app = Flask(__name__)

app.MemoryGame = MemoryGame(app, '/memory_game')
app.HomeControl = HomeControl(app, '/home_control')

if __name__ == '__main__':

    app.run(debug=True)
