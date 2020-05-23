import pandas as pd

from shoe import Shoe, Card, Rank, Suit
from player import Player

class BlackJackTable:
    def __init__(self, hands=1, decks=6, player_count=4):
        self.hands_to_play = hands
        self.hands_played = 0
        self.players = []
        for i in range(player_count):
            self.players.append(Player())
        self.dealer = Player()
        self.deck_count = decks
        self.shoe = Shoe(self.deck_count)
        self.shoe.shuffle()
        self.shoe_threshold = len(self.players) * 6  
        self.df = self.__initialize_data()
    
    def run(self):
        while self.hands_played < self.hands_to_play:
            self.play_hand()
            # self.output_table_status()

    def play_hand(self):
        
        self.wager()
        self.deal()
        hand = self.hands_played + 1

        dealer_card = self.dealer.hand[0] 

        # data collection
        # --------------------------------------
        self.df.loc[hand, 'dealer_card'] = dealer_card.char_rep()
        self.df.loc[hand, 'dealer_hand'] = self.dealer.hand_value()
        for i in range(len(self.players)):
            self.df.loc[hand, f'hand_{i}'] = self.players[i].hand_str()
        # --------------------------------------

        # handle dealer blackjack
        if self.dealer.hand_value() == 21:
            # print(f'DEALER BLACKJACK!!!')
            for player in self.players:
                player.pay(0)
        
        else:
            # have each player play
            for i in range(len(self.players)):
                player = self.players[i]
                
                # check if player is playing
                if player.wager == 0:
                    continue

                # data collection
                self.df.loc[hand, f'init_move_{i}'] = player.play(self.shoe, dealer_card)

                # first check for blackjack
                if player.play(self.shoe, dealer_card) == "BLACKJACK":
                    player.pay(player.wager * 2.5)
                
                # then play hand
                while player.play(self.shoe, dealer_card) not in ["BUST", "S", "P", "BLACKJACK"]:
                    if player.play(self.shoe, dealer_card) == "H":
                        player.hand.append(self.shoe.deal())
                    elif player.play(self.shoe, dealer_card) == "D":
                        player.hand.append(self.shoe.deal())
                        if player.payroll >= player.wager:
                            player.payroll -= player.wager
                            player.wager = player.wager * 2
                        break
                # now check for busts
                if player.hand_value() > 21:
                    player.wager = 0

            
            while self.dealer.hand_value() < 17:
                self.dealer.hand.append(self.shoe.deal())
            
            # print(f'DEALER: {self.dealer.hand_value()}')
            
            # data collection
            self.df.loc[hand, 'dealer_final_hand'] = self.dealer.hand_value()

            if self.dealer.hand_value() > 21:
                for player in self.players:
                    player.pay(player.wager * 2)
            else:
                for player in self.players:
                    if self.dealer.hand_value() < player.hand_value():
                        player.pay(player.wager * 2)
                    elif self.dealer.hand_value() == player.hand_value():
                        player.pay(player.wager)
                    else:
                        player.pay(0)
        
        for i in range(len(self.players)):
            self.df.loc[hand, f'payroll_{i}'] = self.players[i].payroll

        self.clear_table()
        self.hands_played = self.hands_played + 1
        


    def wager(self):
        for player in self.players:
            player.bet()

    def deal(self):    
        self.shoe.burn()
        self.dealer.hand.append(self.shoe.deal())
        for player in self.players:
            if player.wager != 0:
                player.hand.append(self.shoe.deal())
        self.dealer.hand.append(self.shoe.deal())
        for player in self.players:
            if player.wager != 0:
                player.hand.append(self.shoe.deal())
    
    def clear_table(self):
        self.dealer.hand = []
        for player in self.players:
            player.hand = []
        if self.shoe.cards_left() < self.shoe_threshold:
            self.shoe = Shoe(self.deck_count)
            self.shoe.shuffle()

    '''
    def output_table_status(self):
        # for player in self.players:
            # print(f'Player payroll: {player.payroll}')
    '''

    def __initialize_data(self):
        df = pd.DataFrame()
        df.loc[0, 'dealer_card'] = 'NaN'
        df.loc[0, 'dealer_hand'] = 'NaN'
        df.loc[0, 'dealer_final_hand'] = 'NaN'
        for i in range(len(self.players)):
            player = self.players[i]
            df.loc[0, f'payroll_{i}'] = player.payroll
            df.loc[0, f'hand_{i}'] = 'NaN'
            df.loc[0, f'init_move_{i}'] = 'NaN' 
        return df


if __name__ == "__main__":
    table = BlackJackTable(hands=1000)
    table.run()
    # print(table.df)

