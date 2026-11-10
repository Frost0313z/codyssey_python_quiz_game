class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []        # Quiz 객체들을 담을 목록
        self.high_score = None   # 최고 점수. 한 번도 안 풀었으면 None

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
