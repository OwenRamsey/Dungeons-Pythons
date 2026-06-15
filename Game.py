# Owen Ramsey
# Game Class  
# March 20 2026

import tkinter
from Player import Player
from Character import Character
from DiceRoll import rollDice
import database
import tkinter.messagebox
import customtkinter

class Game:
    def __init__(self, floor, roomNum, enyType, playerID):
        self.__floor = floor

        self.__roomNum = roomNum

        self.__enyType = enyType
        
        self.__playerID = playerID

        # Dictionary to store enemies
        self.__enemies = {}  

        # create player
        self.player = Player(2, 5, 5, 0, 1)

        # create main window 
        self.mainWindow = customtkinter.CTk()   
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")   

        self.mainWindow.title("Dungeons & Pythons")

        self.mainWindow.geometry("600x400")

        # create three frames
        self.topFrame = customtkinter.CTkFrame(self.mainWindow)
        self.midFrame = customtkinter.CTkFrame(self.mainWindow)
        self.belowMidFrame = customtkinter.CTkFrame(self.mainWindow)
        self.bottomFrame = customtkinter.CTkFrame(self.mainWindow)

        # check if there are any saves
        saveExist = database.checkForSaves()

        # create label for top frame
        self.descriptionLabel = customtkinter.CTkLabel(self.topFrame, text="Explore the Dungeons, but watch out for monsters!")

        # pack top frame label
        self.descriptionLabel.pack(side="left")

        # create middle frame
        self.hpVar = tkinter.StringVar()
        self.atkVar = tkinter.StringVar()

        self.hpVar.set(f"Player HP: {self.player.getHp()} out of: {self.player.getMaxHp()}")
        self.atkVar.set(f"Base Attack: {self.player.getBaseAttack()}")

        self.hpLabel = customtkinter.CTkLabel(self.midFrame, textvariable=self.hpVar)
        self.atkLabel = customtkinter.CTkLabel(self.midFrame, textvariable=self.atkVar)


        # pack middle frame labels
        self.hpLabel.pack(side="left", padx = 20)
        self.atkLabel.pack(side="left", padx = 20)

        # create below middle frame
    
        # create canvas
        self.canvas = tkinter.Canvas(self.belowMidFrame, width=700, height=200, bg="#1a1a1a", highlightthickness=0)
        

        #pack canvas
        self.canvas.pack()

        # create buttons
        self.attack = customtkinter.CTkButton(self.bottomFrame, text="Attack", command=self.attackMethod, state="disabled")
        self.explore = customtkinter.CTkButton(self.bottomFrame, text="Explore", command=self.exploreMethod)
        self.flee = customtkinter.CTkButton(self.bottomFrame, text="Flee", command=self.fleeMethod, state='disabled')

    
        # pack buttons
        self.attack.pack(side= "left", padx = 10)
        self.explore.pack(side= "left", padx = 10)
        self.flee.pack(side= "left", padx = 10)

        # pack frames
        self.topFrame.pack()
        self.midFrame.pack()
        self.belowMidFrame.pack()
        self.bottomFrame.pack()

        # create menu
        self.menu = tkinter.Menu(self.mainWindow)
        self.mainWindow.configure(menu=self.menu)
        self.savesMenu = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Saves", menu=self.savesMenu)
        self.savesMenu.add_command(label="Save Game", command=self.save)
        self.savesMenu.add_command(label="Load Game", command=self.load)
        self.savesMenu.add_command(label="Delete Save", command=self.delete)
        
        # ask if player want to load save
        if saveExist == True:
            choice = tkinter.messagebox.askyesno("Load Game?", "Do you want to load your previous game?")
            if choice == True:      
                self.__playerID = database.getLastPlayerID()
                self.load()
            else: self.startNewGame()

        else: self.startNewGame()

        # main loop
        self.mainWindow.mainloop()

    # method for buttons
    def attackMethod(self):

        # get the current enemy
        enemy = self.__enemies.get(self.__enyType)

        # have player attack
        damage = self.playerAttacking()

        # check if enemy hp is 0
        if enemy.getHp() <= 0:
            self.explore.configure(state="normal")
            self.attack.configure(state='disabled')
            self.flee.configure(state='disabled')
            self.player.setExp(self.player.getExp() + enemy.getExp())

            leveledUp = self.player.levelUpCheck()
            

            if leveledUp == True:
               self.showEvent("You defeated the enemy and leveld up!")
            else:
                self.showEvent("You defeated the enemy!")
            self.update_stats()
        else:

            # if enemy didnt die show how much damage player dealt
            self.showEvent(f"You hit the enemy for {damage} damage! But the enemy hit you")

            self.playerAttacked()
            self.update_stats()

        if self.__enyType == 3:
            self.__floor += 1
            self.__roomNum = 0



    def exploreMethod(self):
        # increase room number
        self.__roomNum += 1

        # check what room player is on for what type of dice to roll
        if self.__roomNum >= 6:
            diceRole = rollDice(8)
        elif self.__roomNum >= 4:
            diceRole = rollDice(6)
        else:
            diceRole = rollDice(4)

        # if room number is 8 call boss room
        if self.__roomNum == 8:
            self.bossRoom()

        # have diffrent event happen based on dice roll
        elif diceRole == 1:
            self.showEvent("You found a potion that increaased your max health!")
            self.player.increaseMaxHp()
            self.update_stats()

        elif diceRole == 2:
           self.showEvent("You found a potion that increaased your base Strength!")
           self.player.increaseBaseATK()
           self.update_stats()


        elif diceRole == 3:
            self.showEvent("You encountered a goblin prepare to fight!")
            # disable explore button for combat and enable fight and flee
            self.explore.configure(state="disabled")
            self.attack.configure(state='normal')
            self.flee.configure(state='normal')

            # create goblin
            self.createGoblin()

        elif diceRole == 4:
            self.showEvent("You encountered a slime prepare to fight!")
            # disable explore button for combat and enable fight and flee
            self.explore.configure(state="disabled")
            self.attack.configure(state='normal')
            self.flee.configure(state='normal')

            # create slime
            self.createSlimes()

        elif diceRole == 5:
            # flip a coin 
            coinFlip = rollDice(2)
            # if 1 player triggered trap
            if coinFlip == 1:
                self.showEvent("You triggered a trap and lost some health!")
                self.player.decreaseHP(rollDice(4))
                # check if player died
                if self.player.getHp() <= 0:
                    self.gameOver()
                self.update_stats()
            # if 2 player avoided it
            elif coinFlip == 2:
                self.showEvent(text="You triggered a trap but managed to avoid it!")
        
        elif diceRole == 6:
            self.showEvent("You found a potion to replanish your health!")
            self.player.increaseHp()
            self.update_stats()

        elif diceRole == 7:
            # roll d20
            diceRole = rollDice(20)


            # if dice rolled 20 give rewards
            if diceRole == 20:
                self.showEvent("You entered an enchanted room! Your armour and weapon where enchanted!")
                self.player.increaseBaseATK()
                self.player.increaseMaxHp()
                self.update_stats()

            # if roled 1 give punsinment
            elif diceRole == 1:
                self.showEvent("You entered a cursed room! Your armnour and weapon where cursed!")
                self.player.decreaseATK()
                self.player.decreaseMaxHp()
                self.update_stats()
            else:
                self.showEvent("You entered an empty room...")

        elif diceRole == 8:
            # call boss room
            self.bossRoom()
        

    def fleeMethod(self):
        # roll a d6
        diceRoll = rollDice(6)

        # check if user managed to run away
        if diceRoll >= 5:
            # tell user they ran away
            self.showEvent("You ran away from the enemy")

            # reset buttons
            self.flee.configure(state="disabled")
            self.explore.configure(state="normal")
            self.attack.configure(state='disabled')
        else:
            self.showEvent("You failed to run away and got hit!")
            self.playerAttacked()
            self.update_stats()
            

    # Method 
    def update_stats(self):
        if hasattr(self, "hpVar"):
            self.hpVar.set(f"Player HP: {self.player.getHp()} out of: {self.player.getMaxHp()}")
        if hasattr(self, "atkVar"):
            self.atkVar.set(f"Base Attack: {self.player.getBaseAttack()}")
        
        

    # Updated createGoblin method
    def createGoblin(self):
        # create goblin based on floor
        goblin = Character(2 * self.__floor, 3 * self.__floor, 3 * self.__floor, (3 * self.__floor + 2))


        self.__enemies[1] = goblin  
        self.__enyType = 1  

    # Updated createSlimes method
    def createSlimes(self):
        # create slime based on floor

        slime = Character(2 * self.__floor, 3 * self.__floor, 3 * self.__floor, (3 * self.__floor + 2))

        self.__enemies[2] = slime
        self.__enyType = 2

    # Updated bossRoom method
    def bossRoom(self):

        self.showEvent("You encountered a Python prepare to fight!")
        self.explore.configure(state="disabled")
        self.attack.configure(state='normal')

        # create boss based on floor

        boss = Character(5 * self.__floor, 20 * self.__floor, 20 * self.__floor, (15 * self.__floor + 10))

        self.__enemies[3] = boss
        self.__enyType = 3

    # Updated playerAttacked method
    def playerAttacked(self):
        enemy = self.__enemies.get(self.__enyType)
        if enemy:
            damage = enemy.attack()
            self.player.decreaseHP(damage)

        if self.player.getHp() <= 0:
                self.gameOver()

    # Updated playerAttacking method
    def playerAttacking(self):
        enemy = self.__enemies.get(self.__enyType)
        if enemy:
            damage = self.player.attack()
            enemy.decreaseHP(damage)
        return damage

    # game over method
    def gameOver(self):
        # disable buttons
        self.flee.configure(state="disabled")
        self.explore.configure(state="disabled")
        self.attack.configure(state='disabled')

        self.showEvent(f"You have died GAME OVER! You made it to floor {self.__floor} room {self.__roomNum}")
        
        # create restart button
        #self.restartButton = tkinter.Button(self.bottomFrame, text="Restart Game", command=self.startNewGame)
        #self.restartButton.pack(side="left")
    # save save function
    def save(self):
        if self.explore.cget("state") == "disabled":
            tkinter.messagebox.showerror("Save Game", "You cant save in combat")
        else:
            database.updatePlayer(self.__playerID, self.player)
            # check if event text exist
            if hasattr(self, "eventText"):
                # set text to text in event text
                text = self.canvas.itemcget(self.eventText, "text")
            else:
                # set text to empty
                text = ""

            # check if save exist 
            if database.readSave(self.__playerID):

                database.updateSave(self.__playerID, self.__floor, self.__roomNum, text)
            else:
                database.createSave(self.__playerID, self.__floor, self.__roomNum, text)

            tkinter.messagebox.showinfo("Save Game", "Game saved")

    # load save function
    def load(self):
        saveData = database.readSave(self.__playerID)
        playerData = database.readPlayer(self.__playerID)

        if saveData and playerData:
            # set player sates form playerData
            self.player.setBaseAttack(playerData[1])
            self.player.setHp(playerData[2])
            self.player.setMaxHp(playerData[3])
            self.player.setExp(playerData[4])
            self.player.setLevel(playerData[5])

            # check if saved event text has text
            if saveData[4]:
                # display saved event text
                self.showEvent(saveData[4])
                

            # set floor and room from save
            self.__floor = saveData[2]  
            self.__roomNum = saveData[3]

            # reset buttons
            self.flee.configure(state="disabled")
            self.explore.configure(state="normal")
            self.attack.configure(state='disabled')

            self.update_stats()
            tkinter.messagebox.showinfo("Load Game", "Game loaded successfully")


        else:
            tkinter.messagebox.showerror("Load Game", "No save found")

    # delete save function
    def delete(self):
        if database.readSave(self.__playerID):
            choice = tkinter.messagebox.askyesno("Delete Save", "Are you sure you want to delete your save?")
            if choice == True:
                database.deleteSave(self.__playerID)
                tkinter.messagebox.showinfo("Delete Save", "Save deleted")
        else:
            tkinter.messagebox.showerror("Delete Save", "No save to delete")
    
    # start new game function
    def startNewGame(self):
        # create player
        self.player = Player(2, 5, 5, 0, 1)
        self.__floor = 1
        self.__roomNum = 0

        # reset buttons
        self.flee.configure(state="disabled")
        self.explore.configure(state="normal")
        self.attack.configure(state='disabled')
        
        self.__playerID = database.createPlayer(self.player)
        database.createSave(self.__playerID, self.__floor, self.__roomNum, "")

    def showEvent(self, text):

        if hasattr(self, "eventText"):
            self.canvas.delete(self.eventText)

        self.eventText = self.canvas.create_text(
            300, 100,
            text=text,
            fill="white",
            font=("Arial", 14),
            width=460,
            justify="center"
        )

if __name__ == '__main__':
    database.createTables()
    playGame = Game(1,0,0, None)