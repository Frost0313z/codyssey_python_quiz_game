import json
import os

from quiz import Quiz


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        # state.json 은 "실행한 곳"이 아니라 "이 파일(quiz_game.py)이 있는 폴더"에 둔다
        # 그래야 다른 폴더에서 python 경로\main.py 로 실행해도 같은 파일을 쓴다
        folder = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(folder, "state.json")

        self.quizzes = []        # Quiz 객체들을 담을 목록
        self.high_score = None   # 최고 점수. 한 번도 안 풀었으면 None

        # 저장된 퀴즈와 최고 점수를 불러온다
        self.load_data()

    def load_data(self):
        # 퀴즈는 모두 state.json 에서 가져온다 (코드 안에 따로 넣어 둔 퀴즈는 없다)

        # 1) 파일이 없으면 퀴즈 0개로 시작한다
        if not os.path.exists(self.file_path):
            print("state.json 파일이 없습니다. 퀴즈 0개로 시작합니다.")
            return

        # 2) 파일을 읽어서 JSON 을 파이썬 데이터(dict)로 바꾼다
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except ValueError:
            # JSON 모양이 깨졌을 때 (예: 중괄호 하나가 빠짐)
            self.handle_broken_file("저장 파일이 손상되었습니다.")
            return
        except OSError:
            # 파일을 읽을 수 없을 때 (예: 권한이 없음)
            self.handle_broken_file("저장 파일을 읽지 못했습니다.")
            return

        # 3) JSON 은 맞는데 내용 형태가 틀렸을 때 (예: 정답이 7, 선택지가 3개)
        if self.check_data(data) == False:
            self.handle_broken_file("저장 파일의 내용이 올바르지 않습니다.")
            return

        # 4) 여기까지 왔으면 멀쩡한 파일이다. dict 를 Quiz 객체로 바꿔 담는다
        self.quizzes = []
        for item in data["quizzes"]:
            quiz = Quiz(item["question"], item["options"], item["answer"])
            self.quizzes.append(quiz)
        self.high_score = data["high_score"]

        # 불러온 결과를 알려 준다
        if self.high_score == None:
            score_text = "최고점수 없음"
        else:
            score_text = "최고점수 " + str(self.high_score) + "점"
        print("저장된 데이터를 불러왔습니다 (퀴즈 " + str(len(self.quizzes)) + "개, " + score_text + ")")

    def handle_broken_file(self, message):
        # 파일에 문제가 있을 때: 안내 → 망가진 파일은 .bak 로 보관 → 퀴즈 0개로 시작
        # 망가진 파일을 지우지 않는 이유: 그 안에 퀴즈가 남아 있어서 손으로 고쳐 살릴 수 있다
        print(message)
        backup_path = self.file_path + ".bak"
        try:
            os.replace(self.file_path, backup_path)  # 이름 바꾸기 (같은 이름의 .bak 가 있으면 덮어씀)
            print("기존 파일은 state.json.bak 으로 보관했습니다.")
        except OSError:
            print("기존 파일을 보관하지 못했습니다.")

        print("퀴즈 0개로 시작합니다.")
        self.quizzes = []
        self.high_score = None

    def check_data(self, data):
        # 불러온 data 가 PRD 4장의 규칙에 맞으면 True, 하나라도 틀리면 False

        # 맨 바깥은 dict 이고, quizzes 와 high_score 두 키가 있어야 한다
        if type(data) != dict:
            return False
        if "quizzes" not in data or "high_score" not in data:
            return False

        # quizzes 는 목록이어야 한다 (빈 목록도 괜찮다 = 퀴즈 0개)
        if type(data["quizzes"]) != list:
            return False

        # 퀴즈 하나하나를 검사한다
        for item in data["quizzes"]:
            if type(item) != dict:
                return False
            if "question" not in item or "options" not in item or "answer" not in item:
                return False

            # 문제: 빈 글자가 아닌 문자열
            question = item["question"]
            if type(question) != str or question.strip() == "":
                return False

            # 선택지: 문자열 정확히 4개
            options = item["options"]
            if type(options) != list or len(options) != 4:
                return False
            for option in options:
                if type(option) != str:
                    return False

            # 정답: 1~4 정수
            # type() 으로 비교하면 true/false 가 숫자로 몰래 통과하는 것도 막는다
            answer = item["answer"]
            if type(answer) != int:
                return False
            if answer < 1 or answer > 4:
                return False

        # 최고 점수: null(None) 이거나 0~100 정수
        high_score = data["high_score"]
        if high_score != None:
            if type(high_score) != int:
                return False
            if high_score < 0 or high_score > 100:
                return False

        return True

    def save_data(self):
        # Quiz 객체들을 dict 로 바꿔서 목록에 담는다
        quiz_list = []
        for quiz in self.quizzes:
            quiz_list.append(quiz.to_dict())

        data = {
            "quizzes": quiz_list,
            "high_score": self.high_score,
        }

        # 파일에 쓴다. ensure_ascii=False 는 한글을 글자 그대로 저장하라는 뜻
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("파일을 저장하지 못했습니다. 이번 변경은 프로그램을 끄면 사라집니다.")

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

    def play_quiz(self):
        # 퀴즈가 하나도 없으면 풀 게 없으니 안내만 하고 메뉴로 돌아간다
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)  # 전체 문제 수
        correct = 0                # 맞힌 문제 수
        number = 1                 # 지금 몇 번째 문제인지

        print()
        print("퀴즈를 시작합니다! (총 " + str(total) + "문제)")

        # 퀴즈를 하나씩 꺼내서 차례로 낸다
        for quiz in self.quizzes:
            print()
            print("[문제 " + str(number) + "]")
            quiz.show_quiz()

            # 정답 번호는 1~4 만 받는다 (메뉴에서 만든 입력 메서드를 그대로 쓴다)
            user_answer = self.select_num_range("정답 번호: ", 1, 4)

            if quiz.check_answer(user_answer) == True:
                print("정답입니다!")
                correct = correct + 1
            else:
                print("오답입니다. 정답은 " + str(quiz.answer) + "번입니다.")

            number = number + 1

        # 점수는 100점 만점으로 바꾼다 (맞힌 수 ÷ 문제 수 × 100, 반올림)
        # 퀴즈를 추가하면 문제 수가 바뀌니, 맞힌 개수보다 점수로 비교하는 게 공평하다 (PRD D2)
        score = round(correct / total * 100)

        print()
        print(str(total) + "문제 중 " + str(correct) + "문제 정답 (" + str(score) + "점)")

        # 이번 점수를 최고 점수와 비교한다
        self.update_high_score(score)

    def update_high_score(self, score):
        # 처음 푼 경우(None) 이거나, 이번 점수가 더 높으면 최고 점수를 바꾸고 저장한다
        if self.high_score == None or score > self.high_score:
            self.high_score = score
            self.save_data()
            print("새로운 최고 점수입니다! (" + str(score) + "점)")
        else:
            print("최고 점수는 그대로 " + str(self.high_score) + "점입니다.")

    def input_text(self, text):
        # 빈 글자가 아닌 글을 받을 때까지 계속 다시 묻는다
        # (select_num_range 의 "글자 버전". 문제와 선택지를 받을 때 쓴다)
        while True:
            user_input = input(text)
            user_input = user_input.strip()  # 앞뒤 공백을 지운다

            if user_input == "":
                print("빈 칸은 안 됩니다. 다시 입력하세요.")
                continue  # while 맨 위로 돌아가 다시 묻는다

            return user_input

    def input_new_quiz(self):
        # 문제 · 선택지 4개 · 정답 번호를 입력받아 Quiz 객체를 하나 만들어 돌려준다
        print()
        print("새 퀴즈를 추가합니다.")

        question = self.input_text("문제: ")

        # 선택지 4개를 차례로 받아 목록에 담는다
        options = []
        number = 1
        while number <= 4:
            option = self.input_text("선택지 " + str(number) + ": ")
            options.append(option)
            number = number + 1

        # 정답 번호는 1~4 만 받는다 (메뉴 · 퀴즈 풀기와 같은 입력 메서드)
        answer = self.select_num_range("정답 번호(1-4): ", 1, 4)

        new_quiz = Quiz(question, options, answer)
        return new_quiz

    def add_quiz(self, quiz):
        # 만들어진 Quiz 객체를 목록 맨 뒤에 넣고, 바로 state.json 에 저장한다
        # (바로 저장해야 프로그램이 갑자기 꺼져도 추가한 퀴즈가 남는다)
        self.quizzes.append(quiz)
        self.save_data()
        print("퀴즈가 추가되었습니다! (총 " + str(len(self.quizzes)) + "개)")

    def show_list(self):
        # 퀴즈가 하나도 없으면 안내만 하고 메뉴로 돌아간다
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print()
        print("등록된 퀴즈 목록 (총 " + str(len(self.quizzes)) + "개)")

        # 문제만 번호를 붙여서 보여 준다 (선택지와 정답은 보여 주지 않는다)
        number = 1
        for quiz in self.quizzes:
            print("[" + str(number) + "] " + quiz.question)
            number = number + 1

    def show_score(self):
        # 한 번도 안 풀었으면 high_score 가 None 이다
        if self.high_score == None:
            print("아직 기록 없음 — 1번 메뉴에서 퀴즈를 풀어 보세요.")
        else:
            print("최고 점수: " + str(self.high_score) + "점")

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
                self.play_quiz()
            elif choice == 2:
                new_quiz = self.input_new_quiz()  # 입력받아 Quiz 객체를 만들고
                self.add_quiz(new_quiz)           # 목록에 넣고 저장한다
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break  # while 반복을 끝낸다
