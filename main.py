from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from random import randrange, choice
import os

# Correct the template directory path using forward slashes
template_dir = 'C:/Users/HaRi DeLtA/OneDrive/Documents/templates'

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'your_secret_key'


# Connect to the MySQL database for Jumbled Words and Morse Code games
def get_db_connection(db_name):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9tailfox",  # Updated MySQL password
        database=db_name
    )


# Route for the home page
@app.route('/')
def index():
    return render_template('startpage.html')  # Update to startpage.html


# Route for game selection
@app.route('/game_select')
def game_select():
    session.clear()  # Clear the session when entering game selection
    return render_template('game_select.html')


# Jumbled Words Game
@app.route('/jumbled_game', methods=['GET', 'POST'])
def jumbled_game():
    if 'score' not in session:
        session['score'] = 0

    conn = get_db_connection('jumbled')
    cursor = conn.cursor()
    cursor.execute("SELECT incorrect, correct FROM k1")
    words = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        user_input = request.form.get('answer').strip().upper()
        correct_answer = session['correct_word']

        if user_input == correct_answer:
            session['score'] += 5
            message = 'Correct Answer!'
            correct = True
        else:
            message = f'Incorrect! The correct answer was: {correct_answer}'
            correct = False

        word_index = randrange(len(words))
        session['jumbled_word'] = words[word_index][0]
        session['correct_word'] = words[word_index][1]

        return render_template('jumbled_game.html', jumbled_word=session['jumbled_word'], score=session['score'],
                               message=message, correct=correct)

    word_index = randrange(len(words))
    session['jumbled_word'] = words[word_index][0]
    session['correct_word'] = words[word_index][1]
    return render_template('jumbled_game.html', jumbled_word=session['jumbled_word'], score=session['score'],
                           message=None)


# Morse Code Game
@app.route('/morse_game', methods=['GET', 'POST'])
def morse_game():
    if 'score' not in session:
        session['score'] = 0

    conn = get_db_connection('morse_code_game')
    cursor = conn.cursor()
    cursor.execute("SELECT char_value, morse_code FROM morse_code_dict")
    morse_code_data = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        user_input = request.form.get('answer').strip().upper()
        correct_answer = session['correct_letter']

        if user_input == correct_answer:
            session['score'] += 5
            message = 'Correct Answer!'
            correct = True
        else:
            message = f'Incorrect! The correct answer was: {correct_answer}'
            correct = False

        letter_index = choice(list(range(len(morse_code_data))))
        session['letter_index'] = letter_index
        morse_code = morse_code_data[letter_index][1]
        correct_letter = morse_code_data[letter_index][0]
        session['correct_letter'] = correct_letter

        return render_template('morse_game.html', morse_code=morse_code, score=session['score'], message=message,
                               correct=correct)

    letter_index = choice(list(range(len(morse_code_data))))
    session['letter_index'] = letter_index
    morse_code = morse_code_data[letter_index][1]
    correct_letter = morse_code_data[letter_index][0]
    session['correct_letter'] = correct_letter

    return render_template('morse_game.html', morse_code=morse_code, score=session['score'], message=None)


# Exit route to clear session and reset game state
@app.route('/exit_game')
def exit_game():
    session.clear()
    return redirect(url_for('game_select'))


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
