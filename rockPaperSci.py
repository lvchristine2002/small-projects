

import sys
import argparse
import os

os.system('cls||clear')

def determine_winner(p1, p2):
    """Funtionality: player 1 picks from rockk, paper, or scissors (r,p,s) and then player 2 chooses as well
    Will return which player wins or players are tied"""
    if p1 == p2:
        return "tie"
    # checks combinations of rock, paper, and scissors to see who wins
    elif p1 == "r":
        if p2 == "s":
            return "player1"
        else:
            return "player2"
    elif p1 == "s":
        if p2 == "p":
            return "player1"
        else:
            return "player2"
    elif p1 == "p":
        if p2 == "r":
            return "player1"
        else:
            return "player2"

def main(player1_name, player2_name):
    """Functionality: asks player 1 and 2 for hand shape 
    Will call on determine_winner function to determine winner
    Saves the return value using print function"""
    player1_choice = input("Player 1 pick r,p,s (rock, paper, or scissors)'")
    player2_choice = input("Player 2 pick r,p,s (rock, paper, or scissors)")
    # calls determine_winner() 
    if determine_winner(player1_choice,player2_choice) == "tie":
        print("tie!")
    elif determine_winner(player1_choice, player2_choice) == "player1":
        print(player1_name + "wins!")
    else: 
        print(player2_name + "wins!")


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
arguments
  Args:
  args_list (list) : the list of strings from the command prompt
  Returns:
  args (ArgumentParser)"""
    parser = argparse.ArgumentParser() #Create an ArgumentParser object.
    parser.add_argument('p1_name', type=str, help="Please enter Player1's Name")
    parser.add_argument('p2_name', type=str, help="Please enter Player2's Name")
    args = parser.parse_args(args_list) 
    return args

if __name__ == "__main__":
     arguments = parse_args(sys.argv[1:])
     main(arguments.p1_name, arguments.p2_name)
