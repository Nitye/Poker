# from cards import distribute_cards

# hands = distribute_cards(3)

class player():
  pot = 0
  bet = 0
  turn = 0
  _play_ = True
  check = True
  num_players = 0
  max_folds = 0
  players = []

  @classmethod
  def draw_winnings_(cls, num_people):
    player.turn += 1
    return cls.pot/num_people

  @classmethod
  def blind_(cls, player1, player2, blind_bet):
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

  def __init__(self, name,  bank):
    self.name = name
    self.bank = bank
    self.check = False
    self.play = True
    self.bet = 0
    self.current_bet = 0
    self.__class__.players.append(self)
    self.__class__.num_players+=1
    print(self.name, self.bank)

  def check_(self):
    self.check = True
  
  def uncheck_(self):
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
    self.bank-=(player.bet-self.current_bet)
    self.bet = player.bet
    player.pot+=(player.bet-self.current_bet)
    self.check = True

  def fold_(self):
    if player.max_folds != len(player.players):
      self.play = False
      player.max_folds+=1

  def raise_(self):
    self.bank-=(self.bet-self.current_bet)
    self.bet = self.current_bet
    player.pot+=(self.bet-self.current_bet)
    self.check = True

  def big_blind_(self, blind_bet):
    self.bank-=blind_bet
    self.current_bet=blind_bet
    player.pot+=blind_bet
  
  def small_blind_(self, blind_bet):
    self.bank-=blind_bet//2
    self.current_bet=blind_bet//2
    player.pot+=blind_bet//2
  
  def win_(self):
    self.bank+=player.pot
    player.pot = 0
    player.turn += 1
  
  def draw_(self, draw_winnings):
    self.bank += draw_winnings
    player.pot -= draw_winnings

p1_name = input("Enter first player: ")
p2_name = input("Enter second player: ")
p3_name = input("Enter third player: ")
bank = int(input("Enter bank: "))
p1 = player(p1_name, bank) 
p2 =  player(p2_name, bank)
p3 = player(p3_name, bank)

players_in_play = player.players.copy()
players_in_play = player.check_player_play(players_in_play)
for i in range(player.num_players):
  if (player.turn)%(player.num_players)==i & i < (player.num_players-2):
    player.blind_(player.players[i+1], player.players[i+2], 50)
  elif (player.turn)%(player.num_players) == (player.num_players-2):
    player.blind_(player.players[player.num_players-1], player.players[0], 50)
  elif (player.turn)%(player.num_players) == (player.num_players-1):
    player.blind_(player.players[0], player.players[1], 50)
while player._play_ == True:
  for i in players_in_play:
    a = int(input(f"Enter option {i.name}: "))
    if a == 1:
      if player.check == True:
        i.check_()
        print("Check")
      else:
        i.call_()
        print("Called ", i.current_bet)
    elif a == 2:
      b = int(input("Enter bet: "))
      i.bet_(b)
      i.raise_()
      for j in players_in_play:
        if j == i:
          continue
        else:
          j.uncheck_()
      print("Raised to ", i.bet)
    elif a == 3:
      i.fold_()
      print("Folded")
    else:
      continue
    i.check_check_()
    players_in_play = player.check_player_play(players_in_play)
    player.check_play_(players_in_play)

print(p1.bank)
print(p2.bank)
print(p3.bank)
print(player.pot)
