#Rookognition - A web-based chess vision exercise.
#Copyright (C) 2024 Nick Edner

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

import chess
import random
import chess.svg

bp = Blueprint('game', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method == 'POST':
        if request.form.get('newBoard') is not None:
            session['board'] = None
            return redirect(url_for('index'))
        if session.get('board') != None:
            if request.form.get('yes') is not None or request.form.get('no') is not None:
                answer = True if request.form.get('yes') is not None else False
                new_board = chess.Board(fen=session['board'])
                target_square = session['target_square']
                color = session['color']
                attackers = getAttackers(new_board, target_square, color=color)
                correct = (len(attackers) > 0) == answer
                flash('Correct!' if correct else 'Incorrect!')
                enable_answers = False
                arrows = generateAttackerArrows(attackers, target_square)
                answer_image = Markup(generateBoardImage(new_board, target_square, arrows))
                return render_template('game/index.html',
                                       board_image=answer_image,
                                       num_moves=new_board.ply(),
                                       question_text=generateQuestionText(color, target_square),
                                       enable_answers=enable_answers
                                       )
                


    if session.get('board') != None:
        new_board = chess.Board(fen=session['board'])
        target_square = session['target_square']
        color = session['color']
    else:
        new_board = generateRandomBoard()
        target_square = selectRandomSquare()
        color = random.sample([chess.WHITE, chess.BLACK, 2], 1)[0]
    attackers = getAttackers(new_board, target_square, color=color)
    board_image = Markup(generateBoardImage(new_board, target_square))
    session['board'] = new_board.fen()
    session['target_square'] = target_square
    session['color'] = color
    return render_template('game/index.html',
                           num_attackers=len(attackers),
                           board_image=board_image,
                           num_moves=new_board.ply(),
                           question_text=generateQuestionText(color, target_square),
                           enable_answers=True
                           )

def generateRandomBoard(num_moves=None, rand_low=20, rand_high=60) -> chess.Board:
    if num_moves == None:
        num_moves = random.randint(rand_low, rand_high)
    new_board = chess.Board()
    for _ in range(num_moves):
        legal_moves = list(new_board.legal_moves)
        if len(legal_moves) > 0:
            new_board.push(random.sample(legal_moves, 1)[0])
    return new_board

def generateBoardImage(board, target_square=None, arrows=None, size=350) -> str:
    if target_square == None:
        return chess.svg.board(board, size=size)
    if arrows == None:
        return chess.svg.board(board, fill={target_square: "#cc0000"}, size=size)
    else:
        return chess.svg.board(board, arrows=arrows, fill={target_square: "#cc0000"}, size=size)

def selectRandomSquare() -> chess.Square:
    return random.sample(chess.SQUARES, 1)[0]

def getAttackers(board, square, color=None) -> list:
    if color == None or color == 2:
        white_attackers = board.attackers(chess.WHITE, square)
        black_attackers = board.attackers(chess.BLACK, square)
        return list(white_attackers) + list(black_attackers)
    else:
        return list(board.attackers(color, square))

def generateAttackerArrows(attackers, target_square) -> list:
    arrows = []
    for attacker in attackers:
        arrows.append((attacker, target_square))
    return arrows

def generateQuestionText(color, target_square) -> str:
    return f'Is {(chess.COLOR_NAMES + ["either color"])[color]} attacking square {chess.SQUARE_NAMES[target_square]}?'
