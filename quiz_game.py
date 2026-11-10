from quiz import Quiz


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        # Quiz 객체들을 담을 목록. 지금은 기본 퀴즈로 시작한다
        # (5단계에서 state.json 을 불러오도록 바뀐다)
        self.quizzes = self.make_default_quizzes()
        self.high_score = None   # 최고 점수. 한 번도 안 풀었으면 None

    def make_default_quizzes(self):
        # 기본 퀴즈 5개를 새로 만들어서 목록으로 돌려준다
        # state.json 이 없을 때(첫 실행)와 파일이 깨졌을 때 쓴다
        # 부를 때마다 새 목록을 만들기 때문에, 퀴즈를 추가해도 기본 퀴즈는 그대로 남는다
        quizzes = []

        quizzes.append(Quiz(
            "세상에서 가장 큰 동물은?",
            ["아프리카코끼리", "흰긴수염고래", "기린", "백상아리"],
            2
        ))
        quizzes.append(Quiz(
            "다리가 8개인 동물은?",
            ["거미", "개미", "나비", "잠자리"],
            1
        ))
        quizzes.append(Quiz(
            "펭귄은 어떤 무리에 속할까?",
            ["포유류", "조류", "파충류", "어류"],
            2
        ))
        quizzes.append(Quiz(
            "캥거루가 원래 사는 곳은?",
            ["아프리카", "남아메리카", "오스트레일리아", "유럽"],
            3
        ))
        quizzes.append(Quiz(
            "땅 위에서 가장 빨리 달리는 동물은?",
            ["사자", "말", "타조", "치타"],
            4
        ))

        return quizzes

    def select_num_range(self, text, min_num, max_num):
        # text    : 화면에 띄울 질문 (예: "메뉴를 선택하세요: ")
        # min_num : 입력할 수 있는 가장 작은 숫자
        # max_num : 입력할 수 있는 가장 큰 숫자
        # 범위 안의 숫자가 들어올 때까지 계속 다시 묻고, 그 숫자(int)를 돌려준다

        # 잘못 입력했을 때 보여 줄 안내 문구 (예: "1-5 사이의 숫자를 입력하세요.")
        warning = str(min_num) + "-" + str(max_num) + " 사이의 숫자를 입력하세요."

        while True:
            user_input = input(text)

            # 앞뒤 공백을 지운다 (" 1 " -> "1")
            user_input = user_input.strip()

            # 글자를 숫자로 바꿔 본다
            # "abc" 나 빈 글자("")는 숫자로 못 바꿔서 ValueError 가 난다
            try:
                number = int(user_input)
            except ValueError:
                print(warning)
                continue  # 아래는 건너뛰고 while 맨 위로 돌아가 다시 묻는다

            # 숫자이긴 한데 범위 밖인 경우 (예: 메뉴에서 9, 0, -1)
            if number < min_num or number > max_num:
                print(warning)
                continue

            # 여기까지 왔으면 범위 안의 숫자다
            return number

    def run(self):
        # 5번(종료)을 고를 때까지 메뉴를 계속 보여 준다
        while True:
            print()
            print("===== Python 퀴즈 게임 =====")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")

            choice = self.select_num_range("메뉴를 선택하세요: ", 1, 5)

            if choice == 1:
                print("퀴즈 풀기는 준비 중입니다.")
            elif choice == 2:
                print("퀴즈 추가는 준비 중입니다.")
            elif choice == 3:
                print("퀴즈 목록은 준비 중입니다.")
            elif choice == 4:
                print("점수 확인은 준비 중입니다.")
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break  # while 반복을 끝낸다
