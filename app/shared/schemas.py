from dataclasses import dataclass
from random import shuffle


@dataclass
class Question:
    description: str
    correct_answer: str
    wrong_answers: list[str]

    @property
    def choices(self, rearrange: bool = True) -> list[str]:
        answers = [self.correct_answer] + self.wrong_answers
        if rearrange:
            shuffle(answers)
        return answers


@dataclass
class Quiz:
    id: str
    created_by: str
    title: str
    questions: list[Question] | None = None

    @property
    def questions_count(self) -> int:
        return len(self.questions) if self.questions else 0


@dataclass
class Player:
    username: str
    score: int = 0
    on_question_index: int = 0
    has_finished: bool = False


@dataclass
class Game:
    id: str
    player: Player
    quiz: Quiz

    @property
    def current_question(self) -> Question | None:
        try:
            return Question(**self.quiz.questions[self.player.on_question_index])
        except IndexError:
            return None

    @property
    def final_score(self) -> str:
        return f"{self.player.score} / {len(self.quiz.questions)}"

    @property
    def has_questions(self) -> bool:
        return self.quiz.questions is not None

    def has_another_question(self) -> bool:
        if not self.has_questions:
            return False
        return self.player.on_question_index < len(self.quiz.questions)

    def has_next_question(self) -> bool:
        if not self.has_questions:
            return False
        return self.player.on_question_index + 1 < len(self.quiz.questions)

    def has_prev_question(self) -> bool:
        if not self.has_questions:
            return False
        return self.player.on_question_index - 1 >= 0

    def get_next_question(self) -> Question | None:
        if not self.has_questions:
            return None

        # Can only finish a Game of Quiz that has at least one Question
        if not self.has_next_question():
            self.player.has_finished = True
            return None

        self.player.on_question_index += 1
        return self.current_question

    def get_prev_question(self) -> Question | None:
        if not self.has_questions or not self.has_prev_question():
            return None

        self.player.on_question_index -= 1
        return self.current_question

    def current_game_state_to_dict(self) -> dict:
        return dict(game_id=self.id,
                    quiz_id=self.quiz.id,
                    quiz_title=self.quiz.title,
                    quiz_progress=f"{self.player.on_question_index + 1} / "
                                  f"{self.quiz.questions_count}",
                    question_description=self.current_question.description,
                    question_choices=self.current_question.choices,
                    current_score=f"{self.player.score} / "
                                  f"{self.quiz.questions_count}",
                    has_finished=self.player.has_finished
                    )

    def end_game_results_to_dict(self) -> dict:
        return dict(game_id=self.id,
                    quiz_title=self.quiz.title,
                    quiz_progress=f"{self.player.on_question_index + 1} / "
                                  f"{self.quiz.questions_count}",
                    current_score=f"{self.player.score} / "
                                  f"{self.quiz.questions_count}",
                    has_finished=self.player.has_finished
                    )
