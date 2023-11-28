import new_cards
import random

deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
         '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
           '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
             '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']

class player():
  pot = 0
  turn = 0
  bet = 0
  _play_ = True
  check = True
  big_blind_player = None
  num_players = 0
  max_folds = 0
  _bank_ = 0
  players = []
  table_cards = None
  blind_bet = 50
  player_scores = {}
  hands = []

  @classmethod
  def draw_winnings_(cls, num_people):
    player.turn += 1
    return cls.pot/num_people

  @classmethod
  def set_blind_bet(cls):
    blind_bets = []
    c = cls.bank/100
    for i in range(1,6):
      blind_bets.append(c*i)
    if cls.turn <= 5:
      cls.blind_bet = blind_bets[0]
    elif cls.turn <= 10:
      cls.blind_bet = blind_bets[1]
    elif cls.turn <= 15:
      cls.blind_bet = blind_bets[2]
    elif cls.turn <= 20:
      cls.blind_bet = blind_bets[3]
    else:
      cls.blind_bet = blind_bets[4]

  @classmethod
  def blind_(cls, player1, player2, blind_bet):
    cls.bet = blind_bet
    player1.big_blind_(blind_bet)
    player2.small_blind_(blind_bet)

  @classmethod
  def check_player_play(cls, players_in_play):
    for i in players_in_play:
      if i.play != True:
        players_in_play.remove(i)
    return players_in_play
  
  @classmethod
  def check_play_(cls, players_in_play):
    c = 0
    for i in players_in_play:
      if i.check == True:
        c+=1
      else:
        pass
    if len(players_in_play) != 1:
      if c == len(players_in_play):
        player._play_ = False
      else:
        player._play_ = True
    else:
      player._play_ = False

  @classmethod
  def reset_all_(cls):
    for i in cls.players:
      i.reset()

  @classmethod
  def reset_cls(cls):
    cls._play_ = True
    cls.bet = 0
    cls.hands = []
    cls.table_cards = None

  @classmethod
  def draw_cards(cls, num):
    a = 0
    dummy_hand = []
    while a < num:
      card_a = random.choice(deck)
      removed_card_index = deck.index(card_a)
      deck.pop(removed_card_index)
      a+=1
      dummy_hand.append(card_a)
    return dummy_hand

  @classmethod
  def distribute_cards(cls):
    card_num = (cls.num_players*2) + 5
    chosen_cards = cls.draw_cards(card_num)
    b = 0
    while b < cls.num_players:
      cls.hands.append(chosen_cards[2*b:2*(b+1)])
      b+=1
    cls.table_cards = chosen_cards[2*cls.num_players:]

  @classmethod
  def add_cards(cls):
    i = 0
    for j in player.players:
      j.cards = player.hands[i]
      i+=1

  def __init__(self, name,  bank):
    self.score = 0
    self.__class__._bank_ = bank
    self.name = name
    self.bank = bank
    self.prev_bank = bank
    self.play = True
    self.__class__.players.append(self)
    self.__class__.num_players+=1
    self.reset()
    print(self.name, self.bank)

  def reset(self):
    self.cards = None
    self.bet = 0
    self.all_in = False
    self.check = False
    self.current_bet = 0

  def check_(self):
    self.check = True
  
  def allin(self):
    self.all_in = True

  def uncheck_(self):
    if self.all_in:
      pass
    else:
      self.check = False

  def check_check_(self):
    if self.check == False:
      player.check = False
    else:
      pass

  def bet_(self, bet):
    player.check = False
    if bet>=self.__class__.bet:
      self.bet = bet
      self.__class__.bet = bet
    else:
      self.bet = self.__class__.bet

  def call_(self):
    # last mei uske do baar katt gaye for somme reason
    self.bet = player.bet
    self.bank-=(self.bet-self.current_bet)
    player.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_()

  def fold_(self):
    if player.max_folds != len(player.players):
      self.play = False
      player.max_folds+=1
      a = player.players.index(self)
      key = 'player'+str(a+1)+'_score'
      player.player_scores.pop(key)

  def raise_(self):
    self.bank-=(self.bet-self.current_bet)
    player.pot+=(self.bet-self.current_bet)
    self.current_bet = self.bet
    self.check_() 

  def big_blind_(self, blind_bet):
    self.bank-=blind_bet
    self.current_bet=blind_bet
    player.big_blind_player = self
    player.pot+=blind_bet
  
  def small_blind_(self, blind_bet):
    self.bank-=blind_bet//2
    self.current_bet=blind_bet//2
    player.pot+=blind_bet//2
  
  def win_(self, players_in_play):
    self.bank+=player.pot
    player.pot = 0
    player.turn += 1
    self.prev_bank = self.bank
    players_in_play.remove(self)
    return players_in_play
    
  
  def draw_(self, draw_winnings):
    self.bank += draw_winnings
    player.pot -= draw_winnings
    self.prev_bank = self.bank

p1 = player('n',1000)
p2 = player('p',1000)
p3 = player('t',1000)
player.distribute_cards()
player.add_cards()
print(p1.cards)
print(p2.cards)
print(p3.cards)
print(player.table_cards)