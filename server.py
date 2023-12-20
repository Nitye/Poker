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
print('Server started, listening for connections...')

def handle_client(name, g):
  msg = g.clients[name]['conn'].recv(header).decode(format)
  if msg == disc_msg:
    g.clients[name]['conn'].close()
    msg = 'Disconnected'
  print(f"[{name}]: {msg}")

def start(num, bank):
  s.listen(num)
  g = Game(num, bank)
  while len(g.players) < g.num_players:
    conn, addr = s.accept()
    name = conn.recv(2048).decode(format)
    p = player(name, g._bank_, g)
    send_p = sendable_player(p)
    g.players.append(p)
    g.sendable_players.append(send_p)
    print(f"New Connection {name} connected")
    g.clients[name] = dict()
    g.clients[name]['addr'] = addr
    g.clients[name]['conn'] = conn
    g.clients[name]['player_obj'] = p
    g.clients[name]['sendable_player_obj'] = send_p
    conn.send(pickle.dumps(send_p))
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