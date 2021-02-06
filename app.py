from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def base():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey_start.html', title = title, instructions = instructions)

@app.route('/questions/<int:number>')
def questions(number):
    print(session['responses'])
    if (len(session['responses']) == len(satisfaction_survey.questions)):
        stop_messing()
        return redirect('/thanks')
    if (not number == len(session['responses'])):
        stop_messing()
        length = len(session['responses'])
        return redirect(f'/questions/{length}')
    question = satisfaction_survey.questions[number]
    question_text = question.question
    question_answers = question.choices
    return render_template('questions.html', question_text = question_text, question_answers = question_answers)


@app.route('/answer', methods=['POST'])
def answer():
    # responses.append(request.form['answer'])
    responses = session['responses']
    responses.append(request.form['answer'])
    session['responses'] = responses
    if (len(session['responses']) < len(satisfaction_survey.questions)):
        next_question_number = len(session['responses'])
        new_link = f'/questions/{str(next_question_number)}'
        return redirect(new_link)
    else:
        return redirect('/thanks')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

def stop_messing():
    return flash('You\'re trying to access an invalid question')

@app.route('/session', methods=['POST'])
def responses_session():
    session['responses'] = []
    return redirect('/questions/0')