# Owen Ramsey
# Character class
# March 20 2026

from DiceRoll import rollDice

# character class
class Character:
    
    #initialize the class
    def __init__(self, baseAttack,hp, maxHp, exp):
        self.__baseAttack = baseAttack
        self.__hp = hp
        self.__maxHp = maxHp
        self.__exp = exp
        

    # getters
    def getBaseAttack(self):
        return self.__baseAttack

    def getHp(self):
        return self.__hp
    
    def getMaxHp(self):
        return self.__maxHp
    
    def getExp(self):
        return self.__exp

    # setters
    def setBaseAttack(self, baseAttack):
        # make sure baseATK cant be less then 1
        if baseAttack < 1:
            self.__baseAttack = 1
        else:
            self.__baseAttack = baseAttack

    def setHp(self, hp):
        if hp < 0:
            self.__hp = 0
        elif hp > self.__maxHp:
            self.__hp = self.__maxHp
        else:
            self.__hp = hp
        

    def setMaxHp(self, maxHp):
        # make sure maxHp cant be less then 1
        if maxHp < 1:
            self.__maxHp = 1
        else:
            self.__maxHp = maxHp

    def setExp(self, exp):
        self.__exp = exp


    # attack method
    def attack(self):
        # retrun the base attack + the role for total damage
        return self.__baseAttack + rollDice(6)

    # method to decrease hp
    def decreaseHP(self, damage):
        self.setHp(self.getHp() - damage)