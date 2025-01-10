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
import pytest
import chess

def test_index(client):
    response = client.get('/')
    assert b'Board' in response.data

def test_index_post_as_first_call(client):
    response = client.post('/',
                           data={'test':''}
                           )
    assert b'Board' in response.data

@pytest.mark.parametrize(('answer','validation'), (
                         ('Yes',b'Correct!'),
                         ('No',b'Incorrect!')
                         ))
def test_index_answer(client, monkeypatch, answer, validation):
    def generate_test_board(self):
        return chess.Board('2k5/1q6/8/8/8/2p5/1P6/1K6')

    def generate_test_square(self):
        return chess.C3

    def generate_test_color(self):
        return chess.WHITE

    monkeypatch.setattr('rookognition.question.BaseQuestion.generate_random_board', generate_test_board)
    monkeypatch.setattr('rookognition.question.TargetSquareQuestion._select_random_square', generate_test_square)
    monkeypatch.setattr('rookognition.question.TargetSquareQuestion._select_random_color', generate_test_color)
    response = client.get('/')
    response = client.post('/',
                           data={'answer':answer}
                           )
    assert validation in response.data

def test_index_newboard(client):
    response = client.post('/',
                  data={'newBoard':''}
                  )
    assert '/' in response.headers['location']
    response = client.get(response.headers['location'])
    assert b'Board' in response.data

def test_index_sameboard(client, monkeypatch):
    def generate_test_board(self):
        return chess.Board('2k5/1q6/8/8/8/2p5/1P6/1K6')

    def generate_test_square(self):
        return chess.C3

    def generate_test_color(self):
        return chess.WHITE

    monkeypatch.setattr('rookognition.question.BaseQuestion.generate_random_board', generate_test_board)
    monkeypatch.setattr('rookognition.question.TargetSquareQuestion._select_random_square', generate_test_square)
    monkeypatch.setattr('rookognition.question.TargetSquareQuestion._select_random_color', generate_test_color)
    response = client.get('/')
    response = client.post('/',
                           data={'test':''}
                           )
    assert b'<desc><pre>. . k . . . . .\n. q . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . p . . . . .\n. P . . . . . .\n. K . . . . . .</pre></desc>' in response.data
