#Rookognition - A web-based chess vision exercise.
#Copyright (C) 2025 Nick Edner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from flask import (
        Blueprint, current_app, flash, g, redirect, render_template, request, url_for, session
        )
from markupsafe import Markup
from werkzeug.exceptions import abort

from .timer import Timer
from .question import Difficulty, QUESTION_TYPE

bp = Blueprint('game', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    page_load_time = Timer()

    # Check difficulty, render difficulty select if none
    if session.get('difficulty') == None:
        # TODO: Implement difficulty select template
        # return render_template('game/difficulty.html', time_to_generate=page_load_time.elapsed())
        # Default to Easy until implemented
        session['difficulty'] = Difficulty.EASY.value

    if request.method == 'POST':
        # Check for answer, if exists we can check it for correctness
        if request.form.get('answer') != None:
            answer = request.form.get('answer')
            session['answered'] = True
            question = session.get('question',{})
            correct = answer == question.get('correct_answer')
            if correct == True:
                msg = 'Correct!'
                session['current_streak'] = session.get('current_streak',0) + 1
                if session.get('current_streak',0) > session.get('high_score',0):
                    session['high_score'] = session['current_streak']
            else:
                msg = 'Incorrect!'
                session['current_streak'] = 0
            flash(msg)
            return display_page(page_load_time)

        # Check for new board request
        if request.form.get('newBoard') != None:
            session['board'] = None
            # If current question is not answered, reset streak
            if session.get('answered') == None:
                session['current_streak'] = 0
            return redirect(url_for('index'))

    # Check for existing board, generate one if none exists
    if session.get('board') == None:
        board_gen_timer = Timer()
        new_question_dict = generate_random_question()
        session['board_gen_time'] = board_gen_timer.elapsed()
        session['question'] = new_question_dict
        session['board'] = new_question_dict['board_fen']

    session['answered'] = None
    return display_page(page_load_time)

def generate_board_image(question_dict:dict) -> str:
    difficulty = Difficulty(session.get('difficulty'))
    return QUESTION_TYPE[difficulty](**question_dict).get_board_image()

def generate_random_question() -> dict:
    difficulty = Difficulty(session.get('difficulty',0))
    return QUESTION_TYPE[difficulty]().to_dict()

def generate_answer_image(question_dict:dict):
    difficulty = Difficulty(session.get('difficulty',0))
    return QUESTION_TYPE[difficulty](**question_dict).get_answer_image()

def display_page(page_load_time: Timer, page_attrs: dict = {}):
    question = page_attrs.get('question',session.get('question',{}))
    num_moves = page_attrs.get('num_moves',question.get('num_moves',None))
    answered = page_attrs.get('answered',session.get('answered'))
    board_image = page_attrs.get('board_image',Markup(generate_board_image(question)) if not answered else Markup(generate_answer_image(question)))
    current_streak = session.get('current_streak',0)
    high_score = session.get('high_score',0)
    page_gen_time = page_load_time.elapsed()
    board_gen_time = page_attrs.get('board_gen_time',session.get('board_gen_time',0))
    return render_template('game/index.html',
                           question=question,
                           num_moves=num_moves,
                           board_image=board_image,
                           answered=answered,
                           currentStreak=current_streak,
                           highScore=high_score,
                           page_gen_time=page_gen_time,
                           board_gen_time=board_gen_time
                           )
