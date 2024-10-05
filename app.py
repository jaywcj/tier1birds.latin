from flask import Flask, render_template, session, request, jsonify
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def index():
    session['score'] = 0  # Initialize score
    session['question_count'] = 0  # Initialize question count
    return render_template('index.html')  # Render your HTML template

# Add your bird data and etymology dictionaries here...

@app.route('/quiz')
def quiz():
    if session['question_count'] >= 10:
        return jsonify({'finished': True, 'score': session['score']})

    common_name, correct_latin = random.choice(list(birds.items()))
    options = generate_options(correct_latin)
    session['current_question'] = {
        'common_name': common_name,
        'correct_latin': correct_latin
    }
    session['question_count'] += 1
    return jsonify({
        'common_name': common_name,
        'options': options,
        'correct_latin': correct_latin
    })

# Other existing functions...

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from the environment variable, default to 5000
    app.run(host='0.0.0.0', port=port)
