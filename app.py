import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    all_questions = load_questions()

    num_to_select = min(20, len(all_questions))
    selected_questions = random.sample(all_questions, num_to_select)

    for q in selected_questions:
        if q.get('shuffle') is True:
            random.shuffle(q['options'])

    return render_template('quiz.html', questions=selected_questions)


@app.route('/submit', methods=['POST'])
def submit():
    all_questions = load_questions()
    score = 0
    total = 0
    review_data = []

    questions_map = {str(q['id']): q for q in all_questions}

    displayed_ids = request.form.getlist('all_question_ids')

    for q_id in displayed_ids:
        q = questions_map.get(q_id)
        if not q:
            continue

        total += 1

        user_answers = request.form.getlist(f"question_{q_id}")

        if isinstance(q['correct'], list):
            correct_answers = q['correct']
        else:
            correct_answers = [q['correct']]

        is_correct = sorted(user_answers) == sorted(correct_answers)
        if is_correct:
            score += 1

        review_data.append({
            "question": q['question'],
            "options": q['options'],
            "user_answers": user_answers,
            "correct_answers": correct_answers,
            "is_correct": is_correct
        })

    return render_template('result.html', score=score, total=total, review=review_data)


if __name__ == '__main__':
    app.run(debug=True)
