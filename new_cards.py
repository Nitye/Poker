deck = ['♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K',
         '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
           '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
             '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K']
suit_symbols = ['\u2660', '\u2663', '\u2665', '\u2666']

suits={'Spades':deck[0:13], 'Clubs': deck[13:26], 
       'Hearts': deck[26:39], 'Dimmaonds' : deck[39:]}

num_cards = ['A', 'K', 'Q', 'J', '1',
              '9', '8', '7', '6', '5', '4', '3', '2']

card_score ={'A': 14, 'K': 13, 'Q': 12, 'J': 11,
              '1': 10, '9': 9, '8': 8, '7': 7, '6': 6,
                '5': 5, '4': 4, '3': 3, '2': 2}

straight_patterns = [['A','K','Q','J','1'], ['K','Q','J','1','9'], ['Q','J','1','9','8'], ['J','1','9','8','7'], ['1','9','8','7','6'],
                      ['9','8','7','6','5'], ['8','7','6','5','4'], ['7','6','5','4','3'],
                        ['6','5','4','3','2'], ['5','4','3','2','A']]

straight_flush_patterns = [[['\u2660A','\u2660K','\u2660Q','\u2660J','\u26601'], ['\u2660K','\u2660Q','\u2660J','\u26601','\u26609'], ['\u2660Q','\u2660J','\u26601','\u26609','\u26608'], ['\u2660J','\u26601','\u26609','\u26608','\u26607'], ['\u26601','\u26609','\u26608','\u26607','\u26606'],
                      ['\u26609','\u26608','\u26607','\u26606','\u26605'], ['\u26608','\u26607','\u26606','\u26605','\u26604'], ['\u26607','\u26606','\u26605','\u26604','\u26603'],
                        ['\u26606','\u26605','\u26604','\u26603','\u26602'], ['\u26605','\u26604','\u26603','\u26602','\u2660A']],
                          [['\u2663A','\u2663K','\u2663Q','\u2663J','\u26631'], ['\u2663K','\u2663Q','\u2663J','\u26631','\u26639'], ['\u2663Q','\u2663J','\u26631','\u26639','\u26638'], ['\u2663J','\u26631','\u26639','\u26638','\u26637'], ['\u26631','\u26639','\u26638','\u26637','\u26636'],
                      ['\u26639','\u26638','\u26637','\u26636','\u26635'], ['\u26638','\u26637','\u26636','\u26635','\u26634'], ['\u26637','\u26636','\u26635','\u26634','\u26633'],
                        ['\u26636','\u26635','\u26634','\u26633','\u26632'], ['\u26635','\u26634','\u26633','\u26632','\u2663A']],
                          [['\u2665A','\u2665K','\u2665Q','\u2665J','\u26651'], ['\u2665K','\u2665Q','\u2665J','\u26651','\u26659'], ['\u2665Q','\u2665J','\u26651','\u26659','\u26658'], ['\u2665J','\u26651','\u26659','\u26658','\u26657'], ['\u26651','\u26659','\u26658','\u26657','\u26656'],
                      ['\u26659','\u26658','\u26657','\u26656','\u26655'], ['\u26658','\u26657','\u26656','\u26655','\u26654'], ['\u26657','\u26656','\u26655','\u26654','\u26653'],
                        ['\u26656','\u26655','\u26654','\u26653','\u26652'], ['\u26655','\u26654','\u26653','\u26652','\u2665A']],
                          [['\u2666A','\u2666K','\u2666Q','\u2666J','\u26661'], ['\u2666K','\u2666Q','\u2666J','\u26661','\u26669'], ['\u2666Q','\u2666J','\u26661','\u26669','\u26668'], ['\u2666J','\u26661','\u26669','\u26668','\u26667'], ['\u26661','\u26669','\u26668','\u26667','\u26666'],
                      ['\u26669','\u26668','\u26667','\u26666','\u26665'], ['\u26668','\u26667','\u26666','\u26665','\u26664'], ['\u26667','\u26666','\u26665','\u26664','\u26663'],
                        ['\u26666','\u26665','\u26664','\u26663','\u26662'], ['\u26665','\u26664','\u26663','\u26662','\u2666A']]]

royal_flush_patterns =  [[['\u2660A','\u2660K','\u2660Q','\u2660J','\u26601']],
                          [['\u2663A','\u2663K','\u2663Q','\u2663J','\u26631']],
                          [['\u2665A','\u2665K','\u2665Q','\u2665J','\u26651']],
                          [['\u2666A','\u2666K','\u2666Q','\u2666J','\u26661']]]

def num_of_a_kind(num, card, list1):
  list1_count = 0
  for i in range(0,7):
    for j in range(0,2):
      if list1[i][j] == card:
        list1_count+=1
      else: 
        pass
  if list1_count == num:
    result = True
  else:
    result = False
  return result

def royal_flush(player,player_score):
  list1 = [player[i] for i in range(7)]
  royal_flush_bool = False
  score = 120000
  for m in royal_flush_patterns:
    for j in m:
      l = 0
      for k in range(5):
        if j[k] in list1:
          l+=1
        else: 
          pass
      if l == 5:
        royal_flush_bool = True
        player_score+=score
  return [player_score, royal_flush_bool]

def straight_flush(player, player_score):
  list1 = []
  straight_flush_bool = False
  for i in range(0,7):
    list1.append(player[i])
  for m in straight_flush_patterns:
    score=100
    for j in m:
      l = 0
      for k in range(0,5):
        if j[k] in list1:
          l+=1
        else: 
          pass
      if l == 5:
        straight_flush_bool = True
        player_score+=score
      score-=1
  return([player_score, straight_flush_bool])

def four_of_a_kind(player, player_score):
  four_of_a_kind_bool = True
  card = []
  for i in num_cards:
    if num_of_a_kind(4, i, player):
      player_score+=card_score[i]
      card.append(i)
  if len(card) == 0:
    four_of_a_kind_bool = False
  return [player_score, card, four_of_a_kind_bool]

def full_house(player, player_score):
  cards = {}
  full_house_bool = False
  three_list = three_of_a_kind(player, 0)
  pair_list = pair(player, 0)
  if three_list[2] & pair_list[2]:
    cards['three'] = three_list[1][0]
    cards['two'] = pair_list[1][0]
    cards['three_score'] = card_score[three_list[1][0]]
    cards['two_score'] = card_score[pair_list[1][0]]
    full_house_bool = True
  return [cards, full_house_bool]

def flush(player, player_score):
  flush_bool = True
  suit = []
  flush_to_card = []
  b = 0
  for i in suit_symbols:
    if num_of_a_kind(5, i, player):
      suit.append(i)
  if len(suit) == 0:
    flush_bool = False
  else:
    for j in player:
      if j[0] == suit[0]:
        if card_score[j[1]] > b:
          b = card_score[j[1]]
          flush_to_card.append(j[1])
  return [player_score, suit, flush_bool, flush_to_card]

def straight(player, player_score):
  list1 = []
  score = 10
  straight_bool = False
  for i in range(0,7):
    list1.append(player[i][1])
  for j in straight_patterns:
    l = 0
    for k in range(0,5):
      if j[k] in list1:
        l+=1
      else: 
        pass
    if l == 5:
      straight_bool = True
      player_score+=score*10
      break
    score-=1
  return([player_score, straight_bool])

def three_of_a_kind(player, player_score):
  three_of_a_kind_bool = True
  card = []
  for i in num_cards:
    if num_of_a_kind(3, i, player):
      player_score+=card_score[i]
      card.append(i)
  if len(card) == 0:
    three_of_a_kind_bool = False
  return [player_score, card, three_of_a_kind_bool]

def two_pair(player, player_score):
  pair_list = pair(player, player_score)
  player_score = 0
  two_pair_bool = False
  cards = []
  if len(pair_list[1]) >= 2:
    two_pair_bool = True
    cards.append(pair_list[1][0])
    cards.append(pair_list[1][1])
    player_score += card_score[pair_list[1][0]]
    player_score += card_score[pair_list[1][1]]
  else:
    pass
  return [player_score, cards, two_pair_bool]

def pair(player, player_score):
  pair_bool = True
  card = []
  for i in num_cards:
    if num_of_a_kind(2, i, player):
      player_score+=card_score[i]
      card.append(i)
  if len(card) == 0:
    pair_bool = False
  return [player_score, card, pair_bool]

def remove_duplicates(player):
  four_list = four_of_a_kind(player, 0)
  three_list = three_of_a_kind(player, 0)
  pair_list = pair(player, 0)
  two_pair_list = two_pair(player, 0)
  royal_flush_list = royal_flush(player, 0)
  straight_flush_list = straight_flush(player, 0)
  flush_list = flush(player,  0)
  straight_list = straight(player, 0)
  full_house_list = full_house(player, 0)
  if royal_flush_list[1]:
    straight_flush_list[1] = False
    straight_list[1] = False
    flush_list[2] = False
  elif straight_flush_list[1]:
    straight_list[1] = False
    flush_list[2] = False
  if full_house_list[1]:
    three_list[2] = False
    if len(pair_list[1]) == 1:
      pair_list[2] = False
      two_pair_list[2] = False
    elif len(pair_list[1]) >= 2:
      two_pair_list[2] = False
  return [royal_flush_list, straight_flush_list, four_list,full_house_list, flush_list, straight_list,  three_list,two_pair_list, pair_list]

def add_score(player, player_score):
  list1 = remove_duplicates(player)
  list_dup = []
  if list1[1][1] == True:
    player_score += 105000
    player_score += list1[1][0]*100
  if list1[2][2]  == True:
    player_score += 90000
    list_dup += list1[2][1]
    player_score += list1[2][0]*100
  if list1[3][1] == True:
    list2 = [list1[3][0]['three'], list1[3][0]['two']]
    list_dup += list2
    player_score += 75000
    player_score += list1[3][0]['three_score']*100
    player_score += list1[3][0]['two_score']*50
  if list1[4][2] == True:
    player_score += 60000
    player_score += list1[4][0]*100
  if list1[5][1] == True:
    player_score += 45000
    player_score += list1[5][0]*100
  if list1[6][2] == True:
    list_dup += list1[6][1]
    player_score += 30000
    player_score += list1[6][0]*100
  if list1[7][2] == True:
    list_dup += list1[7][1]
    player_score += 15000
    for i in list1[7][1]:
      player_score += card_score[i]*100
  if list1[8][2] == True:
    list_dup += list1[8][1]
    for i in list(list1[8][1]):
      player_score += card_score[i]*100
  return [player_score, list_dup]
 
def add_high_card_score(player, player_score, list_dup):
  a = player[0][1]
  a_score = card_score[a]
  b = player[1][1]
  b_score = card_score[b]
  if a_score>b_score:
    if a not in list_dup:
      player_score+=(a_score*10)
    if b not in list_dup:
      player_score+=(b_score/2)
    else:
      pass
  elif a_score<b_score:
    if a not in list_dup:
      player_score+=(a_score/2)
    if b not in list_dup:
      player_score+=(b_score*10)
    else:
      pass
  else:
    pass
  return player_score

# royal flush
# straight flush 
# four of a kind
# full house
# flush
# straight 
# three of a kind
# two pair 
# pair

def remove_dup_list(list1):
  d = {}
  b =[]
  for i in list1:
    a = 1
    if i in b:
      a+=1
    else:
      b.append(i)
    d[i] = a
  return [b,d]