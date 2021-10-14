from utils import log, choose
from playingcards import cards, Cards
from random import shuffle
# 카드 더미가 0이 되면 다시 섞어준다.

def shuffle_deck() -> Cards:
    deck = cards.copy()
    shuffle(deck)
    return deck

Deck = shuffle_deck()

class Player:
    def __init__(self, name, type, chips, hand, card_sum, card_number):
        self.name = name
        self.type = type
        self.chips = chips
        self.hand = hand
        self.card_sum: int = card_sum
        self.card_number = card_number

    # 시작할 때마다 손패를 초기화한다.
    def basic_setting(self):
        del self.hand[:]
        self.card_sum = 0
        self.card_number = 0

    def cardcal(self, cardlast):
        if cardlast in "0JQK":
            return 10
        return int(cardlast)

    def draw(self, *, say_drawn=False):
        global Deck
        self.card_number += 1
        draw = Deck.pop()
        if say_drawn:
            print(f"뽑은 카드 : {draw}")
        print(f"{self.name}의 {self.card_number}번째 카드 : {draw}")
        self.hand.append(draw)
        self.card_sum += self.cardcal(draw[-1])
        print(f"{self.name}의 현재 카드 : {self.hand}")
        print(f"{self.name}의 현재 합 : {self.card_sum}")
        self.check_bust()
        if not len(Deck):
            print("덱을 셔플합니다.")
            Deck = shuffle_deck()

    def check_bust(self):
        if self.card_sum == 21:
            print(f"{self.name}님이 [Blackjack]을 완성했습니다.")
        elif self.card_sum > 21:
            print(f"{self.name}님이 [Bust]되었습니다.")
            self.card_sum = "Bust"

class UserPlayer(Player):
    def __init__(self):
        Player.__init__(self, "사용자", "User", 0, [], 0, 0)

    def set_chips(self):
        if self.chips == 0:
            log("기본칩 50개를 증정합니다.")
            self.chips = 50
        else:
            log("한 번 오신 적이 있으시군요.")
            log(f"남은 칩은 {self.chips}개 입니다.")
        log("게임을 시작합니다.")

    def cardcal(self, cardlast):
        if cardlast == "A":
            return int(choose("1", "11"))
        return super().cardcal(cardlast)

    def hit_or_stay(self):
        return choose("Hit", "Stay")

    def bet_chips(self):
        def get_int_input(ask: str, max: int):
            while True:
                try:
                    result = int(input(ask))
                    if 0 < result <= max:
                        return result

                    print("칩이 부족합니다.")
                except:
                    print("잘못 입력하셨습니다")

        result = get_int_input(
            f"남은 칩 : {self.chips}\n베팅 금액을 정해주십시오.\n",
            self.chips,
        )
        print(f"{result}개 베팅하셨습니다.")
        self.chips -= result
        return result


class DealerPlayer(Player):
    def __init__(self):
        Player.__init__(self, "딜러", "Dealer", 0, [], 0, 0)

    def draw(self):
        super().draw(say_drawn=True)

    def cardcal(self, cardlast):
        if cardlast == "A":
            return [1, 11][self.card_sum > 10]
        return super().cardcal(cardlast)

    def hit_or_stay(self):
        return ["Hit", "Stay"][self.card_sum < 17]
