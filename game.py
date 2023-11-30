import new_players
from new_players import player

def blind_bet():
  for i in range(player.num_players):
    if (player.turn)%(player.num_players)==i & i < (player.num_players-2):
      player.blind_(player.players[i+2], player.players[i+1], player.blind_bet)
      break
    elif (player.turn)%(player.num_players) == (player.num_players-2):
      player.blind_(player.players[0], player.players[-1], player.blind_bet)
      break
    elif (player.turn)%(player.num_players) == (player.num_players-1):
      player.blind_(player.players[1], player.players[0], player.blind_bet)
      break

def pre_card_bet(d):
  players_in_play = player.players.copy()
  while player._play_ == True:
    for i in players_in_play[d:]+players_in_play[:d]:
      print(i.cards)
      if i.check == True:
        continue
      else:
        if player.check == True:
          opt_1 = 'Check'
        else: 
          opt_1 = 'Call ' + str(player.bet)
        opt_2 = 'Raise'
        if (i == player.big_blind_player) & (player.big_blind_player.current_bet == player.big_blind_):
          print('1.' ,opt_1)
          print('2.', opt_2)
        else:
          print('1.', opt_1)
          print('2.', opt_2)
          print('3. Fold')
        a = int(input(f"Enter option {i.name}: "))
        if a == 1:
          i.call_()
          if player.check == True:
            print("Check")
          else:
            print("Called ", player.bet)
        elif a == 2:
          b = int(input("Enter bet: "))
          i.bet_(b)
          i.raise_()
          for j in players_in_play:
            if j == i:
              continue
            else:
              j.uncheck_()
          print("Raised to ", (b))
        elif a == 3:
          if (i == player.big_blind_player) & (player.big_blind_player.current_bet == player.big_blind_):
            continue
          else:
            i.fold_()
            print("Folded")
        else:
          continue
        i.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
        print(i.bank)
  for k in player.players:
    k.reset()
  player.reset_cls()
  
def post_card_bet(d):
  players_in_play = player.check_player_play(player.players.copy())
  while player._play_ == True:
    for i in players_in_play[d:]+players_in_play[:d]:
      if i.check == True:
        continue
      else:
        a = int(input(f"Enter option {i.name}: "))
        if a == 1:
          i.call_()
          if player.check == True or player.bet == 0:
            print("Check") 
          else:
            print("Called ", player.bet)
        elif a == 2:
          b = int(input("Enter bet: "))
          i.bet_(b)
          i.raise_()
          for j in players_in_play:
            if j == i:
              continue
            else:
              j.uncheck_()
          print("Raised to ", (b))
        elif a == 3:
          if player.check == False:
            i.fold_()
            print("Folded")
          else:
            continue
        else:
          continue
        i.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
        print(i.bank)
  for k in player.players:
    k.reset()
  player.reset_cls()

p1_name = input("Enter first player: ")
p2_name = input("Enter second player: ")
p3_name = input("Enter third player: ")
bank = int(input("Enter bank: "))
p1 = player(p1_name, bank) 
p2 =  player(p2_name, bank)
p3 = player(p3_name, bank)

while len(player.players) != 1:
  player.set_ante_and_blind_bet()
  player.ante()
  blind_bet()
  k = player.players.index(player.big_blind_player) + 1
  player.distribute_cards()
  player.add_cards()
  pre_card_bet(k)
  player_in_play = player.check_player_play(player.players.copy())
  print(player.table_cards)
