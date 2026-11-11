# 프로그램은 여기서 시작한다
from quiz_game import QuizGame

# python main.py 로 직접 실행했을 때만 게임을 시작한다
# (다른 파일에서 import 만 했을 때는 저절로 실행되지 않는다)
if __name__ == "__main__":
    game = QuizGame()  # 게임 객체를 하나 만들고
    game.run()         # 메뉴를 띄운다
