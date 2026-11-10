class Quiz:
    """퀴즈 한 문제를 나타내는 클래스"""

    def __init__(self, question, options, answer):
        # self 는 "지금 만들어지는 이 객체 자신"이다
        self.question = question  # 문제 내용 (str)
        self.options = options    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def to_dict(self):
        # state.json 에 저장하려고 딕셔너리로 바꾼다
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
        }
