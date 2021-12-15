import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')

class ControlStock():
    def __init__(self):
        self.all_money = 0
        # ↓↓ Choice your gain here ↓↓ 
        self.percentage = 50
        # Open the .csv
        self.dataframe = pd.read_csv('Control_Stock.csv')
        self.dataframe.drop(labels=['Unnamed: 0'], axis=1, inplace=True)

    # Register a new item
    def cad_item(self, item, value):
        # Item
        self.item = item

        # Look for if have the item or not
        self.query = self.find_item(self.item)
        if self.query != None:
            return print('already registered.')
        
        # Price of the item
        self.value = value

        # Divide the price for the percentage, for show the real gain.
        self.gain = ((self.value * self.percentage) / 100)
        # Data for add the item into dataframe
        self.data_cad = {
            'item': [self.item],
            'value': [self.value],
            'gain': [self.gain],
            'amount': [0]}
        # Create a dataframe for concatenate with the main dataframe
        self.dataframe_cad = pd.DataFrame(data=self.data_cad)

        # Concatenate
        self.dataframe = pd.concat([self.dataframe, self.dataframe_cad])
        print('cad with sucess')
        self.save_modifications()
        
    # Find if exists the item
    def find_item(self, item):
        self.item = item
        self.query = self.dataframe.query(f"item == '{self.item}'")
        if self.query.empty == True:
            return None
        return (self.query)

    # Find index of the item
    def find_index(self, item):
        self.item = item
        for index, value in self.dataframe.iterrows():
            if self.dataframe['item'][index] == self.item:
                return index
        return None
    
    # Del item
    def drop_item(self, item):
        self.item = item
        for index, value in self.dataframe.iterrows():
            # 'item name' == 'item name'
            if value['item'] == self.item:
                self.dataframe.drop(index, axis=0, inplace=True)
                print('item is deleted')
                self.save_modifications()

    # Save the dataframe
    def save_modifications(self):
        self.dataframe.to_csv('Control_Stock.csv', mode='w')

    # Add amount
    def add_amount(self, item, amount):
        self.item = item
        self.amount = amount
        # Find index of the item
        self.index = self.find_index(self.item)
        # If don't have, return warning
        if self.index == None:
            return print('not found...')
        # If have, sum the amount with the new amount.
        self.dataframe['amount'][self.index] += self.amount
        self.save_modifications()
        print('add with sucess.')

    # Del amount
    def del_amount(self, item, amount):
        self.item = item
        self.amount = amount
        # Find index of the item
        self.index = self.find_index(self.item)

        if self.index == None:
            # If don't have, return warning
            return print('not found...')

        elif self.dataframe['amount'][self.index] - self.amount < 0:
            # if the amount of now be smaller of the request, return warning.
            return print("don't have that amount to remove")

        else:
            # If have, subtraction the amount with the new amount.
            self.dataframe['amount'][self.index] -= self.amount
            self.save_modifications()
            print('amount del with sucess.')

    # Change price
    def change_price(self, item, new_price):
        self.item = item
        self.new_price = new_price
        self.new_gain = (new_price * self.percentage) / 100
        self.query = self.find_index(self.item)
        if self.query == None:
            return print('not found...')
        self.dataframe['value'][self.query] = self.new_price
        self.dataframe['gain'][self.query] = self.new_gain
        print('price be changed.')

    # Print the itens and the real gain
    def print_informations(self):
        self.all_gain = 0
        self.query = self.dataframe[self.dataframe['amount'] > 0]
        for index, value in self.query.iterrows():
            print(
                f"• item: {value['item']}\ngain total p/amount({value['amount']}): R$ {value['gain'] * value['amount']}\n")

            self.all_gain = self.all_gain + (value['gain'] * value['amount'])
            self.all_money = (self.dataframe['amount']*self.dataframe['value']).sum()
        return (f'Patrimony: R$ {self.all_money}\ntotal gain: R$ {self.all_gain}')
    # Gui with prompt.
    def GUI(self):
        while True:
            os.system('cls')
            print(
                f"(type 'exit' for exit)\n"
                f"1 ⇾  Find item.\n"
                f'2 ⇾  Add amount.\n'
                f'3 ⇾  Remove amount.\n'
                f'4 ⇾  Change price.\n'
                f'5 ⇾  Del item.\n'
                f'6 ⇾  Register item.\n')
            print(self.print_informations())

            self.input = (input('\nchoice: '))

            if self.input == 'exit':
                exit('closing application...')
            else:
                self.input = int(self.input)

            if self.input == 1:
                os.system('cls')
                print("choice: Find item\n")
                self.func = self.find_item(input("Type the name of item: "))
                print(self.func)
                os.system('pause')

            elif self.input == 2:
                os.system('cls')
                print("choice: Add amount\n")
                self.item = input('Type the name of item: ')
                self.amount = int(input("Type the amount: "))
                self.add_amount(self.item, self.amount)
                os.system('pause')

            elif self.input == 3:
                os.system('cls')
                print("choice: Del amount\n")
                self.item = input('Type the name of item: ')
                self.amount = int(input("Type the amount: "))
                self.del_amount(self.item, self.amount)
                os.system('pause')

            elif self.input == 4:
                os.system('cls')
                print("choice: Chance price\n")
                self.item = input('Type the name of item: ')
                self.new_price = int(input("Type new price: "))
                self.modifi_price(self.item, self.new_price)
                os.system('pause')

            elif self.input == 5:
                os.system('cls')
                print("Choice: Del cad\n")
                self.item = input('Type the name of item: ')
                self.drop_item(self.item)
                os.system('pause')

            elif self.input == 6:
                os.system('cls')
                print("Choice: Cad item\n")
                self.item = input('Type the name of item: ')
                self.value = int(input("Type the value R$ "))
                self.cad_item(self.item, self.value)
                os.system('pause')

p1 = ControlStock()
p1.GUI()