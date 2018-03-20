import random
import colorama
import os
from .magic import Spell

convert = ''
strip = ''

if 'PYCHARM_HOSTED' in os.environ:
    convert = False  # in PyCharm, we should disable convert
    strip = False
    print("Hi! You are using PyCharm")
else:
    convert = None
    strip = None


class bcolors():

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKMAGENTA = '\33[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        self.colorama_init()

    def colorama_init(self):
        colorama.init(convert=convert, strip=strip)


class Person:
    '''
        mp: magic points
        hp: health points
        atk: attack strength in points
        df: defense points
        magic: list of instances of class Spell
    '''
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items", "Quit"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp >= self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i), ". ", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i), ". ", spell.name,
                  "(cost/damage: ", str(spell.cost) + "/" +
                  str(spell.effective_dmg) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKMAGENTA + bcolors.BOLD + "ITEMS" + bcolors.ENDC)
        # item is a dictionary with "item", "quantity" keys
        for item in self.items:
            print("    " + str(i), ". ", item["item"].name, ": ", item["item"].description,
                  "(x" + str(item["quantity"]) + ")")
            i += 1

    def get_stats(self):
        print("NAME               HP                                  MP            ")
        print("                   _________________________           ___________  ")
        print(bcolors.BOLD +
              self.name + "   " +
              str(self.hp) + "/" + str(self.maxhp) + "  " + "|" +
              bcolors.OKGREEN + "███████████       " + " |" +
              bcolors.BOLD + "   " + str(self.mp) + "/" + str(self.maxmp) + " |" +
              bcolors.OKMAGENTA + "█████   " + "|")
