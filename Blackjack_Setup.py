import random

try:
    import tkinter
except:     # Python 2
    import Tkinter as tkinter

# print(tkinter.TkVersion)
# PNG impage file only work on tkinter 8.6 and higher


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'pmm'

    # For each suit, retrieve the image for the cards

    for suit in suits:
        # First the numbered cards (1 to 10)
        for card in range(1, 11):
            name = 'cards\\{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image))

        # Secondly the face cards

        for card in face_cards:
            name = 'cards\\{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image))


def deal_card(frame):
    # pop the next card off the top of the deck
    # NB. Pop is a way of retrieving an item from a list
    # at the same time removing that card
    next_card = deck.pop(0)    # 0 is the index of the card to pop (card on top of deck)
    # then add the card to the bottom of the deck
    deck.append(next_card)
    # add the image to a Label and display the ;label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calculates the total score of all cards in th list.
    # Only one ace can have a value of 11, and this will be reduced to 1
    # if the hand would bust.
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # If the hand would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score

def shuffle():
    random.shuffle(deck)

def deal_dealer():
    # Get the score of the card that's initially dealt to the dealer
    dealer_score = score_hand(dealer_hand)
    # The dealer cannot end with a score of less than 17
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer wins")
    else:
        result_text.set("Draw!")


def deal_player():
    player_hand.append(deal_card(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer wins!")
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # If he would bust, check if there is an ace and subtract 10
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")
    # print(locals())     # Prints a list of all the local variables

# Set up the screen and the frames for the dealer and the player


def new_game():
    global dealer_card_frame
    global player_card_frame
    global player_hand
    global dealer_hand

    # Embed the frames to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    # Embed frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    # Clear the result of the previous game
    result_text.set("")

    # Reset the scores
    player_score_label.set(0)
    dealer_score_label.set(0)

    # Create lists to store the dealer's and player's hands
    player_hand = []
    dealer_hand = []

    # Deal new initial cards
    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


mainWindow = tkinter.Tk()
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background="green")

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)
# Embedded frame to hold the cards images for the dealer
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar()
# player_score = 0
# player_ace = False
tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)
# Embedded frame to hold the card images for the player
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2, sticky='ew')

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3, sticky='ew')
# Load Cards
cards = []
load_images(cards)
print(cards)

# Create a new deck of cards and shuffle them
# deck = list(cards)

# Modifying the deck to be made up of multiple decks of cards
deck = list(cards) + list(cards) + list(cards)
random.shuffle(deck)

# Create the lists to store the dealer's and the player's hands
dealer_hand = []
player_hand = []

# Initially the dealer deals himself a card and then deals two cards to
# the player


deal_player()
dealer_hand.append(deal_card(dealer_card_frame))
dealer_score_label.set(score_hand(dealer_hand))
deal_player()

mainWindow.mainloop()
