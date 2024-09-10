
from argparse import ArgumentParser
import sys


def get_min_payment(balance, fees=0):
    """ Computes minimum credit card payement using formula from balance fees and minimum percentage
     Parameters:
      - balance: total left to pay 
      - fees: default 0
      
      Returns:
      - min_payment: credit card payment minimum that is needed
      """
    m = 0.02
    b = balance
    f = fees
    min_payment = ((b * m) + f)
    if min_payment < 25: #makes sure min payment is always 25 or above
        min_payment = 25
    return min_payment

def interest_charged(balance, apr):
    """ Calculates interest charged in payments
     Parameters:
      - balance: total left to pay
      - apr: annual interest rate
    
     Returns:
      - i: amount of interest charged 
    """
    a = apr/100 # apr turns into decimal 
    y = 365 # days in a year
    b = balance 
    d = 30
    i = (a/y)*b*d
    return i

def remaining_payments(balance, apr, targetamount, credit_line=5000, fees=0):
    """ Calculates amount of payments needed to pay off credit card
     Parameters: 
      - balance: total left to pay
      - apr: annual interest rate
      - targetamount: target amount per payment deafult = none
      - credit_line: max amount allowed default = 5000
      - fees: default 0

     Returns:
      - total payment: payments needed to pay off credit card
      - above_25: number of month balance is over 25% of credit line
      - above_50: number of month balance is over 50% of credit line
      - above_75: number of month balance is over 75% of credit line
     """
    
    total_payments = 0
    above_25, above_50, above_75 = 0, 0 ,0 
    while balance > 0:
        if targetamount is None:
            payment_needed = get_min_payment(balance, fees)
        else:
            payment_needed = targetamount
        interest = interest_charged(balance, apr)
        payment_needed -= interest
        balance -= payment_needed

        if balance > 0.75 * credit_line:
            above_75 += 1
        if balance > 0.50 * credit_line:
            above_50 += 1
        if balance > 0.25 * credit_line:
            above_25 += 1
        total_payments +=1

        if payment_needed < 0:
            print("The card balance cannot be paid off.")
            quit()
        
    return total_payments, above_25, above_50, above_75
            

        


def main(balance, apr, targetamount=None, credit_line=5000, fees=0):
    """ Perfroms calculations based off of the above functions
    
    Returns: 
    Message that displays number of payments needed to pay off credit card balance and months above each (25, 50 ,75) threshold"""
    min_payment = get_min_payment(balance, fees)
    message = f"Your recommended starting minimum payment is ${min_payment}\n"

    pays_minimum = targetamount is None or targetamount <= min_payment

    if pays_minimum:
        total_payments, above_75, above_50, above_25 = remaining_payments(balance, apr, targetamount, credit_line=credit_line, fees=fees)
        message += f"If you pay the minimum payments each month, you will pay off the balance in {total_payments} payments.\n"
    else:
        total_payments, above_75, above_50, above_25 = remaining_payments(balance, apr, targetamount=targetamount, credit_line=credit_line, fees=fees)
        message += f"If you make payments of ${targetamount}, you will pay off the balance in {total_payments} payments.\n"

    message += f"You will spend a total of {above_25} months over 25% of the credit line\n"
    message += f"You will spend a total of {above_50} months over 50% of the credit line\n"
    message += f"You will spend a total of {above_75} months over 75% of the credit line\n"
    
    return message

def parse_args(args_list):
    """ Takes list of strings from command and passes as arguments"""
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type= float, help= 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type= int, help= 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')

    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments
.credit_line, targetamount = arguments.payment, fees = arguments.fees))
