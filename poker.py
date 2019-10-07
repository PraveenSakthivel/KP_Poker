import random
import math
from collections import Counter

#Create a shuffled deck of cards
def create_deck():
    deck = list(range(52))
    random.shuffle(deck)
    return deck

#Create graphics for each list of cards
def card_graphic(cards):
    suits = ["♠","♣", "♥","♦"]
    ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    top_line=suit_line=rank_line=bottom_line = ""
    for card in cards:

        suit = math.floor(card / 13)
        rank = card % 13
        color = 37 #Set initial color to black
        if  card > 25: #If card is a red card set color to red
            color = 31

        top_line += "\033[1;{0};40m".format(color)
        suit_line += "\033[1;{0};40m".format(color)
        rank_line += "\033[1;{0};40m".format(color)
        bottom_line += "\033[1;{0};40m".format(color)

        if card == -1: #Show a blank card
            top_line += " ___     "
            suit_line += "|   |    "
            rank_line += "|   |    " 
            bottom_line += "|___|    "
            continue


        top_line += " ___ ".format(color)
        suit_line  += "|{1}  |".format(color,suits[suit])
        if rank % 13 == 9: #Check if rank is 10, then we need to remove a space
            rank_line += "| {1}|".format(color,ranks[rank])
        else:
            rank_line += "| {1} |".format(color,ranks[rank])
        bottom_line += "|___|".format(color)

        top_line += "    "
        suit_line += "    "
        rank_line += "    " 
        bottom_line += "    "

    top_line += "\n"
    suit_line += "\n"
    rank_line += "\n" 
    bottom_line += "\n\033[0;37;40m"
    return top_line + suit_line + rank_line + bottom_line

#Draw the number of cards from the deck
def draw_deck(deck,num):
    draw = deck[0:num]
    deck = deck[num:]
    return (draw,deck)

#Get the bet from the user
def get_bet(account):
    while(True):
        bet = input("Place your bet (Enter 0 to check): ")
        if bet.isnumeric():
            bet = int(bet)
            if bet > account:
                print("You do not have enough money to place that bet\n")
                continue
            return bet
        else:
            print("Invalid entry, please enter a number\n")

#Deal the starting hands
def get_hands(deck):
    draw, deck = draw_deck(deck,2)
    user_hand = draw
    draw, deck = draw_deck(deck,2)
    cpu1_hand = draw
    draw, deck = draw_deck(deck,2)
    cpu2_hand = draw
    draw, deck = draw_deck(deck,5)
    table_hand = draw

    return (user_hand, cpu1_hand, cpu2_hand, table_hand, deck)

def get_points(hand, table_hand):
    points = 0
    cards = hand + table_hand
    cards.sort()
    royal_flushs = [[8,9,10,11,12],[21,22,23,24,25],[34,35,36,37,38],[47,48,49,50,51]]
    
    #Check for royal flush
    for flush in royal_flushs: 
        if all(card in cards for card in flush):
            points += 900

    #Check for Straight flush
    for start in range(0,2): 
        for i in range(start,start + 4):
            if cards[i] != cards[i + 1] + 1:
                break
            if i == (start + 4):
                if cards[i] % 13 < 5:
                    break
                points += 800

    #Get the number of time each card occurs in pool
    occurences = list(Counter([card % 13 for card in cards]).values())
    if 4 in occurences:
        points += 700

    #Check for full house
    if 3 in occurences and 2 in occurences: 
        poker += 600
    
    #Check for flush
    suit_count = [0] * 4 
    for card in cards: 
        suit_count[math.floor(card / 13)] += 1
    if 5 in suit_count:
        poker += 500
    
    #Check for Straight
    rank_only = list(set([card % 13 for card in cards]))
    rank_only.sort()
    counter = 0
    for start in range(len(rank_only) - 5):
        for i in range(start, start + 4):
            if rank_only[i] != rank_only[i + 1] + 1:
                break
            if i == (start + 4):
                if cards[i] % 13 < 5:
                    break
                points += 400     

    #Check for 3 of a kind
    if 3 in occurences:
        points += 300

    #Check for 2 pairs
    if occurences.count(2) == 2:
        points += 200
    
    #Check for pair
    if 2 in occurences:
        points += 100
    
    #Get high card
    points += max([card % 13 for card in cards])
    return points


#Game runner
def play_game(account):
    turned_card = " ___ \n|   |\n|   |\n|___|"
    welcome_message = "\nWelcome to Poker! You are playing against two players "\
    "who will match all bets\nYou currently have {} dollars\n".format(account)
    print(welcome_message)
    deck = create_deck()
    bet = get_bet(account)
    account -= bet
    user_hand, cpu1_hand, cpu2_hand, table_hand, deck = get_hands(deck)
    print("Here is your hand:")
    print(card_graphic(user_hand))

    #Loop through revealing the community pile
    for turn in range(5):
        print("__________\n")
        print("Here is the community pool: ")
        community = table_hand[0:turn] + ([-1] * (5 - turn))
        print(card_graphic(community))
        print("\nHere is your hand:")
        print(card_graphic(user_hand))
        bet = get_bet(account)
        account -= bet
    print("__________\n")
    print("Here is the community pool: ")
    print(card_graphic(table_hand))

    #Calculate the value of each hand
    user_pts = get_points(user_hand,table_hand)
    cpu1_pts = get_points(cpu1_hand,table_hand)
    cpu2_pts = get_points(cpu2_hand,table_hand)

    #Find the winner
    if user_pts == cpu1_pts:
        if user_pts == cpu2_pts:
            print("It's a 3 way tie! The pot has been split")
            account += bet
        else:
            print("You tied with CPU 1")
            account += bet * 1.5
    elif user_pts == cpu2_pts:
        print("You tied with CPU 2")
        account += bet * 1.5
    elif user_pts > cpu1_pts and user_pts > cpu2_pts:
        print("You won!")
        account += bet * 3
    elif cpu1_pts > cpu2_pts:
        print("CPU 1 won with this hand: ")
        print(card_graphic(cpu1_hand))
    else:
        print("CPU 2 won with this hand: ")
        print(card_graphic(cpu2_hand))
    return account

account = 100    
while(True):
    account = play_game(account)
    play_again = input("\nPlay Again (y/n):")
    if play_again.lower() == 'n':
        break


    

    



