import random as rnd

"""
***READ BEFORE PLAYING***

Scoundrel is a dungeon crawler that's played with a regular deck of playing cards.
In this game, you use the lettered HEARTS and DIAMONDS (J,Q,K,A) as your health, so
those cards wont appear in the dungeon.

The dungeon consists of rooms that have 4 cards each.
There are 3 types of cards:
    1. HEARTS: Potions that restore HP. There is no overhealing so use it wisely.
    Once you use a potion, it is consumed and sent to the discard pile.

    2. SPADES & CLUBS: Monsters that deal damage. Whenever they attack the user
    they disappear and are sent to the discard pile.

    3. DIAMONDS: Shields that block damage from incoming attacks. Whenever a shield
    blocks an attack, its DURABILITY gets set to the value of the last card blocked.
    A shield with a DURABILITY of 'x' can only block attacks of a value of 'x-1'.
    You can only hold one shield at a time and whenever you equip a shield, the previous
    one gets sent to the discard pile.
    
When there's one card left, you can either refill the room with 3 more cards or play that
last card as per usual.
"""

MAX_HEALTH = 20
health = MAX_HEALTH

SUIT_UNICODE = {
    'C': '\u2663',  # CLUBS
    'H': '\u2665',  # HEARTS
    'D': '\u2666',  # DIAMONDS
    'S': '\u2660'   # SPADES
}

SUIT_LABEL = {
    'C': 'damage',
    'H': 'heal',
    'D': 'block',
    'S': 'damage'
}

SUITS = ['C', 'H', 'D', 'S']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
LETTER_RANKS = ['A', 'J', 'Q', 'K']
VALUES = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}

# DECK BUILDING
deck = [{'rank': rank, 'suit': suit, 'value': VALUES[rank]}
        for suit in SUITS for rank in RANKS]
deck = [card for card in deck if not
(card['suit'] in ['H', 'D'] and card['rank'] in LETTER_RANKS)]
rnd.shuffle(deck)

def card_display(card):
    suit_symbol = SUIT_UNICODE[card['suit']]
    label = SUIT_LABEL[card['suit']]
    return f"{card['rank']}{suit_symbol}, {label}: {card['value']}"

def fill_room(card_deck):
    # CREATES A "ROOM" THAT CONTAINS 4 CARDS
    room = []
    print('\nCurrent room:')
    i = 0

    for card in range(min(4, len(card_deck))):
        card_in_room = card_deck.pop(0)
        room.append(card_in_room)
        print(f'\t{i + 1}. {card_display(room[i])}')
        i += 1
    return room

def fill_room_mid(card_deck, room):
    """REFILLS THE ROOM BACK TO 4 CARDS"""
    cards_to_add = min(3, len(card_deck))  # only need 3 since 1 card remains
    for x in range(cards_to_add):
        room.append(card_deck.pop(0))
    print('\nRoom refilled! Current room:')
    for i, card in enumerate(room):
        print(f'\t{i+1}. {card_display(room[i])}')

def display_hp_and_choice(room, hp, card_deck):
    """
    SHOWS HP AND SHIELD, THEN ASKS FOR THE PLAYER TO PICK A CARD
    AFTER THE PLAYER PICKS A CARD, IT TURNS IT INTO CHOSEN CARD
    """
    try:
        # Display HP + Shield
        if len(hp) == 1:
            print(f'Your current health is {hp[0]} HP')
        elif len(hp) == 2:
            print(f'Your current health is {hp[0]} HP. '
                  f'\n\tShield: {hp[1]['value']} BLOCK')
        elif len(hp) > 2:
            print(f'Your current health is {hp[0]} HP. '
                  f'\n\tShield: {hp[1]['value']} BLOCK ; Durability: {hp[len(hp) - 1]['value']}')

        # LAST CARD IN ROOM
        if len(room) == 1:
            if len(card_deck) == 0:
                print('(Use 1 to pick a card. This is the last card...)')
                player_action = int(input('What do you want to do? '))
            else:
                print('(Use 1 to pick a card) (Use 5 to refill the room)')
                player_action = int(input('What do you want to do? '))
                if player_action == 5:
                    fill_room_mid(card_deck, room)
                    player_action = int(input('What do you want to do? '
                                              + '(Use 1-' + str(len(room)) + ' to pick a card) '))
        else:
            player_action = int(input('What do you want to do? '
                                      + '(Use 1-' + str(len(room)) + ' to pick a card) '))

    except ValueError:
        player_action = 0

    while player_action > (len(room)) or player_action < 1:
        try:
            player_action = int(input('Nothing happened...' + '\n(Use 1-' + str(len(room)) + ' to pick a card) '))
        except ValueError:
            player_action = 0

    chosen_card = room.pop(player_action - 1)
    return chosen_card
    """
    SHOWS HP AND SHIELD, THEN ASKS FOR THE PLAYER TO PICK A CARD
    AFTER THE PLAYER PICKS A CARD, IT TURNS IT INTO CHOSEN CARD
    """


def action(room, hp, discard_pile, card_deck):

    while len(room) > 0:
        chosen_card = display_hp_and_choice(room, hp, card_deck)
        # returns chosen card

        # HEARTS
        if chosen_card['suit'] == 'H':
            restored_health = min(chosen_card['value'], MAX_HEALTH - hp[0])
            hp[0] = min(MAX_HEALTH, hp[0] + chosen_card['value'])
            print(f"You restored {restored_health} HP! \nYour health is now {hp[0]} HP")
            discard_pile.append(chosen_card)

        # DIAMONDS
        if chosen_card['suit'] == 'D':
            shield = chosen_card['value']

            # No shield equipped
            if len(hp) == 1:
                hp.append(chosen_card)
                print(f"You equipped a shield! Blocks up to {shield} damage from every attack")

            # Shield no DMG equipped
            elif len(hp) == 2:
                print(f"You already have a {hp[1]['value']} BLOCK shield!"
                      f"\nWould you like to trade it for the {shield} BLOCK shield?")

                try:
                    response = input(f"\t0. Keep current shield ({hp[1]['value']} BLOCK)"
                                     f"\n\t1. Swap for new shield ({shield} BLOCK)")
                except ValueError:
                    response = -1

                while int(response) < 0 or int(response) > 1:
                    try:
                        response = input(f"\t0. Keep current shield ({hp[1]['value']} BLOCK)"
                                         f"\n\t1. Swap for new shield ({shield} BLOCK)")
                    except ValueError:
                        response = -1
                # Final part
                if int(response) == 0:
                    discard_pile.append(chosen_card)
                else:
                    discard_pile += [hp.pop() for i in range(len(hp) - 1)]
                    print(f"You equipped a shield! Blocks up to {shield} damage from every attack")

            # Shield w/damage
            elif len(hp) >= 3:
                print(
                    f"You already have a {hp[1]['value']} BLOCK shield! (Shield durability: {hp[len(hp) - 1]['value']})"
                    f"\nWould you like to trade it for the {shield} BLOCK shield?")

                try:
                    response = input(f"\t0. Keep current shield ({hp[1]['value']} BLOCK)"
                                     f"\n\t1. Swap for new shield ({shield} BLOCK)")
                except ValueError:
                    response = -1

                while int(response) < 0 or int(response) > 1:
                    try:
                        response = input(f"\t0. Keep current shield ({hp[1]['value']} BLOCK)"
                                         f"\n\t1. Swap for new shield ({shield} BLOCK)")
                    except ValueError:
                        response = -1
                # Final part
                if int(response) == 0:
                    discard_pile.append(chosen_card)
                else:
                    discard_pile += [hp.pop() for i in range(len(hp) - 1)]
                    hp.append(chosen_card)
                    print(f"You equipped a shield! Blocks up to {shield} damage from every attack")

        # SPADES & CLUBS
        if chosen_card['suit'] == 'S' or chosen_card['suit'] == 'C':
            # NO SHIELD EQUIPPED
            if len(hp) == 1:
                damage_taken = chosen_card['value']
                hp[0] -= chosen_card['value']
                print(f"You took {damage_taken} damage! \nYour current health is {hp[0]} HP")
                discard_pile.append(chosen_card)

            # SHIELD EQUIPPED
            if len(hp) >= 2:
                damage_taken = chosen_card['value']
                if len(hp) == 2:
                    print(
                        f"The enemy will deal {damage_taken} damage. Do you wish to use your shield ({hp[1]['value']} BLOCK)?")
                else:
                    print(
                        f"The enemy will deal {damage_taken} damage. Do you wish to use your shield ({hp[1]['value']} BLOCK) (Durability: {hp[len(hp) - 1]['value']})?")
                try:
                    use_shield = int(input(f"\t0. Don't use shield"
                                           f"\n\t1. Use shield (will reduce durability)"))
                except ValueError:
                    use_shield = -1

                while int(use_shield) < 0 or int(use_shield) > 1:
                    try:
                        use_shield = int(input(f"\t0. Don't use shield"
                                               f"\n\t1. Use shield (will reduce durability)"))
                    except ValueError:
                        use_shield = -1

                # DON'T USE SHIELD
                if use_shield == 0:
                    damage_taken = chosen_card['value']
                    hp[0] -= chosen_card['value']
                    print(f"You took {damage_taken} damage! \nYour current health is {hp[0]} HP")
                    discard_pile.append(chosen_card)

                # USE SHIELD
                if use_shield == 1:
                    # SHIELD HASN'T BEEN USED
                    if len(hp) == 2:
                        postblock_dmg = max(0, damage_taken - hp[1]['value'])
                        hp[0] -= postblock_dmg
                        hp.append(chosen_card)
                        print(f"You blocked the attack with your shield! You took {postblock_dmg} damage!"
                              f"\nYour current health is {hp[0]} HP. Your shield durability is now {hp[len(hp) - 1]['value']}")

                    # SHIELD HAS BEEN USED BEFORE
                    elif len(hp) > 2:
                        if damage_taken >= hp[len(hp) - 1]['value']:
                            hp[0] -= chosen_card['value']
                            print(f"Your shield was too damaged and couldn't block! You took {damage_taken} damage!"
                                  f"\nYour current health is {hp[0]} HP")
                            discard_pile.append(chosen_card)
                        else:
                            postblock_dmg = max(0, damage_taken - hp[1]['value'])
                            hp[0] -= postblock_dmg
                            hp.append(chosen_card)
                            print(f"You blocked the attack with your shield! You took {postblock_dmg} damage!"
                                  f"\nYour current health is {hp[0]} HP. Your shield durability is now {hp[len(hp) - 1]['value']}")

        if hp[0] <= 0:
            print("\nYou were hit a fatal blow")
            break

        if len(room) > 0:
            print('\nCurrent room:')

        for i in range(len(room)):
            print('\t' + str(i + 1) + '.', card_display(room[i]))

    return hp


def game():
    health = [MAX_HEALTH]
    graveyard = []
    while deck and health[0] > 0:
        # print(f'Your current health is {health[0]} HP')
        room = fill_room(deck)
        health = action(room, health, graveyard, deck)

    if health[0] > 0:
        print('You win!')
    else:
        print('You lost...')


def main():
    print("WELCOME TO SCOUNDREL! The card based dungeon crawler")
    print()
    print('You enter the dungeon...')
    game()


if __name__ == '__main__':
    main()