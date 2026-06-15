# About the game
This is my first project on GitHub. It is based on the game Scoundrel created in 2011 by Zach Gage and Kurt Bieg

# RULES:
Scoundrel is a dungeon crawler that's played with a regular deck of playing cards.
In this game, you use the lettered HEARTS and DIAMONDS (J,Q,K,A) as your health, so
those cards wont appear in the dungeon.

The dungeon consists of rooms that have 4 cards each.
When there's one card left, you can either refill the room with 3 more cards or play that
last card as per usual.

There are 3 types of cards:
    
# 1. HEARTS: 
Potions that restore HP. There is no overhealing so use it wisely.
Once you use a potion, it is consumed and sent to the discard pile.
    
# 2. SPADES & CLUBS: 
Monsters that deal damage. Whenever they attack the user
they disappear and are sent to the discard pile.
    
# 3. DIAMONDS: 
Shields that block damage from incoming attacks. Whenever a shield
blocks an attack, its DURABILITY gets set to the value of the last card blocked.
A shield with a DURABILITY of 'x' can only block attacks of a value of 'x-1'.
You can only hold one shield at a time and whenever you equip a shield, the previous
one gets sent to the discard pile.
