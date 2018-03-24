from classes.game import bcolors, Person
from classes.magic import Spell
from classes.inventory import Item
import random
import termcolor


# black magic instantiation
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 200, "black")
blizzard = Spell("Blizzard", 10, 300, "black")
meteor = Spell("Meteor", 20, 500, "black")
quake = Spell("Quake", 14, 700, "black")

# white magic instantiation
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 1200 damage", 1200)

player_items = [
    {"item": potion, "quantity": 1},
    {"item": hipotion, "quantity": 2},
    {"item": superpotion, "quantity": 2},
    {"item": elixer, "quantity": 2},
    {"item": hielixer, "quantity": 1},
    {"item": grenade, "quantity": 6}
]

player1 = Person("Valos:", 4460, 265, 360, 125, player_magic, player_items)
player2 = Person("Nick :", 6460, 365, 460, 250, player_magic, player_items)
player3 = Person("Robot:", 7460, 465, 560, 301, player_magic, player_items)

enemy1 = Person("Cruel:", 1120, 150, 560, 325, enemy_magic, [])
enemy2 = Person("Magus:", 17200, 700, 525, 25, enemy_magic, [])
enemy3 = Person("Magog:", 1200, 135, 325, 300, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

print(bcolors.FAIL + "Enemy Attacks!!!" + bcolors.ENDC)
# print(termcolor.colored("Sa te imbogatesti", "red", "on_blue"))

defeated_enemies = 0
defeated_players = 0

running = True
i = 0

while running:
    print("===============================================")
    print("\n")
    print("NAME               HP                                    MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()

        choice = input("Choose action:")
        print("You choose: ", choice)
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            index_enemy = player.choose_target(enemies)
            enemies[index_enemy].take_damage(dmg)
            print("You attacked ", enemies[index_enemy].name,  " for ", dmg, " points of damage")

            if enemies[index_enemy].get_hp() == 0:
                print(enemies[index_enemy].name, " has died ")
                del enemies[index_enemy]
                defeated_enemies += 1

        if defeated_enemies >= 2:
            print(bcolors.OKGREEN + "You won!!!" + bcolors.ENDC)
            running = False
            break

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            # if the input is 0; magic_choice = -1, go back to the menu
            if magic_choice == -1:
                continue

            # this is an instance of Spell class with all properties and methods
            spell = player.magic[magic_choice]
            magic_dmg = spell.effective_dmg

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for "
                      + str(magic_dmg) + "HP: " + str(player.get_hp()) + bcolors.ENDC)
            elif spell.type == 'black':
                index_enemy = player.choose_target(enemies)
                enemies[index_enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " " + str(magic_dmg)
                 + " points of damage to " + enemies[index_enemy].name + bcolors.ENDC)

                if enemies[index_enemy].get_hp() == 0:
                    print(enemies[index_enemy].name, " has died ")
                    del enemies[index_enemy]
                    defeated_enemies += 1

        if defeated_enemies >= 2:
            print(bcolors.OKGREEN + "You won!!!" + bcolors.ENDC)
            running = False
            break

        elif index == 3:
            running = False
            break

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            # if the input is 0; item_choice = -1, go back to the menu
            if item_choice == -1:
                continue

            # item is a dictionary, with keys: "item", "quantity"
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left...get another item" + bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"] # the Item object
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for "
                      + str(item.prop) + "HP: " + str(player.get_hp()) + bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restore HP/MP " + bcolors.ENDC)

            elif item.type == "attack":
                index_enemy = player.choose_target(enemies)
                enemies[index_enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      " points of damage to " + enemies[index_enemy].name + bcolors.ENDC)

                if enemies[index_enemy].get_hp() == 0:
                    print(enemies[index_enemy].name, " has died ")
                    del enemies[index_enemy]
                    defeated_enemies += 1

            if defeated_enemies >= 2:
                print(bcolors.OKGREEN + "You won!!!" + bcolors.ENDC)
                running = False
                break

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        # choose attack
        if enemy_choice == 0:
            target_player = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            # get the random player, and apply attack
            target_player = random.randrange(0, 3)
            players[target_player].take_damage(enemy_dmg)
            print(enemy.name, " attacks ", players[target_player].name, " for ", enemy_dmg)

        # choose magic
        if enemy_choice == 1:
            spell = enemy.choose_enemy_spell()
            if spell:
                if spell.type == "black":
                    # get the index of the player
                    target_player = random.randrange(0, 3)
                    magic_dmg = spell.generate_dmg()
                    players[target_player].take_damage(magic_dmg)
                    print(enemy.name, " directed black magic to ",
                          players[target_player].name, " for ", magic_dmg)
                else:
                    magic_dmg = spell.generate_dmg()
                    enemy.heal(magic_dmg)
                    print(enemy.name, " white magic ", spell.name, " heals for ", magic_dmg)

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players >= 2:
        print(bcolors.FAIL + "Enemies have been defeated you!!!" + bcolors.ENDC)
        running = False



