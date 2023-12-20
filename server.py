import socket
import pickle
from game import Game
from players import player

g = Game()

b = int(input("Enter number of people: "))
bank = int(input("Enter bank: "))
for a in range(b):
  s = str("Enter player " + str(a+1) + ": ")
  name = input(s)
  player(name, bank, g)

while True:
  g.hands = []
  g.big_blind_player = None
  g.set_ante_and_blind_bet()
  g.ante()
  Game.blind_bet(g)
  k = g.players.index(g.big_blind_player) + 1
  if k < g.num_players:
    pass
  else:
    k = 0
  g.player_in_turn = g.players[k]
  g.distribute_cards()
  g.add_cards()
  Game.pre_card_bet(g)
  print("End of Pre-Flop Bet")
  players_in_play = g.check_player_play(g.players.copy())
  Game.post_card_bet(players_in_play, 1, g)
  print('Turn 1 done')
  players_in_play = g.check_player_play(players_in_play)
  Game.post_card_bet(players_in_play, 2, g)
  print('Turn 2 done')
  players_in_play = g.check_player_play(players_in_play)
  Game.post_card_bet(players_in_play, 3, g)
  print('Turn 3 done')
  players_in_play = g.check_player_play(players_in_play)
  players_in_play = list(set(players_in_play + g.all_in_players))
  if len(players_in_play) == 1:
      print(players_in_play[0].name, " wins")
      players_in_play[0].win_(players_in_play)
  else:
    Game.add_score_for_all(players_in_play, g)
    while g.pot != 0:
      Game.compare_score(g.player_scores, players_in_play)
      players_in_play = g.check_player_play(players_in_play)
  g.remove_cards()
  g.check_broke()
  g.broke_unbroke()
  if len(g.players) < 2:
    break
  else:
    pass