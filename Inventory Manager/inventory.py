from tabulate import tabulate


class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return(self.cost)

    def get_quantity(self):
        return(self.quantity)

    def __str__(self):
        return("Code {}, {} from {}, has a cost of {} and current stock of {}. "
                .format(self.code, self.product, self.country,
                self.cost, self.quantity))


def read_shoes_data(shoes_list):
    try:
        with open("./inventory.txt", "r+") as file:
            #getting rid of newlines at end of each entry in the text file
            data = file.read().split("\n")
            #removing header that was imported with the text file
            data = data[1:]
            for i in range(0,len(data)):
                data[i] = data[i].split(",")
                #creating a shoe object for each line of data,
                # and appending to the shoes list
                shoes_list.append(Shoe(data[i][0], data[i][1], data[i][2],
                                    data[i][3], data[i][4]))
    except:
        print("Inventory file not found.")


def capture_shoes(shoes_list):
    country = input("What is the country of origin for this pair of shoes? ")
    code = input("Enter the product code: ")
    product = input("Enter the product name: ")

    #cost and quantity must be entered as valid integers
    while True:
        try:
            cost = int(input("Enter the cost of this pair of shoes as an"
                            " integer value: "))
            cost = str(cost)
            break
        except:
            print("Invalid entry, try again.")

    while True:
        try:
            quantity = int(input("Enter the stock quantity of this pair of"
                                " shoes as an integer value: "))
            quantity = str(quantity)
            break
        except:
            print("Invalid entry, try again.")

    #creating the new object of Shoe class, and appending it to the shoes list
    shoes_list.append(Shoe(country, code, product, cost, quantity))
    '''
    Adding the new shoe object to the text file.
    '''
    with open("./inventory.txt", "a") as file:
        file.write("\n" + country + "," + code + "," + product + "," +
                cost + "," + quantity)


def view_all(shoes_list):
    #variables in each Shoe object are broken down into a
    #simple nested list for ease of tabulation
    shoes_variables = []
    for shoe in shoes_list:
        shoes_variables.append([shoe.country, shoe.code,
                            shoe.product, shoe.get_cost(), shoe.get_quantity()])

    #turning the nested list into a table
    table = tabulate(shoes_variables,
                    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
                    ,tablefmt = "rst")
    print(table)


def search_shoe(shoes_list, shoe_code):
    for shoe in shoes_list:
        if shoe.code == shoe_code:
            return(shoe)


def re_stock(shoes_list):
    '''
    Identify the shoe with the lowest quantity in stock,
    prompt the option to restock, and take in the amount
    by which to do so if selected.
    The increased stock value is updated in the shoe object,
    as well as the text file.
    '''

    lowest = min(shoes_list, key=lambda shoe: int(shoe.get_quantity()))
    #taking user input to restock or not
    add_quantity = input("Shoe code {}, {}, has remaining stock of {}."
                        " Would you like to restock (enter y/n): "
                        .format(lowest.code, lowest.product,
                                lowest.get_quantity()))

    while add_quantity not in ["y", "n"]:
        add_quantity = input("Invalid input. Would you like to restock"
                            " (enter y/n): ")

    #restocking chosen, they are now prompted to enter the quantity to order
    if add_quantity == "y":
        while True:
            try:
                order = int(input("Enter the quantity of inventory to restock"
                                " as an integer: "))
                break
            except:
                print("Invalid input, try again.")

        #using the search_shoe method to find the shoe given its code, so we
        # can update the stock quantity
        quantity = lowest.get_quantity() #since I can't pass a method into int()
        lowest.quantity = str(int(quantity) + order)
        print("Shoe code {}, {}, now has stock of {}."
                        .format(lowest.code
                                ,lowest.product
                                ,lowest.get_quantity()))
        '''
        Next step is to update the file.
        I do this by first reading it and adding the data to a list.
        From there, I identify the item with newly ordered stock by its code.
        The data list is updated accordingly, then written to the file,
        keeping the format as before.
        '''
        data = []
        with open("./inventory.txt", "r+") as file:
            data = file.read().split("\n")
            for i in range(0, len(data)):
                data[i] = data[i].split(",")
            #finding the shoe by code to update the stock quantity in the list
            code = lowest.code
            for i in range(0, len(data)):
                if data[i][1] == code:
                    cost = lowest.get_cost()
                    quantity = lowest.get_quantity()
                    data[i] = [lowest.country, lowest.code
                                ,lowest.product,cost,quantity]

        #writing the list to the file with updated information
        with open('./inventory.txt', 'w') as file:
            for i in range(0, len(data)):
                if i == 0:
                    file.write(data[i][0] + "," + data[i][1] + "," + data[i][2]
                            + "," + data[i][3] + "," + data[i][4])
                else:
                    file.write("\n" + data[i][0] + "," + data[i][1] + ","
                            + data[i][2] + "," + data[i][3] + "," + data[i][4])
    else:
        print("No additional stock has been ordered for shoe code {}."
            .format(lowest.code))
        pass


def value_per_item(shoes_list):
    for shoe in shoes_list:
        quantity = int(shoe.get_quantity())
        cost = int(shoe.get_cost())
        print("Shoe code {}, {}, has total value of {} in stock"
            .format(shoe.code,shoe.product,quantity*cost))


def highest_qty(shoes_list):
    '''
    Identify the shoes with the highest quantity, and then
    print a statement about it.
    '''
    highest = max(shoes_list, key=lambda shoe: int(shoe.get_quantity()))
    print("Shoe code {}, {}, has the highest stock quantity, at {}."
        " It is for sale."
        .format(highest.code
                ,highest.product
                ,highest.get_quantity()))


'''
Executing the menu
'''
setting = "0"
print("Welcome to the inventory management portal."
    " Before commencing, ensure that the inventory list is available.")
setting = input("\n To begin, enter 1. To exit, enter -1: ")

#Only terminate once setting is set to "-1"
while True:
    if setting == "-1":
        print("\n Exiting the inventory management system.")
        break
    elif setting != "1":
        setting = input("\n Invalid input specified. To begin, enter 1."
                        " To exit, enter -1: ")
    else:
        shoes_list = []
        read_shoes_data(shoes_list)
        print("\n Select 2 to view your current stock list.")
        print(" Select 3 to add an entry to your stock list.")
        print(" Select 4 to identify the stock with the lowest inventory"
            " and get the option to order more.")
        print(" Select 5 to find an inventory item given the product code.")
        print(" Select 6 to view the total value of each item"
            " in your stock list.")
        print(" Select 7 to view the product with the highest inventory"
            " on hand, and put it up for sale.")
        print(" If you want to quit, select -1")
        setting = input("\n Given the options above, make your selection: ")

        if setting == "2":
            view_all(shoes_list)
            print("\n Returning back to the main menu. \n")
            setting = "1"

        if setting == "3":
            capture_shoes(shoes_list)
            print("\n Returning back to the main menu \n")
            setting = "1"

        if setting == "4":
            re_stock(shoes_list)
            print("\n Returning back to the main menu \n")
            setting = "1"

        if setting == "5":
            #search_setting: tracks whether to search again if an invalid code is entered
            search_setting = "1"
            while search_setting == "1":
                code = input("Enter the code of the product"
                            " you are looking for: ")
                shoe = search_shoe(shoes_list, code)
                if search_shoe(shoes_list, code) == None:
                    print("Oops, code did not match a shoe in the database.")
                    search_setting = input("\n Enter 1 if you would like"
                                        " to try again. Press any other key to"
                                        " return to the main menu.")
                else:
                    cost = shoe.get_cost()
                    quantity = shoe.get_quantity()
                    print("Code {}, {}, from {}. Cost is {}"
                        " and current stock quantity is {}"
                        .format(shoe.code, shoe.product,
                                shoe.country, cost, quantity))
                    search_setting = "-1"
                    print("\n Returning back to the main menu \n")
            setting = "1"

        if setting == "6":
            value_per_item(shoes_list)
            print("\n Returning back to the main menu \n")
            setting = "1"

        if setting == "7":
            highest_qty(shoes_list)
            print("\n Returning back to the main menu \n")
            setting = "1"





