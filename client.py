import socket
import pickle

class Client:
  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "192.168.1.4"
    self.port = 5050
    self.addr = (self.server, self.port)
    self.name = ''
    self.p = self.connect()
    self.players = None
    self.recv_players()

  def getP(self):
    return self.p

  def connect(self):
    name = str(input("Enter a name: "))
    self.name = name
    try:
        self.client.connect(self.addr)
        self.client.send(str.encode(name))
        return pickle.loads(self.client.recv(2048))
    except:
        pass

  def send_state(self):
    data = input('')
    self.p.option = data
    self.client.send(pickle.dumps(self.p))

  def recv_msg(self):
    return pickle.loads(self.client.recv(2048))

  def recv_players(self):
    self.players = pickle.loads(self.client.recv(2048))
    self.show_status()

  def show_status(self):
    for i in self.players:
      if i.name == self.name:
          if i.cards == None:
            print(i.name, i.bank)
          else:
            print(i.name, i.cards, i.bank)
      else:
        print(i.name, i.bank)

  def handle_msg(self, mesg):
    if mesg['id'] == 0:
      self.players = mesg['players']
      for i in self.players:
        if i.name == self.name:
          self.p.cards = i.cards
      self.show_status()
    elif mesg['id'] == 1:
      recv_msg = mesg['message']
      print(recv_msg)
    elif mesg['id'] == 2:
      if mesg['msg'] == 'bet-1':
        print(self.p.cards)
        print('1. ', mesg['params'])
        print('2. Raise')
        print('Enter option:', end=' ')
        self.send_state()
      elif mesg['msg'] == 'bet-1a':
        print(mesg['params']['list'])
        print(self.p.cards)
        print('1. ', mesg['params']['opt'])
        print('2. Raise')
        print('Enter option:', end=' ')
        self.send_state()
      elif mesg['msg'] == 'bet-2':
        print(self.p.cards)
        print('1. ', mesg['params'])
        print('2. Raise')
        print('3. Fold')
        print('Enter option:', end=' ')
        self.send_state()
      elif mesg['msg'] == 'bet-2a':
        print(mesg['params']['list'])
        print(self.p.cards)
        print('1. ', mesg['params']['opt'])
        print('2. Raise')
        print('3. Fold')
        print('Enter option:', end=' ')
        self.send_state()
      elif mesg['msg'] == 'bet-3':
        print('Enter bet:', end=' ')
        self.send_state()
      elif mesg['msg'] == 'broke':
        print('1. Rebought')
        print('2. Spectate Table')
        print('3. Leave Table')
        print('Enter option:', end=' ')
        self.send_state()
    elif mesg['id'] == 22:
      if mesg['msg'] == 'bet-res-1':
        print(mesg['name'], ': Checked')
      elif mesg['msg'] == 'bet-res-2':
        print(mesg['name'], ': Called ', mesg['params'])
      elif mesg['msg'] == 'bet-res-3':
        print(mesg['name'], ': Raised to ', mesg['params'])
      elif mesg['msg'] == 'bet-res-4':
        print(mesg['name'], ': Folded')
      elif mesg['msg'] == 'res-1':
        print(mesg['name'], ': Wins pot of ', msg['params'])
      elif mesg['msg'] == 'res-2':
        print('Tie between:', end=' ')
        for i in  mesg['params']['players']:
          print(i, end=' ')
        print('Split Pot: ', mesg['params']['amt'])
      elif mesg['msg'] == 'broke-res-1':
        print(mesg['name'], ': Rebought')
      elif mesg['msg'] == 'broke-res-2':
        print(mesg['name'], ': Spectating')
      elif mesg['msg'] == 'broke-res-3':
        print(mesg['name'], ': Left the table')
    elif mesg['id'] == 3:
      inp_statement = mesg['inp_statement']
      print(inp_statement, end = ' ')
      while True:
        try:
          self.send_state()
          break
        except:
          continue
    else:
      print('didnt match')

n = Client()
while True:
  try:
    msg = n.recv_msg()
    n.handle_msg(msg)
    continue
  except:
    continue