import chess
import chess.svg
import random
from enum import Enum, auto

class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()

class BaseQuestion(object):
    def __init__(self, board:chess.Board|None=None):
        self.num_moves = None
        if board == None:
            self.board = self.generate_random_board()
        else:
            self.board = board
        return

    def to_dict(self):
        return {
                'board_fen': self.get_board_fen() if self.board != None else None,
                'num_moves': self.num_moves
                }

    def get_board(self):
        return self.board

    def get_board_fen(self):
        if self.board == None:
            raise Exception('Cannot get fen without valid board')
        return self.board.fen()

    def get_num_moves(self):
        return self.num_moves

    def generate_random_board(self, num_moves=None, rand_low=20, rand_high=60) -> chess.Board:
        if num_moves == None:
            num_moves = random.randint(rand_low, rand_high)
        self.num_moves = num_moves
        new_board = chess.Board()
        for _ in range(num_moves):
            legal_moves = list(new_board.legal_moves)
            if len(legal_moves) > 0:
                new_board.push(random.sample(legal_moves, 1)[0])
        return new_board

    def get_board_image(self, target_square=None, arrows=None, size=None) -> str:
        if self.board == None:
            raise Exception('Cannot generate board image without valid board')
        if target_square == None:
            return chess.svg.board(self.board, size=size)
        if arrows == None:
            return chess.svg.board(self.board, fill={target_square: "#cc0000"}, size=size)
        else:
            return chess.svg.board(self.board, arrows=arrows, fill={target_square: "#cc0000"}, size=size)

    def get_attacker_arrows(self, attackers, target_square) -> list:
        arrows = []
        for attacker in attackers:
            arrows.append((attacker, target_square))
        return arrows

    def get_attackers(self, square, color=None) -> list:
        if self.board == None:
            raise Exception('Cannot get attackers without valid board')
        if color == None or color == 2:
            white_attackers = self.board.attackers(chess.WHITE, square)
            black_attackers = self.board.attackers(chess.BLACK, square)
            return list(white_attackers) + list(black_attackers)
        else:
            return list(self.board.attackers(color, square))


class TargetSquareQuestion(BaseQuestion):
    def __init__(self, board=None, board_fen=None, difficulty=Difficulty.EASY, color=None, target_square=None, possible_answers=None, correct_answer=None, **kwargs) -> None:
        self.difficulty = difficulty
        self.color = color
        self.target_square = target_square
        self.possible_answers = possible_answers
        self.correct_answer = correct_answer
        self.board_fen = board_fen
        self.answer_image = None
        if board != None:
            super().__init__(board=board)
            self.board = board
        elif board_fen != None:
            super().__init__(board=chess.Board(fen=board_fen))
        else:
            super().__init__()
            self.generate()
        pass

    def to_dict(self) -> dict:
        to_return = super().to_dict()
        return to_return | {
                'difficulty_value': self.difficulty.value if self.difficulty else None,
                'color': getattr(self, 'color', None),
                'target_square': getattr(self, 'target_square', None),
                'question_text': getattr(self, 'question_text', None),
                'possible_answers': getattr(self, 'possible_answers', None),
                'correct_answer': getattr(self, 'correct_answer', None),
                'answer_image': getattr(self, 'answer_image', None)
                }

    def _select_random_square(self) -> chess.Square:
        return random.sample(chess.SQUARES, 1)[0]

    def _select_random_color(self) -> int:
        return random.sample([chess.WHITE, chess.BLACK, 2], 1)[0]

    def _color_to_name(self, color:int) -> str:
        return (chess.COLOR_NAMES + ["either color"])[color]

    def get_difficulty(self) -> Difficulty:
        return self.difficulty

    def get_question_text(self) -> str:
        if self.color == None or self.target_square == None:
            raise Exception('get_question_text() requires color and target_square defined for type TargetSquareQuestion')
        # Temp catch for other difficulties until they are implemented
        if self.difficulty != Difficulty.EASY:
            raise Exception(f"Invalid difficulty: {self.difficulty.name}")
        #if self.difficulty == Difficulty.EASY:
        return f'Is {self._color_to_name(self.color)} attacking square {chess.SQUARE_NAMES[self.target_square]}?'

    def get_color(self):
        return self.color

    def get_target_square(self):
        return self.target_square

    def get_possible_answers(self):
        return self.possible_answers

    def get_correct_answer(self):
        return self.correct_answer

    def get_attackers(self, color=None) -> list:
        if self.target_square == None:
            raise Exception("Cannot get attackers without a valid target square")
        if color != None:
            return super().get_attackers(self.target_square, color)
        else:
            return super().get_attackers(self.target_square, self.color)

    def get_board_image(self) -> str:
        if self.target_square == None:
            return super().get_board_image()
        else:
            return super().get_board_image(self.target_square)

    def get_answer_image(self):
        if getattr(self, 'answer_image', None) == None:
            if getattr(self, 'target_square', None) == None or getattr(self, 'color', None) == None:
                raise Exception('Cannot generate an answer image without both target_square and color')
            self.answer_image = super().get_board_image(
                        target_square=self.target_square,
                        arrows=self.get_attacker_arrows(
                            target_square=self.target_square,
                            attackers=self.get_attackers()
                            )
                        )
        return self.answer_image

    def generate(self, board:chess.Board|None=None, difficulty:Difficulty=Difficulty.EASY):
        if getattr(self, 'board', None) == None:
            if board == None:
                raise Exception("No board object provided, cannot generate TargetSquareQuestion")
            print(f"DEBUG: updating board to new board {board}")
            self.board = board
        if getattr(self, 'difficulty', None) == None:
            if difficulty == None:
                raise Exception("No difficulty provided, cannot generate TargetSquareQuestion")
            print(f"DEBUG: updating difficulty to new difficulty: {difficulty.name}")
            self.difficulty = difficulty
        # Temp catch for other difficulties until they are implemented
        if self.difficulty != Difficulty.EASY:
            raise Exception(f"Invalid difficulty: {self.difficulty.name}")
        print(f"DEBUG: generating question of difficulty {self.difficulty.name}")
        if self.difficulty == Difficulty.EASY:
            self.color = self._select_random_color()
            self.target_square = self._select_random_square()
            self.question_text = self.get_question_text()
            self.possible_answers = ['Yes','No']
            self.correct_answer = 'Yes' if len(self.get_attackers()) > 0 else 'No'
        return self


#----------------------------------
# Constant to associate difficulty to question type (class)
#----------------------------------

QUESTION_TYPE = {
        Difficulty.EASY: TargetSquareQuestion
        #Difficulty.MEDIUM: ??
        #Difficulty.HARD: ??
        }