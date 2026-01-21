# the game logic for blackjack i wrote myself, but i used ai to help with streamlit and actually display the content

import streamlit as st
import random

# initialize game state
# if the player has hit play again dont do any of this though. 
# code further down says if we the deck hasnt be initialized for some reason, initialize it, since there was a weird bug if you hit play too fast
if 'deck' not in st.session_state:
    st.session_state.deck = []
    st.session_state.player_hand = []
    st.session_state.dealer_hand = []
    st.session_state.game_over = False
    st.session_state.result = ""

def create_deck():
    # we dont use suits because it doesnt really matter
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return ranks * 4

# we have to specify the score of jacks, queens, kings and aces, but for other ranks we can just add their rank number to the score
def calculate_score(hand):
    score = 0
    aces = 0
    values = {'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    for card in hand:
        if card in values:
            score += values[card]
            # fixing weird ace bug
            if card == 'A':
                aces += 1
        else:
            score += int(card)
    
    # even tho there aren't any suits we still have to account for aces
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

#.pop removes an item from a list, while append adds it
def start_new_game():
    st.session_state.deck = create_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    st.session_state.result = ""
#if you go over 21 you lose
def hit():
    st.session_state.player_hand.append(st.session_state.deck.pop())
    if calculate_score(st.session_state.player_hand) > 21:
        st.session_state.result = "Bust! You lose."
        st.session_state.game_over = True

def stand():
    st.session_state.game_over = True
    # dealer must hit until they reach at least 17 as per da rules
    while calculate_score(st.session_state.dealer_hand) < 17:
        st.session_state.dealer_hand.append(st.session_state.deck.pop())
    
    p_score = calculate_score(st.session_state.player_hand)
    d_score = calculate_score(st.session_state.dealer_hand)
    
    if d_score > 21:
        st.session_state.result = "Dealer busts! You win!"
    elif p_score > d_score:
        st.session_state.result = "You win!"
    elif d_score > p_score:
        st.session_state.result = "Dealer wins!"
    else:
        st.session_state.result = "It's a tie!"

st.title("Blackjack")
st.write("You may have to click Deal New Game twice to initialize the deck properly")

# if we haven't already initialized the deck, start a new game. the code at the top says if we hit play again we dont initialize everything to save a few seconds
if not st.session_state.deck:
    if st.button("Deal New Game"):
        start_new_game()
else:
    # Dealer Area
    st.subheader("Dealer's Hand")
    d_cards = st.session_state.dealer_hand
    if not st.session_state.game_over:
        # hide the dealer's second card
        st.write(f"[{d_cards[0]}] [?]")
    else:
        st.write(f"{'  '.join(d_cards)}  (Total: {calculate_score(d_cards)})")

    st.subheader("Your Hand")
    p_cards = st.session_state.player_hand
    st.write(f"{'  '.join(p_cards)}  (Total: {calculate_score(p_cards)})")

    # buttons
    if not st.session_state.game_over:
        col1, col2 = st.columns(2)
        with col1:
            st.button("Hit", on_click=hit, use_container_width=True)
        with col2:
            st.button("Stand", on_click=stand, use_container_width=True)
    else:
        if "you win" in st.session_state.result.lower() or "dealer busts" in st.session_state.result.lower():
            text_color = "#2ecc71"  # green if u win
        elif "dealer wins" in st.session_state.result.lower() or "lose" in st.session_state.result.lower() or "bust" in st.session_state.result.lower():
            text_color = "#e74c3c"  # red if you lose
        else:
            text_color = "#e3e01b"  # yellow for ties

        # Display the styled result
        st.markdown(f"""
            <div style="background-color:{text_color}; padding:20px; border-radius:10px; text-align:center;">
                <h1 style="color:white; margin:0;">{st.session_state.result}</h1>
            </div>
            <br>
            """, unsafe_allow_html=True)
            
        st.button("Play Again", on_click=start_new_game, use_container_width=True)