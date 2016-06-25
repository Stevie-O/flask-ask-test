from flask import Flask, render_template

from memory_game import MemoryGame

app = Flask(__name__)

app.MemoryGame = MemoryGame(app, '/memory_game')

if __name__ == '__main__':

    app.run(debug=True)
