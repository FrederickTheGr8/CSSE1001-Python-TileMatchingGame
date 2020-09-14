#http://csse1001.uqcloud.net/notes/gui

#!/usr/bin/env python3
################################################################################
#
#   CSSE1001/7030 - Assignment 3
#
#   Student Username: xxxxxxxx
#
#   Student Name: Luke Hewitt
#
################################################################################

# VERSION 1.0.2

################################################################################
#
# The following is support code. DO NOT CHANGE.

from a3_support import *


# End of support code
################################################################################
# Write your code below
################################################################################

# Write your classes here (including import statements, etc.)

def popmessage(msg, title):
    """
    Generates pop up message for winning and losing

    popmessage(str, str) -> None
    """
    popupwin = tk.Tk()
    popupwin.wm_title(title)
    label = tk.Label(popupwin, text=msg)
    label.pack(side="top", fill="x", padx=40, pady=20)
    okbutton = tk.Button(popupwin, text="Okay", command = popupwin.destroy)
    okbutton.pack()

class SimpleTileApp(object):
    def __init__(self, master):
        """
        Constructor(SimpleTileApp, tk.Frame)
        """
        self._master = master

        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)

        self._grid_view = TileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


        self._master.title("Simple Tile Game")
        self._player = SimplePlayer()


        self._resetbtn = tk.Button(self._master, \
            text = "Reset Status", command = self._push_resetbtn)
        self._resetbtn.pack(side=tk.BOTTOM)
        
        self._statusbar = SimpleStatusBar(self._master, self._player)

        self._menubar = tk.Menu(self._master)
        self._master.config(menu=self._menubar)

        self._filemenu=tk.Menu(self._menubar)
        self._menubar.add_cascade(label = "File", menu = self._filemenu)
        self._filemenu.add_command(label = "New Game", \
            command = self._new_game)
        self._filemenu.add_command(label = "Exit", command = self._exit)
        
       
    def _handle_swap(self, from_pos, to_pos):
        """
        Run when a swap on the grid happens.
        """
        self._player.record_swap()
        self._statusbar.update_swaps()

    def _handle_score(self, score):
        """
        Run when a score update happens.
        """
        self._player.add_score(score)
        self._statusbar.update_score()
  
    def _push_resetbtn(self):
        """
        Run when reset button pressed.

        SimpleTileApp._push_resetbtn() -> None
        """
        self._player.reset_score()
        self._player.reset_swaps()
        self._statusbar.update_swaps()
        self._statusbar.update_score()

    def _new_game(self):
        """
        Begins a new game; resets the tiles includding resetting 
        SimpleStatusBar

        SimpleTileApp._new_game -> None
        """
        self._game.reset()
        self._grid_view.draw()
        self._push_resetbtn()

    def _exit(self):
        """
        Closes tkinter app window

        SimpleTileApp()._exit -> None
        """
        self._master.destroy()


class SimplePlayer():

    def __init__(self):
        """
        Constructs the player.

        SimplePlayer.__init__() -> None
        """
        self._score = 0
        self._swaps = 0

    def add_score(self, score):
        """
        Adds a score to the player's score. Returns the player's new score.

        SimplePLayer.add_score(int) -> int
        """
        self._score += score
        return self._score

    def get_score(self):
        """
        Returns the player’s score.

        SimplePlayer.get_score() -> int
        """
        return self._score

    def reset_score(self):
        """
        Resets the player's score.

        SimplePlayer.reset_score() -> None
        """
        self._score = 0

    def record_swap(self):
        """
        Records a swap for the player. Returns the player’s new swap count.

        SimplePlayer.record_swap() -> int
        """
        self._swaps += 1
        return self._swaps

    def get_swaps(self):
        """
        Returns the player's swap count.

        SimplePlayer.get_swaps() -> int
        """
        return self._swaps

    def reset_swaps(self):
        """
        Resets the player's swap count.

        SimplePlayer.reset_swaps() -> None
        """
        self._swaps = 0


class SimpleStatusBar(tk.Frame):
    """
    The SimpleStatusBar must inherit from tk.Frame and display the following:
        The number of swaps that the playter has made.
        The Player's score.
    """

    def __init__(self, parent, player):
        super().__init__(parent)

        self._statusplayer = player

        self._myframe = tk.Frame(parent)
        self._myframe.pack(side=tk.BOTTOM, expand = True, fill = tk.BOTH)

        self._scorelbl = tk.Label(self._myframe, \
            text="Score {}".format(self._statusplayer.get_score()))
        self._scorelbl.pack(side=tk.RIGHT)

        self._swapslbl = tk.Label(self._myframe, \
            text="{} Swaps used".format(self._statusplayer.get_swaps()))
        self._swapslbl.pack(side=tk.LEFT)

    def update_swaps(self):
        """
        Updates swap Label

        SimpleStatusBar.update_swaps() -> None
        """
        self._swapslbl.config\
        (text="{} Swaps used".format(self._statusplayer.get_swaps()))

    def update_score(self):
        """
        Updates score Label

        SimpleStatusBar.update_score() -> None
        """
        self._scorelbl.config\
        (text="Score {}".format(self._statusplayer.get_score()))    


class Character():
    """
    The Character class implements the basic functionality of a 
    player/enemy within the game, and is the superclass of Player & Enemy.
    """

    def __init__(self, max_health):
        """
        Constructs the character, where max_health is an integer representing
        the maximum amount of the player can have, and the amount of health 
        they start with.

        Character.__init__(int) -> None
        """
        self._maxhealth = max_health

        #Assumption: health of character begins at max health
        self._currenthealth = self._maxhealth

    def get_max_health(self):
        """
        Returns the maximum health the player can have.

        Character.get_max_health() -> int
        """
        return self._maxhealth

    def get_health(self):
        """
        Returns the player's current health.

        Character.get_health() -> int
        """
        return self._currenthealth

    def lose_health(self, amount):
        """
        Decreases the player’s health by amount. Health cannot go below zero.

        Character.lose_health(int) -> None
        """
        if self._currenthealth >= amount:
            self._currenthealth -= amount
        else:
            self._currenthealth = 0
        
        
    def gain_health(self, amount):
        """
        Increases the player’s health by amount. Health cannot go above
        maximum health.

        Character.gain_health(int) -> None
        """
        if (self._maxhealth - self._currenthealth) >= amount:
            self._currenthealth += amount
        else:
            self._currenthealth = self._maxhealth


    def reset_health(self):
        """
        Resets the player’s health to the maximum.

        Character.reset_health() -> None
        """
        self._currenthealth = self._maxhealth


class Enemy(Character):
    """
    The Enemy class represents an enemy, and inherits from Character. 
    """

    def __init__(self, type, max_health, attack):
        super().__init__(max_health)
        """
        Constructs the player, where type is the enemy’s
        type, max_health is an integer representing the amount of health the 
        enemy has, and attack is a pair of the enemy’s attack range, 
        (minimum, maximum).

        Enemy.__init__('str', int, (int, int)) -> None
        """
        self._type = type
        self._attack = attack

    def get_type(self):
        """
        Returns the enemy’s type.

        Enemy.get_type() -> str
        """
        return self._type

    def attack(self):
        """
        Returns a random integer in the enemy's attack range

        Enemy.attack() -> int
        """
        return random.randint(self._attack[0], self._attack[1])


class Player(Character):

    def __init__(self, max_health, swaps_per_turn, base_attack):
        super().__init__(max_health)
        """
        Constructs the player, where max_health is an integer representing 
        the amount of health the player has, and swaps_per_turn is an integer
        representing the number of swaps a player makes each turn, and
        base_attack is the player's base attack.

        Player.__init__(int, int, int) -> None
        """
        self._maxhealth = max_health
        self._swapsperturn = swaps_per_turn
        self._baseattack = base_attack

        self._bonusweaknesses = {
                            'fire': 'water',
                            'water': 'ice',
                            'poison': 'psychic',
                            'psychic': 'poison',
                            'ice': 'fire'
                            }

    def record_swap(self):
        """
        Decreases the player’s swap count by 1, which cannot go below zero. 
        Returns the player’s new swap count.

        Player.record_swap() -> int
        """
        if (self._swapsperturn - 1) >= 0:
            self._swapsperturn -= 1
        else:
            self._swapsperturn = 0
        

    def get_swaps(self):
        """
        Returns the player's swap count.

        Player.get_swaps() -> int
        """
        return self._swapsperturn

    def reset_swaps(self):
        """
        Resets the player’s swap count to the maximum swap count.

        Player.reset_swaps() -> None
        """
        self._swapsperturn = SWAPS_PER_TURN

    def attack(self, runs, defender_type):
        """
        Takes a list of Run instances and a defender type. Returns a pair of 
        (type, damage), where attack is a list of pairs of the form 
        (tile, damage), listing damage amounts for each type, in the order 
        the attacks should be performed.

        Player.attack([Object], 'str') -> ('str', int)
        """
        damage = 0
        enemyweakness = self._bonusweaknesses.get(defender_type)
        bonus = 1
        attacklist = []

        for r in runs:
            celltype = next(iter(r._cells.values())).get_type()

            #bonus damage calculations
            if celltype == enemyweakness:
                bonus = 1.4
                msg = celltype + ' is ' + defender_type + \
                's weakness, you deal x1.4 damage!'
                popmessage(msg, 'BONUS')
            if celltype == 'coin':
                bonus = 2
                popmessage('Coin tile: 2x Damage!', 'BONUS')

            damage = len(r) * r.get_max_dimension() * self._baseattack * bonus

            attacklist.append((celltype, damage))

        return attacklist

class VersusStatusBar(tk.Frame):
    """
    The VersusStatusBar is responsible for displaying the game/player/enemy’s 
    status. It must inherit from tk.Frame - 
    (it is also permissible to inherit from SimpleStatusBar).
    """

    def __init__(self, parent, player, enemy):
        super().__init__(parent)

        self._vsplayer = player
        self._vsenemy = enemy

        self._myframe = tk.Frame(parent)
        self._myframe.pack(side=tk.BOTTOM, expand = True, fill = tk.BOTH)

        self._currentlevellbl = tk.Label(self._myframe, \
            text="Current Level: 1")
        self._currentlevellbl.pack(side=tk.TOP)

        self._swapslbl = tk.Label(self._myframe, \
            text="{} Swaps remaining".format(self._vsplayer.get_swaps()))
        self._swapslbl.pack(side=tk.TOP)

        self._enemyhealthlbl = tk.Label(self._myframe, \
            text="Enemy Health: {}".format(self._vsenemy.get_health()))
        self._enemyhealthlbl.pack(side=tk.RIGHT)

        self._playerhealthlbl = tk.Label(self._myframe, \
            text="Player Health: {}".format(self._vsplayer.get_health()))
        self._playerhealthlbl.pack(side=tk.LEFT)

    def update_swaps(self):
        """
        Updates swap Label

        VersusStatusBar.update_swaps() -> None
        """
        self._swapslbl.config\
        (text="{} Swaps remaining".format(self._vsplayer.get_swaps()))

    def update_player_health(self):
        """
        Updates played health

        VersusStatusBar.update_score() -> None
        """
        self._playerhealthlbl.config\
        (text="Player Health: {}".format(self._vsplayer.get_health()))    

    def update_enemy_health(self):
        """
        Updates enemy health

        VersusStatusBar.update_score() -> None
        """
        self._enemyhealthlbl.config\
        (text="Enemy Health: {}".format(self._vsenemy.get_health()))    

    def update_current_level(self, currentlevel):
        """
        Updates current level 

        VersusStatusBar.update_score() -> None
        """
        self._currentlevellbl.config\
        (text="Current Level {}".format(currentlevel))


class ImageTileGridView(TileGridView):
    """
    The ImageTileGridView class inherits from TileGridView.
    """

    def __init__(self, master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, \
                 cell_height=GRID_CELL_HEIGHT,
                 **kwargs):
        """
        Constructor(tk.Frame, TileGrid, *, int, int, int, int, *)
        """
        super().__init__(master, grid, *args, width, height, \
            cell_width, cell_height, **kwargs)


class SinglePlayerTileApp(SimpleTileApp):
    """
    The SinglePlayerTileApp class is responsible for displaying the top-level
    GUI.
    """

    def __init__(self, master):
        """
        Constructor(master)
        """
        #variable stuff
        self._master = master
        self._game = SimpleGame()

        self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)
        self._game.on('runs', self._handle_runs)

        #inital grid frame
        self._grid_view = ImageTileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._master.title("Tile Game - Level 1")

        #character instances
        self._player = Player(PLAYER_BASE_HEALTH, SWAPS_PER_TURN, PLAYER_BASE_ATTACK)

        self._currentlevel = 1
        self.enemygen()

        self._statusbar = VersusStatusBar(self._master, self._player, \
            self._newenemy)

        self._menubar = tk.Menu(self._master)
        self._master.config(menu=self._menubar)

        self._filemenu=tk.Menu(self._menubar)
        self._menubar.add_cascade(label = "File", menu = self._filemenu)
        self._filemenu.add_command(label = "New Game", \
            command = self._new_game)
        self._filemenu.add_command(label = "Exit", command = self._exit)


    def _handle_swap(self, from_pos, to_pos):
        """
        Handles swapping, detects if swaps are zero and if so commences
        enemy attack.


        SinglePlayerTileApp._handle_swap((int, int), (int, int)) -> None
        """
        if self._player.get_swaps() > 0:
            self._player.record_swap()
            self._statusbar.update_swaps()
        else:
            self._player.lose_health(self._newenemy.attack())
            if self._player.get_health() < 1:
                popmessage('YOU DIED!, Game will reset', 'OH NOES')
                self._new_game()
            self._statusbar.update_player_health()
            self._player.reset_swaps()
            self._statusbar.update_swaps()


    def _handle_runs(self, runs):
        """
        Handles runs and enemy attack after a run happend in game.
        Also calls for next level if the enemy health is 0.

        SinglePlayerTileApp._handle_runs(list(Runs)) -> None
        """
        attacks = self._player.attack(runs, self._newenemy.get_type())
        
        for a in attacks:
            self._newenemy.lose_health(a[1])
            self._statusbar.update_enemy_health()
            if self._newenemy.get_health() < 1:
                popmessage('You killed the Enemy! Initiating Next Level',\
                    'Congratulations!')
                self.levelgen()
                break

    def _handle_score(self, score):
        pass

    def _push_resetbtn(self):
        """
        Run when reset button pressed.

        SinglePlayerTileApp._push_resetbtn() -> None
        """
        self._player.reset_health()
        self._player.reset_swaps()
        self._statusbar.update_swaps()

        #create new enemy
        self.enemygen()
        self._statusbar._vsenemy=self._newenemy
        self._statusbar.update_enemy_health()

    def _new_game(self):
        """
        Begins a new game; resets the tiles includding resetting 
        VersusStatusBar

        SinglePlayerApp._new_game -> None
        """
        self._game.reset()
        self._grid_view.draw()

        self._currentlevel = 1
        self._statusbar.update_current_level(self._currentlevel)
        self._master.title("Tile Game - Level {}".format(self._currentlevel))

        self._push_resetbtn()

    def _exit(self):
        """
        Closes tkinter app window

        SinglePlayerApp()._exit -> None
        """
        self._master.destroy()


    def levelgen(self):
        """
        Generates a new level

        SinglePlayerTileApp.levelgen() -> None
        """
        self._currentlevel += 1
        self.enemygen()
        self._statusbar._vsenemy=self._newenemy
        self._master.title("Tile Game - Level {}".format(self._currentlevel))
        self._statusbar.update_current_level(self._currentlevel)
        self._game.reset()
        self._grid_view.draw()
        self._player.reset_health()
        self._player.reset_swaps()
        self._statusbar.update_swaps()
        self._statusbar.update_enemy_health()
        self._statusbar.update_player_health()

    def enemytypegen(self):
        """
        Returns random type of enemy

        SinglePlayerTileApp.enemytypegen() -> str
        """
        return random.choice(list(ENEMY_PROBABILITIES.keys()))

    def enemygen(self):
        """
        Generates a new enemy and increases difcullty based on current level

        SinglePlayerTileApp.enemygen() -> None
        """
        h,a = generate_enemy_stats(self._currentlevel)

        #difficulty increasing
        h = h*self._currentlevel

        self._newenemy = Enemy(self.enemytypegen(), h, a)






def task1():
#    Add task 1 GUI instantiation code here
    #root = tk.Tk()
    #app = SimpleTileApp(root)
    #root.mainloop()
    pass

def task2():
    # Add task 2 GUI instantiation code here
    root = tk.Tk()
    app = SinglePlayerTileApp(root)
    root.mainloop()
    #pass

def task3():
    # Add task 3 GUI instantiation code here
    pass


def main():
    # Choose relevant task to run
#    task1()
    task2()


    




################################################################################
# Write your code above - NOTE you should define a top-level
# class (the application) called Breakout
################################################################################
if __name__ == '__main__':
    main()
