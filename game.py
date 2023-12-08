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

def pre_card_bet():
  players_in_play = player.players.copy()
  d = player.players.index(player.player_in_turn)
  while player._play_ == True:
    for i in players_in_play[d:]+players_in_play[:d]:
      if player.max_folds != len(player.players)-1:
        if i.check == True:
          continue
        else:
          print(i.cards)
          if player.bet-i.current_bet == 0: 
            opt_1 = 'Check'
          else:
            opt_1 = 'Call ' + str(player.bet-i.current_bet)
          if (i == player.big_blind_player) & (player.bet == player.blind_bet):
            print('1.' ,opt_1)
            print('2. Raise')
          else:
            print('1.', opt_1)
            print('2. Raise')
            print('3. Fold')
          a = int(input(f"Enter option {i.name}: "))
          if a == 1:
            player.player_in_turn = i
            i.call_()
            if player.check == True:
              print("Check")
            else:
              print("Called ", player.bet)
          elif a == 2:
            player.player_in_turn = i
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
            c = player.players.index(i)
            if c < len(player.players)-1:
              player.player_in_turn = player.players[c+1]
            else:
              player.player_in_turn = player.players[0]
            if (i == player.big_blind_player) & (player.bet == player.blind_bet):
              continue
            else:
              i.fold_()
              print("Folded")
          else:
            continue
          print(i.bank)
      else:
        for j in players_in_play:
          j.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
        break
      for j in players_in_play:
        j.check_check_()
      players_in_play = player.check_player_play(players_in_play)
      player.check_play_(players_in_play)
  for k in player.players:
    k.reset()
  player.reset_cls()
  
def post_card_bet(players_in_play, turn):
  if turn == 1:
    l1 = player.table_cards[:3]
  elif turn == 2:
    l1 = player.table_cards[:4]
  else:
    l1 = player.table_cards
  d = player.players.index(player.player_in_turn)
  while player._play_ == True:
    if len(players_in_play) > 1:
      for i in players_in_play[d:]+players_in_play[:d]:
        if player.max_folds != player.num_players-1:
          if i.check == True:
            continue
          else:
            print(l1)
            print(i.cards)
            if player.check == True:
              opt_1 = 'Check'
            else: 
              if player.bet-i.current_bet == 0:
                opt_1 = 'Check'
              else:
                opt_1 = 'Call ' + str(player.bet-i.current_bet)
            print('1. ', opt_1)
            print("2. Raise")
            if player.bet == 0:
              pass
            else:
              print('3. Fold')
            a = int(input(f"Enter option {i.name}: "))
            if a == 1:
              player.player_in_turn = i
              i.call_()
              if player.check == True or player.bet == 0:
                print("Check") 
              else:
                print("Called ", player.bet)
            elif a == 2:
              player.player_in_turn = i
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
              c = players_in_play.index(i)
              if c < len(players_in_play)-1:
                player.player_in_turn = players_in_play[c+1]
              else:
                player.player_in_turn = players_in_play[0]
              if player.check == False:
                i.fold_()
                print("Folded")
              else:
                continue
            else:
              continue
            print(i.bank)
        else:
          for j in players_in_play:
            j.check_check_()
          players_in_play = player.check_player_play(players_in_play)
          player.check_play_(players_in_play)
          break
        for j in players_in_play:
          j.check_check_()
        players_in_play = player.check_player_play(players_in_play)
        player.check_play_(players_in_play)
    else:
      break
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

b = int(input("Enter number of people: "))
bank = int(input("Enter bank: "))
for a in range(b):
  s = str("Enter player " + str(a+1) + ": ")
  name = input(s)
  player(name, bank)

while True:
  player.hands = []
  player.big_blind_player = None
  player.set_ante_and_blind_bet()
  player.ante()
  blind_bet()
  k = player.players.index(player.big_blind_player) + 1
  if k < player.num_players:
    pass
  else:
    k = 0
  player.player_in_turn = player.players[k]
  player.distribute_cards()
  player.add_cards()
  pre_card_bet()
  print("End of Pre-Flop Bet")
  players_in_play = player.check_player_play(player.players.copy())
  post_card_bet(players_in_play, 1)
  print('Turn 1 done')
  players_in_play = player.check_player_play(players_in_play)
  post_card_bet(players_in_play, 2)
  print('Turn 2 done')
  players_in_play = player.check_player_play(players_in_play)
  post_card_bet(players_in_play, 3)
  print('Turn 3 done')
  players_in_play = player.check_player_play(players_in_play)
  players_in_play = list(set(players_in_play + player.all_in_players))
  if len(players_in_play) == 1:
      print(players_in_play[0].name, " wins")
      players_in_play[0].win_(players_in_play)
  else:
    add_score_for_all(players_in_play)
    while player.pot != 0:
      compare_score(player.player_scores, players_in_play)
      players_in_play = player.check_player_play(players_in_play)
  player.remove_cards()
  player.check_broke()
  player.broke_unbroke()