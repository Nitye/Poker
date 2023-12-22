import socket
import pickle
from game import Game
from players import player, sendable_player

header = 64
server = "192.168.1.4"
port = 5050
addr = (server, port)
format = 'utf-8'
disc_msg = 'Disconnect'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
print('Server started')

def start(num, bank):
  g = Game(num, bank)
  s.listen(num)
  while len(g.players) < g.num_players:
    conn, addr = s.accept()
    name = conn.recv(2048).decode(format)
    p = player(name, g._bank_, g)
    send_p = sendable_player(p)
    g.players.append(p)
    g.sendable_players.append(send_p)
    print(f"New Player {name} connected")
    g.clients[name] = dict()
    g.clients[name]['addr'] = addr
    g.clients[name]['conn'] = conn
    g.clients[name]['player_obj'] = p
    g.clients[name]['sendable_player_obj'] = send_p
    conn.sendall(pickle.dumps(send_p))
  print(g.sendable_players[0].name, g.sendable_players[1].name, g.sendable_players[2].name)
  for i in g.players:
    g.clients[i.name]['conn'].sendall(pickle.dumps(g.sendable_players))
  return g

g = start(3, 1000)
while True:
  g.hands = []
  g.big_blind_player = None
  g.set_ante_and_blind_bet()
  g.ante()
  Game.blind_bet_(g)
  k = g.players.index(g.big_blind_player) + 1
  if k < g.num_players:
    pass
  else:
    k = 0
  g.player_in_turn = g.players[k]
  g.distribute_cards()
  g.add_cards()
  for i in g.sendable_players:
    i.update(g.clients[i.name]['player_obj'])
  Game.send_players(g)
  Game.pre_card_bet(g)
  print("End of Pre-Flop Bet")
  Game.send_str_all(g, 'End of Pre-Flop Bet')
  players_in_play = g.check_player_play(g.players.copy())
  Game.post_card_bet(players_in_play, 'a', g)
  print('Turn 1 betting done')
  Game.send_str_all(g, 'Turn 1 betting done')
  players_in_play = g.check_player_play(players_in_play)
  Game.post_card_bet(players_in_play, 'b', g)
  print('Turn 2 betting done')
  Game.send_str_all(g, 'Turn 2 betting done')
  players_in_play = g.check_player_play(players_in_play)
  Game.post_card_bet(players_in_play, 'c', g)
  print('Turn 3 betting done')
  Game.send_str_all(g, 'Turn 3 betting done')
  players_in_play = g.check_player_play(players_in_play)
  players_in_play = list(set(players_in_play + g.all_in_players))
  if len(players_in_play) == 1:
      print(players_in_play[0].name, " wins")
      players_in_play[0].win_(players_in_play)
  else:
    Game.add_score_for_all(players_in_play, g)
    while g.pot != 0:
      Game.compare_score(g.player_scores, players_in_play, g)
      players_in_play = g.check_player_play(players_in_play)
  g.remove_cards()
  Game.send_players(g)
  g.check_broke()
  g.broke_unbroke()
  Game.send_players(g)
  if len(g.players) < 2:
    break
  else:
    pass