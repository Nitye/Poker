from new_players import player
import new_cards as nc

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

def pre_card_bet(player_in_turn):
  players_in_play = player.players.copy()
  d = player.players.index(player_in_turn)
  for i in players_in_play[d:]+players_in_play[:d]:
    print(i.cards)
    while player._play_ == True:
      if i.check == True:
        break
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
  
def post_card_bet(player_in_turn, players_in_play):
  d = player.players.index(player_in_turn)
  for i in players_in_play[d:]+players_in_play[:d]:
    print(i.cards)
    while player._play_ == True:
      if i.check == True:
        break
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

def add_score_for_all(players_in_play):
  for i in players_in_play:
    i.add_score()
    player.player_scores[i] = i.score

def compare_score(player_scores, players_in_play):
  max_score = max(player_scores.values())
  d = nc.remove_dup_list(player_scores.values())[1]
  if d[max(d.keys())] == 1:
    for z in players_in_play:
      if max_score == player_scores[z]:
        print(f"{z.name} wins")
        z.win_(players_in_play)
        player.player_scores.pop(z)
  else:
    draw_winnings = player.draw_winnings_(d[max(d.keys())])
    for y in players_in_play:
      if y.score == max(d.keys()):
        y.draw_(draw_winnings)
    print('Draw')

p1_name = input("Enter first player: ")
p2_name = input("Enter second player: ")
p3_name = input("Enter third player: ")
bank = int(input("Enter bank: "))
p1 = player(p1_name, bank) 
p2 =  player(p2_name, bank)
p3 = player(p3_name, bank)

while True:
  player.set_ante_and_blind_bet()
  player.ante()
  blind_bet()
  k = player.players.index(player.big_blind_player) + 1
  if k < player.num_players:
    pass
  else:
    k = 0
  player_in_turn = player.players[k]
  player.distribute_cards()
  player.add_cards()
  pre_card_bet(player_in_turn)
  print("End of Pre-Flop Bet")
  players_in_play = player.check_player_play(player.players.copy())
  while True:
    if len(players_in_play) != 1:
      print(player.table_cards[0:3])
      post_card_bet(player_in_turn, players_in_play)
      players_in_play = player.check_player_play(player.players.copy())
      if len(players_in_play) != 1:
        print(player.table_cards[:4])
        post_card_bet(player_in_turn, players_in_play)
        players_in_play = player.check_player_play(player.players.copy())
        if len(players_in_play) != 1:
          print(player.table_cards)
          post_card_bet(player_in_turn, players_in_play)
          players_in_play = player.check_player_play(player.players.copy())
          break
        else:
          break
      else:
        break
    else:
      break
  if len(players_in_play) == 1:
    print(players_in_play[0].name, " wins")
    players_in_play[0].win_(players_in_play)
  else:
    add_score_for_all(players_in_play)
    while player.pot != 0:
      compare_score(player.player_scores, players_in_play)
      players_in_play = player.check_player_play(players_in_play)
    player.remove_cards()
