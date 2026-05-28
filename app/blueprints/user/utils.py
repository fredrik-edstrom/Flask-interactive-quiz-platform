def get_clean_question_form_data(form_data: dict) -> dict:
    return dict(
        description=form_data["description"],
        correct_answer=form_data["correct_answer"],
        wrong_answers=[wrong_answer for wrong_answer in form_data["wrong_answers"]]
    )
