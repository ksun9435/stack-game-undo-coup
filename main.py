import random
#when comp challenges human's exchange, exchange process restarts for human, and human's current influences are wrong

#sometimes goes past first move also not sure if fixed but if u see this error and cant figure it out, just screenshot and send cause the code is kinda messy down there
'''havent encountered this yet '''
#not doing correct player, somewhere in challenge, cha_bool, block, move_stack.pop(), undo_action there is multiple undos? basically idea is that when challenge is successful should only pop the last action, turn number and player keep going

#if challenge succeed opponent needs to lose influence and print what influence was lost


class Player:

  def __init__(self, name):
    self.name = name
    self.coins = 0
    self.p_influences = []
    self.p_lost = []  #flipped
    self.p_moves_names = ["i", "t", "e", "f", "s"]
    self.exiled = False

  def player_influences(self):
    str = ""
    for influence in self.p_lost:
      str += influence.name + " "
    for influence in self.p_influences:
      #after finish testing delete line below and uncomment rest of method
      #str += "unknown  " + influence.name + " "
      str += "unknown "

    return str

  def human_player_influences(self):
    str = ""
    if not self.is_human():
      return ""
    for influence in self.p_influences:
      str += influence.name + " "
    return str

  #influence_name is type string full name
  def has_influence(self, influence_name):
    for influence in self.p_influences:
      if influence.name == influence_name:
        return True
    return False

  def find_influence(self, influence_name):
    for influence in self.p_influences:
      if influence.name == influence_name:
        return influence

  #works
  def player_lost_influences(self):
    return self.p_lost

  #works
  def set_influence(self, new, old):
    #new and old are actual influence objects

    if old in self.p_influences:
      deck.add(old)
      self.p_influences.remove(old)
      self.p_influences.append(new)

  #works
  #not sure why print(players) didnt print names
  def lose_influences(self, lost):
    #lost is influence object
    self.p_influences.remove(lost)
    self.p_lost.append(lost)
    if self.is_exiled():
      print(f"{self} is exiled.")
      self.exile()

  def is_exiled(self):
    return len(self.p_influences) == 0

  def exile(self):
    global playing
    self.exiled = True
    playing -= 1
    print(f"Remaining players: {playing}")
    players_names.remove(self.name)
    exiled.append(self)

  #works
  def is_human(self):
    return False

  def avail_names(self, move_name):
    #move_name is shortened name
    avail_names = []
    for player in players:
      if not player.is_exiled() and not player == self:
        avail_names.append(player.name)
    #print(self.name)
    #print(avail_names)
    if moves_names[move_name] == "Steal":
      for player in players:
        #print("entered for loop in avail_names")
        if not player.is_exiled() and not player==self and player.coins < 2:
          avail_names.remove(player.name)
    '''if move_name == "s" or move_name == "c":  #only print avail names if action has an opponent
      print(f"{avail_names}")'''
    #print(f"avail names: {avail_names}")
    return avail_names

  #if have time figure out 10+ coins only coup possible
  def p_avail_moves(self):
    if "c" in self.p_moves_names and self.coins < 7:
      self.p_moves_names.remove("c")
    elif not "c" in self.p_moves_names and self.coins > 7:
      self.p_moves_names.append("c")
    #print(f"avail moves: {self.p_moves_names}")

    return self.p_moves_names

  def change_coins(self, amt):
    self.coins += amt
    if self.coins < 0:
      self.coins = 0

  def __str__(self):
    return self.name


class HumanPlayer(Player):

  def __init__(self, name):
    super().__init__(name)

  def is_human(self):
    return True


class CompPlayer(Player):

  def __init__(self, name):
    super().__init__(name)

  def get_move(self, turn_number, player):
    #move is short move-name
    #print(player.p_avail_moves())
    move = random.choice(player.p_avail_moves())
    while self.avail_names(move) == []:
      move = random.choice(player.p_avail_moves())
    if player.coins > 12 and "c" in player.p_avail_moves():
      move = "c"
    opponent = self.get_opponent(move)
    #print("opponent in get_move is", type(opponent))
    return name_to_move(moves_names.get(move), turn_number, player, opponent)

  def get_opponent(self, move):
    #move should be string type shortened
    if attack_action(move):
      #opponent is player name string
      opponent = random.choice(self.avail_names(move))
      while opponent == self.name:
        opponent = random.choice(self.avail_names(move))
        #opponent = random.choice(players_names)
      for player in players:
        if opponent == player.name:
          opponent = player
          return opponent
    #change later
    #print("comp's attack action isnt c or s. choose rand opponent anyway")
    opponent = random.choice(players_names)
    while opponent == self.name:
      opponent = random.choice(players_names)
    return Player(opponent)

  def get_block(self, player):  #123
    if random.randint(0, 100) > -1:  #og >25
      output = move_stack.peek().block(player)
      #print(f"in get_block, output: {output}")
      if isinstance(output, list):
        return random.choice(output)
      return output

  def choose_challenge(self, player, opponent, influence, move,
                       blocking):  #456
                         
    if not move.name == "Income" and not move.name == "Foreign Aid" and not move.name == "Coup":
      if random.randint(0, 20) > -1:  #og <100
        return challenge(player, opponent, influence, blocking)
      else: #bm
        return False 
   #returns None for unchallengable actions

#works
class Deck:
  #deck of influences cards, 4 of each of the 4 types
  def __init__(self):
    self.influences_pool = []

    for x in influences_names.values():
      for y in range(4):
        self.influences_pool.append(Influence(x))
    random.shuffle(self.influences_pool)

  def draw(self):
    return self.influences_pool.pop()

  def add(self, influence):
    self.influences_pool.append(influence)

  def __str__(self):
    return str(self.influences_pool)


#works
class Influence:

  def __init__(self, name):
    self.lost = False
    self.name = name

  def __str__(self):
    return self.name

  def __repr__(self):
    return str(self)


class Move:

  def __init__(self, name, turn_number, player, opponent):
    self.turn_number = turn_number
    self.player = player
    self.name = name
    self.opponent = opponent

  #p sure it works
  def action(self):
    if self.name == "Income":
      print(f"{self.player} is attempting Income. ")
      self.player.change_coins(1)
    elif self.name == "Foreign Aid":
      print(f"{self.player} is attempting Foreign aid. ")
      self.player.change_coins(2)
    elif self.name == "Tax":
      print(f"{self.player} is attempting Tax. ")
      self.player.change_coins(3)

    elif self.name == "Coup":
      print(f"{self.player} is attempting Coup against {self.opponent.name}. ")
      self.player.change_coins(-7)
      if self.player.is_human():
        #guess is type string
        guess_name = influences_names.get(
          input(f"Guess one of {self.opponent}'s influences: "))
        while not guess_name in influences_names.values():
          guess_name = influences_names.get(
            input(f"Try again. Guess one of {self.opponent}'s influences: "))
        if self.opponent.has_influence(guess_name):
          guess = self.opponent.find_influence(guess_name)
          self.opponent.lose_influences(guess)
          print(
            f"{self.player}'s Coup against {self.opponent}'s {guess.name} succeeded."
          )
        else:
          print(f"{self.opponent} doesn't have a {guess_name}. Coup failed.")
      else:  #coup for comp
        self.opponent.lose_influences(random.choice(
          self.opponent.p_influences))
        print("Coup was successful.")

    elif self.name == "Exchange":

      print(f"{self.player} is attempting Exchange. ")
      newPool = [deck.draw() for x in range(len(self.player.p_influences) * 2)]
      #print(f"DECK: {deck}\n")

      temp_influences = []
      for influence in self.player.p_influences:
        temp_influences.append(influence)
      for influence in temp_influences:
        #print("Loop is at", influence.name)
        if not self.player.is_human():
          self.player.set_influence(newPool.pop(), influence)

        else:
          print("New influences drawn: ", newPool, "\nCurrent influences: ",
                self.player.p_influences)
          print(f"Use {influences_names.keys()} for {influences_names.values()}")
          answer = input("Select a new influence: ")
          new_is_in_pool = False
          while not new_is_in_pool:
            if answer in influences_names.keys():
              for new_influence in newPool:
                if new_influence.name == influences_names[answer]:
                  new = new_influence
                  new_is_in_pool = True
            if new_is_in_pool:
              break
            answer = input("Try again. Select a new influence: ")

          answer = input("Choose a current influence to replace: ")
          old_is_in_pool = False
          while not old_is_in_pool:
            if answer in influences_names.keys():
              for old_influence in self.player.p_influences:
                if old_influence.name == influences_names[answer]:
                  old = old_influence
                  old_is_in_pool = True
            if old_is_in_pool:
              break
            answer = input(
              "Try again. Which old influence do you want to switch out: ")

          self.player.set_influence(new, old)  #does get called
          #print(f"Returned {old} to deck")
          newPool.remove(new)
          #print("Removed", new, "from newPool")
          #print(f"DECK: {deck.influences_pool} \n")
      if self.player.is_human:
        print("Influences after exchange:", self.player.p_influences)
      else:
        print(f"{self.player.name} exchanged their influences.")

      for influence in newPool:  #return unchosen cards
        deck.add(influence)
        #print(f"Returned unchosen {influence} to deck")
      #print(f"DECK: {deck}\n")
      #print(deck)

    elif self.name == "Steal":
      print(f"{self.player} is attempting Steal from {self.opponent}")
      #print(f"{self.opponent} has {self.opponent.coins}")
      self.opponent.change_coins(-2)
      self.player.change_coins(2)
      '''if self.opponent.coins >= 2:
        self.player.change_coins(2)
        self.opponent.change_coins(-2)
      else:
        print(f"{self.opponent} has less than 2 coins") '''

  def undo_action(self):
    #just undoing the action in action method same way as result and action methods
    if self.name == "Income":
      self.player.change_coins(-1)
    elif self.name == "Foreign Aid":
      self.player.change_coins(-2)
    elif self.name == "Tax":
      self.player.change_coins(-3)
    elif self.name == "Steal":
      self.player.change_coins(-2)
      self.opponent.change_coins(2)
    elif self.name == "Exchange":
      #print(deck)
      for x in range(len(self.player.p_influences)):  #mark
        temp = self.player.p_influences[-x - 1]
        #self.player.p_influences[-1] = self.player.p_lost[-2 or (-3 and -4) depending on # of influences left]
        self.player.p_influences[-x - 1] = deck.influences_pool.pop(
          -x - 1 - len(self.player.p_influences))
        #print(self.player.p_influences[-x - 1])

        #self.player.p_lost.append(temp)
        deck.add(temp)
      #exchange: swap last element of deck and current influences

  def redo_exchange(self):
    if self.name == "Exchange":
      for x in range(len(self.player.p_influences)):  #mark
        #print(deck)

        temp = deck.influences_pool.pop(-x - 1)
        #self.player.p_influences[-1] = self.player.p_lost[-2 or (-3 and -4) depending on # of influences left]
        deck.add(self.player.p_influences[-x - 1])
        #print(self.player.p_influences[-x - 1])

        #self.player.p_lost.append(temp)
        self.player.p_influences[-x - 1] = temp
        #print(deck)

  #supposed to be counteraction/block
  def block(self, other_player):
    #duke blocks foregin aid (anyone), contessa blocks assassin (against self only), ambassador + captain blocks steal (against self)
    if self.name == "Foreign Aid":
      print(
        f"{other_player} is attempting to block {self.player}'s Foreign Aid")
      return "Duke"
    if other_player == self.opponent:  #123
      if self.name == "Steal":
        print(f"{other_player} is attempting to block {self.player}'s Steal")
        return ["Captain", "Ambassador"]

  def result(self):  #qwe
    #basically just print statement after action is successful
    if self.name == "Income":
      return f"{self.player} took income from the treasury.\n{self.player} gained 1 coin."
    if self.name == "Foreign Aid":
      return f"{self.player} took foreign aid from the treasury.\n{self.player} gained 2 coins."
    if self.name == "Coup":
      return f"{self.player} launched coup on {self.opponent}. {self.opponent}'s revealed influences: {self.opponent.p_lost}"
    if self.name == "Tax":
      return f"{self.player} took 3 coins from the treasury."
    if self.name == "Steal":
      return f"{self.player} stole 2 coins from {self.opponent}."

    if self.name == "Exchange":
      if self.player.is_human():
        return f"{self.player} exchanged for {self.player.p_influences}"
      else:
        return f"{self.player} exchanged their cards."

  def move_influence(self):
    if self.name == "Tax":
      return "Duke"
    if self.name == "Steal":
      return "Captain"
    if self.name == "Exchange":
      return "Ambassador"

  def __str__(self):
    return self.name


class MoveStack():

  def __init__(self):
    self.stack = []

  def push(self, move):
    self.stack.append(move)

  def peek(self):
    if not self.size() == 0:
      return self.stack[-1]

  def pop(self):
    self.stack.pop()
    if not self.size() == 0:
      return self.peek().result()
    else:
      return "No previous actions."

  def size(self):
    return len(self.stack)

  def __str__(self):
    str = ""
    for move in self.stack:
      str += move.name + ", "
    return str


#works
def name_to_move(name, turn_number, player, opponent):
  #print("opponent in name_to_move is", type(opponent))
  p_opponent = Player("none")
  for oppo in players:
    if opponent.name == oppo.name:
      p_opponent = oppo
  return Move(name, turn_number, player, p_opponent)


def attack_action(str):
  return str == "c" or str == "s"


#456
def uncha_action(str):
  return str == "i" or str == "f" or str == "c"


def challenge(player, opponent, influence, blocking):  #works: income
  #blocking is boolean, player and opponent are player objects, influence is influence name
  #basically use player methods to check if influence is in player's hand returns true or false?

  #print(f"{type(player)} entered challenge()")
  print(f"{player} is attempting to challenge {opponent}")
  success = True
  #challenge block
  #print(f"BLOCKING: {blocking}")
  if blocking:
    #print("blocking true")
    if move_stack.peek().name == "Foreign Aid":
      if opponent.has_influence("Duke"):
        found_influence = opponent.find_influence("Duke") 
        success = False
    elif move_stack.peek().name == "Steal":
      if opponent.has_influence("Captain") or opponent.has_influence(
          "Ambassador"):
        if not opponent.find_influence("Captain") == None:
          found_influence = opponent.find_influence("Captain")
        else:
          found_influence = opponent.find_influence("Ambassador")
        success = False


#challenge regular actions
#tax, exchange, steal

  elif move_stack.peek().name == "Tax" or move_stack.peek(
  ).name == "Exchange" or move_stack.peek().name == "Steal":
    print(f"{player} challenges {opponent}'s {move_stack.peek().name}")
    if move_stack.peek().name == "Tax":
      if opponent.has_influence("Duke"):
        found_influence = opponent.find_influence("Duke")
        success = False
    elif move_stack.peek(
    ).name == "Exchange":  #needs the 0 or 1 like in the undo_action how theres a x in player.p_influences which is either 0 or 1
      move_stack.peek().undo_action()
      if opponent.has_influence("Ambassador"):
        found_influence = opponent.find_influence("Ambassador")
        success = False
      move_stack.peek().redo_exchange()
    elif move_stack.peek().name == "Steal":
      if opponent.has_influence("Captain"):
        found_influence = opponent.find_influence("Captain")
        success = False
  else:  #income, foreign aid, coup
    print(f" {move_stack.peek().name} can't be challenged. ")

  if success == False:
    #so set influence failed
    print("Challenge failed. ")  #opponent has required influence
    player.lose_influences(random.choice(player.p_influences))
    opponent.set_influence(deck.draw(), found_influence)
    print(
      f"{player} failed challenge and {player} revealed influence: {player.p_lost[-1]}"
    )
  else:
    print("Challenge succeeded.")
    move_stack.peek().undo_action()
    opponent.lose_influences(random.choice(opponent.p_influences))
    print(
      f"{player} succeeded challenge and {opponent} revealed influence: {opponent.p_lost[-1]}"
    )
    #print(f"{opponent}'s remaining influence: {opponent.p_influences}")
    print("Previous action:\n", move_stack.pop())

  return success


def players_print_influences():
  for player in players:
    print(f"player: {player} influences: {player.player_influences()}")


#move_names will be dict: (key = first letter, value = full name)
#influence too
moves_names = {
  "i": "Income",
  "f": "Foreign Aid",
  "c": "Coup",
  "t": "Tax",
  #"a": "Assassinate",
  "e": "Exchange",
  "s": "Steal"
}
influences_names = {
  "du": "Duke",
  #"as": "Assassin",
  "ca": "Captain",
  "am": "Ambassador",
  "co": "Contessa"
}

players_names = []
move_stack = MoveStack()
players = []
exiled = []
deck = Deck()

#play1.change_coins(20)  #test

for x in range(5):
  if x == 0:
    player = HumanPlayer(input("What is your name: "))
  else:
    player = CompPlayer(input("What is this player's name: "))
  players.append(player)
  players_names.append(players[x].name)
  players[x].p_influences.append(deck.draw())
  players[x].p_influences.append(deck.draw())

#print(players_names)
#print(f"DECK: {deck}")
turn_num = 0
undo_bool = False
cha_bool = None
next_player = Player("")
playing = len(players)

print()
print("Coup")
print("The goal of the game is to remain the last one standing.")
print("Income adds one coin. Foreign Aid adds two, but can be blocked by Duke. Coup requires 7 coins, and reveals the opponent's influence. Steal can only happen if someone has more than 2 coins, and can be blocked by Captain or Ambassador. It can be challenged if someone thinks you don't have a Captain. Exchange switches out your influences from a choice of two influences for each of your remaining influences. It can be blocked if someone thinks you don't have an Ambassador. Tax adds 3 coins. It can be challenged if someone thinks you don't have a Duke.")
print("A few modifications were made: there is no Assassin influence, (which makes Contessa useless but it's still in the game), there is a total of 16 influences, 4 of each of the 4 types, you can't undo the revealing of an influence, and you can't use Coup like normal, unlike the other computer players. Instead, you have to guess the influence correctly to be able to reveal it.)")
print()
print()
print()

while playing > 1:
  for player in players:
    #print(f" goin through players, current player is: {player.name} ")
    if player.exiled:
      continue
    #if undo, go through players from beginning until get to the correct next player
    if undo_bool and not player == next_player:
      continue
    undo_bool = False
    #start of turn
    print(f"turn number: {turn_num+1}\nplayer: {player}\ncoins: {player.coins}")
    if player.is_human():
      print(f"your unrevealed influences: {player.human_player_influences()}")
    print()
    #choose action
    players_print_influences()
    print()
    if player.is_human():
      n_answer = None
      m_answer = input(f"Enter action {list(moves_names.keys())} for corresponding {list(moves_names.values())}: ")
      while m_answer not in player.p_avail_moves() or len(
          player.avail_names(m_answer)) == 0:
        m_answer = input(f"Try again {list(moves_names.keys())}: ")
      if attack_action(m_answer):
        n_answer = input("Enter player name: ")
        while n_answer not in players_names or n_answer == player.name:
          n_answer = input("Try again: ")

      move_stack.push(
        name_to_move(moves_names.get(m_answer), turn_num, player,
                     Player(n_answer)))
      #move_stack.push(name_to_move(moves_names.get(m_answer), turn_num, player, find_influence(n_answer)) #supposed to be this?
    else:
      move_stack.push(player.get_move(turn_num, player))
    move_stack.peek().action()
    turn_num += 1
    #testing
    #print(move_stack)

    #asks whether to undo
    #should not be able to undo for coup?
    while (not move_stack.size() == 0 and input("Do you want to undo? [y]: ") == "y"):
      next_player = move_stack.peek().player
      move_stack.peek().undo_action()
      print("Previous action:\n", move_stack.pop())
      turn_num -= 1
      undo_bool = True

    if undo_bool:
      break

    #action and undo done, now challenge and block
    #cha_bool is challenge boolean
    #if cha_bool is True, challenge was successful, False, challenge was not, None, challenge did not happen
    cha_bool = None
    block = None
    #ask other players if want to challenge/block first player's action
    for second_player in players:
      if second_player.is_exiled():
        continue
      #challenge happened, so shouldnt have anyone else challenging
      if not cha_bool == None:
        #maybe happens when challenge block and still need to go through rest of players
        #print("still looping while cha_bool is not None shouldnt be happening? i think")
        break
      #start of challenge/block
      #note have to make this not run when action fails

      #commented out print(f"second_player: {second_player} and move's opponent: {move_stack.peek().opponent}")
      if not second_player == player:
        #print("second_player is not player")
        if second_player == move_stack.peek().opponent or move_stack.peek(
        ).name == "Foreign Aid":  # alr inside block?
          #print("second_player is opponent of foreign aid")
          if not second_player.is_human():
            #print("comp second player block?")
            block = second_player.get_block(second_player)  #123
          else:
            if input(
                f"Do you want to block this action? The action is {move_stack.peek().name} (Notice, you can challenge if you choose not to block) [y]: "
            ) == 'y':
              block = move_stack.peek().block(second_player)
              if isinstance(block, list):
                answer = input("Is your influence Captain or Ambassador? ['ca', 'am']: ")
                while not answer == "ca" or not answer == "am":
                  answer = input("Try again. Is your influence Captain or Ambassador? ['ca', 'am']: ")
                block = influences_names[answer]

          if not block == None:
            #print("second_player attempting block")
            for third_player in players:
              if third_player.is_exiled():
                continue
              #print(f"third player: {third_player}")
              if not third_player == second_player:
                #print("third player is not second_player")
                if not third_player.is_human(): #asks challenge for comps
                  #print("comp challenge block?")  #bm
                  
                  cha_bool = third_player.choose_challenge(
                    third_player, second_player,
                    move_stack.peek().move_influence(), move_stack.peek(),
                    True)
                  #print("line 682 cha_boo: ", cha_bool) # -> line 693
                else: #asks challenge for human
                  if input(f"Do you want to challenge {second_player}'s' block? [y]: ") == "y":  #will later move inside challenge so wont print for nonchallengable actions
                    cha_bool = challenge(third_player, second_player,
                                         move_stack.peek().move_influence(),
                                         True)
                #print(f"in block cha bool : {cha_bool}")
                if not cha_bool == None:
                  break
            if not cha_bool == True:
              move_stack.peek().undo_action()
              print("Previous action:\n", move_stack.pop())
              print("Block was successful.")
              break
          else:
            if move_stack.peek().name == "Income" or move_stack.peek().name == "Coup" or move_stack.peek().name == "Exchange":
              print(f"{move_stack.peek().name} is unblockable")
            else:
              print("No blocks attempted.")
        else:
          #print("second_player is not opponent")
          if not second_player.is_human():
            #print("comp challenge action?")
            cha_bool = second_player.choose_challenge(
              second_player, player,
              move_stack.peek().move_influence(), move_stack.peek(), False)
          else:
            if input("Do you want to challenge the action? [y]: ") == "y":
              cha_bool = challenge(second_player, player,
                                   move_stack.peek().move_influence(), False)

    #print(f"end of secondn players loop cha_bool: {cha_bool}")

    #print("result")
    if not move_stack.size() == 0:
      #not sure if that whole not (not block == None and not cha_bool == True) works
      if not cha_bool == True and block == None:
        print(move_stack.peek().result())
    #else: print("no previous moves")
    print()

print("Game Over")
for player in players:
  if not player in exiled:
    winner = player
#might not work
print(f"{winner.name} won!")

#assassinate bye bye
'''
    elif self.name == "Assassinate":
      print(f"{self.player} is attempting assassinate on {self.opponent}")
      self.player.change_coins(-3)
      #ask if want to block?
      if self.player.is_human():
        if len(self.opponent.p_lost) == 0:
          print(f"{self.opponent} hasnt lost any influences")
          move_stack.pop()  #test
        else:
          name = influences_names.get(
            input("Choose influence to assassinate: "))
          for target in self.opponent.p_influences:
            if target.name == name:
              if target.lost:
                print(f"{self.opponent}'s {target} was assassinated.")
                self.opponent.lose_influence(target)
                self.opponent.p_lost.remove(target)
              else:
                print(f"{target} has not been guessed")
                move_stack.pop()  #test
                break
            else:
              print(f"{self.opponent} does not have {target}.")
              move_stack.pop()  #test
      else:
        self.opponent.lose_influence()
    '''
'''elif self.name == "Assassinate":
      self.player.change_coins(3)
      self.opponent.p_influences.append(self.opponent.p_lost[-1])
'''
'''    if self.name == "Assassinate":
      return f"{self.player} assassinated {self.opponent}'s influence."'''
'''    if self.name == "Assassinate":
      return "Assassin"'''
'''elif move_stack.peek().name == "Assasinate":
      if opponent.has_influence("as"):
        success = False'''
'''if "a" in self.p_moves_names and self.coins < 3:
      self.p_moves_names.remove("a")
    elif not "a" in self.p_moves_names and self.coins > 3:
      self.p_moves_names.append("a") '''
'''if self.name == "Assassin":
        print(
          f"{other_player} is attempting to block {self.player}'s Assassin")
        return "Contessa"'''
'''i think exchage is ok now'''
#computer does steal action, stealing from "none"; might have been fixed but idea is that in get_move, opponent should be player class so that a player class type gets passed into name_to_move and created as Move - just check if it works when comp does steal action
''' ^that was bc get_opponent returned None whenever attack_action was false, and so None was passed to name_to_move's opponent. while testing for that I noticed the name_to_move in line 481 didnt take a Player type for opponent so I changed that, not sure if supposed to .


line 535 name 'block' is not defined '''
#ok i put a block = None above where cha_bool is also = None

