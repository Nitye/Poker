from players import player
import cards as nc
import random
import pickle

class Game:
  @classmethod
  def send_players(cls, g):
    print(g.players[0].name, g.players[1].name, g.players[2].name)
    print(g.players[0].name, g.players[0].cards)
    print(g.players[1].name, g.players[1].cards)
    print(g.players[2].name, g.players[2].cards)
    for i in g.players:
      g.clients[i.name]['conn'].sendall(pickle.dumps({'id': 0, 'players': g.sendable_players}))

  @classmethod
  def send_str(cls, g, i, data):
    g.clients[i.name]['conn'].sendall(pickle.dumps({'id': 1, 'message': data}))

  @classmethod
  def send_str_all(cls, g, data):
    for i in g.players:
      g.clients[i.name]['conn'].sendall(pickle.dumps({'id': 1, 'message': data}))
  
  @classmethod
  def send_dict(cls, g, i, msg, params):
    g.clients[i.name]['conn'].sendall(pickle.dumps({'id': 2,'msg':msg, 'params':params}))

  @classmethod
  def send_dict_all(cls, g, name, msg, params=''):
    for i in g.players:
      g.clients[i.name]['conn'].sendall(pickle.dumps({'id': 22, 'name': name, 'msg':msg, 'params':params}))

  # @classmethod
  # def get_input(cls, g, i, inp_statement):
  #   g.clients[i.name]['conn'].sendall(pickle.dumps({'id':3, 'inp_statement': inp_statement}))
  #   while True:
  #     try:
  #       return g.clients[i.name]['conn'].recv(64).decode()
  #     except:
  #       pass

  @classmethod
  def blind_bet_(cls, g):
    for i in range(g.num_players):
      if (g.turn)%(g.num_players)==i & i < (g.num_players-2):
        g.blind_(g.players[i+2], g.players[i+1], g.blind_bet)
        break
      elif (g.turn)%(g.num_players) == (g.num_players-2):
        g.blind_(g.players[0], g.players[-1], g.blind_bet)
        break
      elif (g.turn)%(g.num_players) == (g.num_players-1):
        g.blind_(g.players[1], g.players[0], g.blind_bet)
        break
    for i in g.sendable_players:
      i.update(g.clients[i.name]['player_obj'])

  @classmethod
  def pre_card_bet(cls, g):
    players_in_play = g.players.copy()
    d = g.players.index(g.player_in_turn)
    while g._play_ == True:
      for i in players_in_play[d:]+players_in_play[:d]:
        if g.max_folds != len(g.players)-1:
          if i.check == True:
            continue
          else:
            print(i.cards)
            if g.bet-i.current_bet == 0: 
              opt_1 = 'Check'
            else:
              opt_1 = 'Call ' + str(g.bet-i.current_bet)
            if (i == g.big_blind_player) & (g.bet == g.blind_bet):
              print('1.' ,opt_1)
              print('2. Raise')
              Game.send_dict(g, i, 'bet-1', opt_1)
            else:
              print('1.', opt_1)
              print('2. Raise')
              print('3. Fold')
              Game.send_dict(g, i, 'bet-2', opt_1)
            g.clients[i.name]['sendable_player_obj'] = pickle.loads(g.clients[i.name]['conn'].recv(2048))
            a = int(g.clients[i.name]['sendable_player_obj'].option)
            print(a)
            if a == 1:
              g.player_in_turn = i
              i.call_()
              if g.check == True:
                print(i.name, ": Checked")
                Game.send_dict_all(g, i.name, 'bet-res-1')
              else:
                print(i.name, ": Called ", g.bet)
                Game.send_dict_all(g, i.name, 'bet-res-2', g.bet)
            elif a == 2:
              Game.send_dict(g, i, 'bet-3', '')
              g.player_in_turn = i
              g.clients[i.name]['sendable_player_obj'] = pickle.loads(g.clients[i.name]['conn'].recv(2048))
              b = int(g.clients[i.name]['sendable_player_obj'].option)
              i.bet_(b)
              i.raise_()
              for j in players_in_play:
                if j == i:
                  continue
                else:
                  j.uncheck_()
              print(i.name, ": Raised to ", (b))
              Game.send_dict_all(g, i.name, 'bet-res-3', b)
            elif a == 3:
              c = g.players.index(i)
              if c < len(g.players)-1:
                g.player_in_turn = g.players[c+1]
              else:
                g.player_in_turn = g.players[0]
              if (i == g.big_blind_player) & (g.bet == g.blind_bet):
                continue
              else:
                i.fold_()
                print(i.name, ": Folded")
                Game.send_dict_all(g, i.name, 'bet-res-4')
            else:
              print('not_working')
            print(i.bank)
        else:
          for j in players_in_play:
            j.check_check_()
          for i in g.sendable_players:
            i.update(g.clients[i.name]['player_obj'])
          Game.send_players(g)
          players_in_play = g.check_player_play(players_in_play)
          g.check_play_(players_in_play)
          break
        for j in players_in_play:
          j.check_check_()
        for i in g.sendable_players:
          i.update(g.clients[i.name]['player_obj'])
        Game.send_players(g)
        players_in_play = g.check_player_play(players_in_play)
        g.check_play_(players_in_play)
    for k in g.players:
      k.reset()
    g.reset_cls()
    
  @classmethod
  def post_card_bet(cls, players_in_play, turn, g):
    if turn == 'a':
      l1 = g.table_cards[:3]
    elif turn == 'b':
      l1 = g.table_cards[:4]
    elif turn == 'c':
      l1 = g.table_cards
    d = g.players.index(g.player_in_turn)
    while g._play_ == True:
      if len(players_in_play) > 1:
        for i in players_in_play[d:]+players_in_play[:d]:
          if g.max_folds != g.num_players-1:
            if i.check == True:
              continue
            else:
              print(l1)
              print(i.cards)
              if g.check == True:
                opt_1 = 'Check'
              else: 
                if g.bet-i.current_bet == 0:
                  opt_1 = 'Check'
                else:
                  opt_1 = 'Call ' + str(g.bet-i.current_bet)
              print('1. ', opt_1)
              print("2. Raise")
              if g.bet == 0:
                m = str('bet-1' + turn)
                Game.send_dict(g, i, m, opt_1)
                pass
              else:
                print('3. Fold')
                m = str('bet-2' + turn)
                Game.send_dict(g, i, m, opt_1)
              g.clients[i.name]['sendable_player_obj'] = pickle.loads(g.clients[i.name]['conn'].recv(2048))
              a = int(g.clients[i.name]['sendable_player_obj'].option)
              if a == 1:
                g.player_in_turn = i
                i.call_()
                if g.check == True or g.bet == 0:
                  print("Check")
                  Game.send_dict_all(g, i.name, 'bet-res-1') 
                else:
                  print("Called ", g.bet)
                  Game.send_dict_all(g, i.name, 'bet-res-2', g.bet)
              elif a == 2:
                Game.send_dict(g, i, 'bet-3', '')
                g.player_in_turn = i
                g.clients[i.name]['sendable_player_obj'] = pickle.loads(g.clients[i.name]['conn'].recv(2048))
                b = int(g.clients[i.name]['sendable_player_obj'].option)
                i.bet_(b)
                i.raise_()
                for j in players_in_play:
                  if j == i:
                    continue
                  else:
                    j.uncheck_()
                print("Raised to ", (b))
                Game.send_dict_all(g, i.name, 'bet-res-3', b)
              elif a == 3:
                c = players_in_play.index(i)
                if c < len(players_in_play)-1:
                  g.player_in_turn = players_in_play[c+1]
                else:
                  g.player_in_turn = players_in_play[0]
                if g.check == False:
                  i.fold_()
                  print("Folded")
                  Game.send_dict_all(g, i.name, 'bet-res-4')
                else:
                  continue
              else:
                continue
              print(i.bank)
          else:
            for j in players_in_play:
              j.check_check_()
            for i in g.sendable_players:
              i.update(g.clients[i.name]['player_obj'])
            Game.send_players(g)
            players_in_play = g.check_player_play(players_in_play)
            g.check_play_(players_in_play)
            break
          for j in players_in_play:
            j.check_check_()
          for i in g.sendable_players:
            i.update(g.clients[i.name]['player_obj'])
          Game.send_players(g)
          players_in_play = g.check_player_play(players_in_play)
          g.check_play_(players_in_play)
      else:
        break
    for k in g.players:
      k.reset()
    g.reset_cls()

  @classmethod
  def add_score_for_all(cls, players_in_play, g):
    for i in players_in_play:
      i.add_score()
      g.player_scores[i] = i.score

  @classmethod
  def compare_score(cls, player_scores, players_in_play, g):
    max_score = max(player_scores.values())
    d = nc.remove_dup_list(player_scores.values())[1]
    if d[max(d.keys())] == 1:
      for z in players_in_play:
        if max_score == player_scores[z]:
          print(f"{z.name} wins")
          Game.send_dict_all(g, z.name, 'res-1', g.pot)
          z.win_(players_in_play)
          g.player_scores.pop(z)
    else:
      draw_winnings = g.draw_winnings_(d[max(d.keys())])
      draw_players = []
      for y in players_in_play:
        if y.score == max(d.keys()):
          draw_players.append(y.name) 
          y.draw_(draw_winnings)
      Game.send_dict_all(g, y.name, 'res-2', {'amt':draw_winnings, 'players':draw_players})  
      print('Draw between:', end=' ')
      for i in draw_players:
        print(i, end =' ')

  def __init__(self, num_players, bank):
    self.id = 0
    self.num_players = num_players
    self.clients = {}
    self.players = []
    self.sendable_players = []
    self.deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
        '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
          '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']
    self.pot = 0
    self.turn = 0
    self.bet = 0
    self._play_ = True
    self.check = True
    self.big_blind_player = None
    self.player_in_turn = None
    self.max_folds = 0
    self._bank_ = bank
    self.table_cards = None
    self.blind_bet = 0
    self.an = 0
    self.player_scores = {}
    self.hands = []
    self.broke_players = {}
    self.all_in_players = []
    self.all_in_num = 0
    print(f'Game initiated with {num_players} players and Bank: {bank}')
    print('Waiting for players...')

  def reset_cls(self):
    self._play_ = True
    self.bet = 0
    self.deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
      '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
        '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
          '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']

  def draw_winnings_(self, num_people):
    self.turn += 1
    return self.pot/num_people

  def set_ante_and_blind_bet(cls):
    c = cls._bank_//50
    _ = cls._bank_//200
    blind_bets = [c*a for a in range(1,6)]
    antes = [_*a for a in range(1,6)]
    if cls.turn <= 5:
      cls.blind_bet = round(blind_bets[0])
      cls.an = round(antes[0])
    elif cls.turn <= 10:
      cls.blind_bet = round(blind_bets[1])
      cls.an = round(antes[1])
    elif cls.turn <= 15:
      cls.blind_bet = round(blind_bets[2])
      cls.an = round(antes[2])
    elif cls.turn <= 20:
      cls.blind_bet = round(blind_bets[3])
      cls.an = round(antes[3])
    else:
      cls.blind_bet = round(blind_bets[4])
      cls.an = round(antes[4])

  def check_player_play(self, players_in_play):
    p = []
    for i in players_in_play:
      if not i.play or i.all_in: 
        p.append(i)
    for j in p:
      players_in_play.remove(j)
    return players_in_play
  
  def check_play_(self, players_in_play):
    c = 0
    for i in players_in_play:
      if i.check == True:
        c+=1
      else:
        pass
    if len(players_in_play) != 1:
      if c == len(players_in_play):
        self._play_ = False
      else:
        self._play_ = True
    else:
      self._play_ = False

  def blind_(self, player1, player2, blind_bet):
    self.bet = blind_bet
    player1.big_blind_(blind_bet)
    player2.small_blind_(blind_bet)

  def reset_all_(self):
    for i in self.players:
      i.reset()

  def reset_play_for_all(self):
    for i in self.players:
      i.play = True

  def draw_cards(self, num):
    a = 0
    dummy_hand = []
    while a < num:
      card_a = random.choice(self.deck)
      removed_card_index = self.deck.index(card_a)
      self.deck.pop(removed_card_index)
      a+=1
      dummy_hand.append(card_a)
    return dummy_hand

  def distribute_cards(self):
    card_num = (self.num_players*2) + 5
    chosen_cards = self.draw_cards(card_num)
    b = 0
    while b < self.num_players:
      self.hands.append(chosen_cards[2*b:2*(b+1)])
      b+=1
    self.table_cards = chosen_cards[2*self.num_players:]

  def add_cards(self):
    i = 0
    for j in self.players:
      j.cards = self.hands[i]
      j.table = self.table_cards
      i+=1

  def remove_cards(self):
    for j in self.players:
      j.cards = None

  def ante(self):
    for k in self.players:
      self.pot+=self.an
      k.bank-=self.an

  def check_broke(self):
    for i in self.players:
      if i.bank <= 0:
        self.broke_players[self.players.index(i)] = i
      else:
        continue
    for j in list(self.broke_players.values()):
      self.players.remove(j)

  def broke_unbroke(self):
    if len(self.broke_players) != 0:
      p = []
      for i in list(self.broke_players.keys()):
        print("1. Rebuy")
        print("2. Spectate")
        print("3. Leave Table")
        b = 0
        while b == 0:
          a = int(input(f"Enter option {self.broke_players[i].name}: "))
          if a == 1:
            print("Rebought")
            self.players.insert(i, self.broke_players[i])
            p.append(i)
            self.players[i].bank+=self._bank_
            b = 1
          elif a == 2:
            del self.broke_players[i]
            self.num_players-=1
            print("Spectating")
            b = 1
          elif a == 3:
            self.num_players-=1
            b = 1
          else:
            pass
      for k in p:
        del self.broke_players[k]
      p.clear()
