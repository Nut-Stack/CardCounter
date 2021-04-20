#Created by Nut-Stack

def make_deck(num_of_decks):
    card_points = ['a','k','q','j','2','3','4','5','6','7','8','9','10']
    card_signs = ['Hearts','Clubs','Diamonds','Spades']
    deck = {}

    for points in range(len(card_points)):
        for signs in range (len(card_signs)):
            card = (card_points[points],card_signs[signs])
            deck.update({card_points[points]:num_of_decks*4})
    return deck


class DeckShit:
    def __init__(self,deck,card):
        self.card = card
        self.deck = deck
    def calculate_value(self):
        if self.deck.get(self.card) != None and self.deck.get(self.card) > 0:
            if self.card in self.deck:
                high = ['a','k','q','j','10']
                low = ['2','3','4','5','6']
                medium = ['7','8','9']
                if self.card in high:
                    value = -1
                if self.card in low:
                    value = 1
                if self.card in medium:
                    value = 0
                self.deck.update({self.card:self.deck.get(self.card)-1})
        else:
            print("{} not in deck".format(self.card))
            value = False
        return value

def main():
    num_of_decks = int(input("How many decks are there?"))
    #base_bet = int(input("What is your base bet?"))
    base_bet = 1
    while True:
        deck = make_deck(num_of_decks)
        count = 0
        card_num = 0
        while True:
            while True:
                value = input("Value:")
                if value == "quit":
                    break
                p = DeckShit(deck,value)
                output = p.calculate_value()
                if output != False:
                    count += output
                    card_num += 1
                print(deck)
            true_count = (count)/(num_of_decks - (card_num/52))
            bet_amount = base_bet * true_count
            print("Current Count: {}".format(count))
            print("True Count   : {}".format(true_count))
            if true_count <= 1:
                print("Bet          : {}".format(base_bet))
            else:
                print("Bet          : {}".format(bet_amount))
            shuffle = input("Was there a shuffle? (y/n)")
            if shuffle == "y":
                break

if __name__ == '__main__':
    main()


