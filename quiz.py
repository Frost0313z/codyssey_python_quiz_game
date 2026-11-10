class Quiz:
    """퀴즈 한 문제를 나타내는 클래스"""

    def __init__(self, question, options, answer):
        # self 는 "지금 만들어지는 이 객체 자신"이다
        self.question = question  # 문제 내용 (str)
        self.options = options    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def show_quiz(self):
        # 문제를 먼저 보여 준다
        print(self.question)

        # 선택지 앞에 붙일 번호. 1번부터 시작한다
        number = 1

        # 선택지를 하나씩 꺼내서 "1. 선택지" 모양으로 보여 준다
        for option in self.options:
            print(str(number) + ". " + option)
            number = number + 1  # 다음 선택지는 번호가 1 커진다

    def check_answer(self, user_answer):
        # user_answer 는 사용자가 입력한 번호 (int)
        # 정답 번호와 같으면 맞힌 것이다
        if user_answer == self.answer:
            return True
        else:
            return False

    def to_dict(self):
        # state.json 에 저장하려고 딕셔너리로 바꾼다
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
        }
