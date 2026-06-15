# Owen Ramsey
# Player class
# March 20 2026

from Character import Character
from DiceRoll import rollDice

# player class
class Player(Character):

    #initialize the class
    def __init__(self, baseAttack,hp, maxHp, exp, level ):
        Character.__init__(self, baseAttack,hp, maxHp, exp)

        self.__level = level

    # getters
    def getLevel(self):
        return self.__level


    # setters
    def setLevel(self, level):
        self.__level = level

    # method to set exp needed to level up
    def expToNextLevel(self):
        return self.__level * 10
    
    # level up method 
    def levelUp(self):
        self.__level +=1
        self.increaseMaxHp()
        self.setHp(self.getMaxHp())
        self.increaseBaseATK()

    # method to check if player can level up
    def levelUpCheck(self):
        leveledUp = False
        while True:
            requiredExp = self.expToNextLevel()

            if self.getExp() < requiredExp:
                break

            self.setExp(self.getExp() - requiredExp) 
            self.levelUp()
            leveledUp = True
        return leveledUp

    # method to increase max health
    def increaseMaxHp(self):
        self.setMaxHp(self.getMaxHp() + rollDice(6))

    # method to increase  health
    def increaseHp(self):
        self.setHp(self.getHp() + rollDice(4))

    # method to increase base attack
    def increaseBaseATK(self):
        self.setBaseAttack(self.getBaseAttack() + rollDice(6))
    
    # method to decrease base attack
    def decreaseATK(self):
        self.setBaseAttack(self.getBaseAttack() - rollDice(4))

    # method to decrease max health
    def decreaseMaxHp(self):
        
        self.setMaxHp(self.getMaxHp() - rollDice(4))
        if self.getHp() > self.getMaxHp():
            self.setHp(self.getMaxHp())
        