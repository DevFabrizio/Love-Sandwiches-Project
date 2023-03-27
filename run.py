# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches_sheet')


def get_sales_data():
    """ Get sales figure imput from the user 
    Run a while loop to collect valid data input from the user from the terminal which must be a string of 6 numbers separated by commas. The loop will keep running until valid data is provided. """
    while True:
        print('Please enter sales data from the last market')
        print('Data should be six numbers, separated by commas.')
        print('Example: 10, 20, 30, 40, 50, 60\n')

        data_str = input('Enter your data here:')
        sales_data = data_str.split(',')
        validate_data(sales_data)
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """ Inside the try, converts all the values into integers.
        Raises ValueError if string can't be converted into int or if they aren't exaclty 6 values """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required! You provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data {e}. Please try again\n")
        return False
    return True    


def update_worksheet(data, worksheet):
    """ 
    Receives a list of integers to be inserted into the worksheet. Update the relevant worksheet with the data provided 
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"Worksheet {worksheet} successfully updated!\n")


    
def calculate_surplus(sales_row):
    """ Compare sales with stock and calculate surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates extra made when stock was sold out """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stocks, sales in zip(stock_row, sales_row):
        surplus = int(stocks) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """ Collects columns of data from sales worksheet, collecting the last 5 entries for each sandwich and returns the data as a list of lists """

    sales = SHEET.worksheet('sales')
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def main():
    """ Run all program functions """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus(sales_data)
    update_worksheet(new_surplus_data, 'surplus')

print('Welcome to Love Sandwiches data automation')
# main()
sales_columns = get_last_5_entries_sales()