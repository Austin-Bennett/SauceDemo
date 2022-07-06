import os
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver

os.system("")

# WebDriver options
options = webdriver.ChromeOptions()
#options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\austi\Documents\GitHub\SauceDemo\chromedriver.exe")
driver.implicitly_wait(1)
wait = WebDriverWait(driver, 1)


# Username and Password Definitions
standard_username = "standard_user"
problem_username = "problem_user"
locked_username = "locked_out_user"
glitch_username = "performance_glitch_user"
password = "secret_sauce"


inventory_list = []
#current_inventory_list = []
list_descriptors = ["Item Name", "Item Description", "Item Price", "In/Out of Cart", "Image"]


# Log in with standard user, pull the proper inventory item information and save to a text file for future pulls.
def initialize():

    login_to_saucedemo(standard_username, password)
    get_inventory_list(inventory_list)
    dump_inventory_list_to_txt_file(inventory_list)

    

# Log in
def login_to_saucedemo(user = standard_username, pw = password):

    elem = driver.find_element(By.ID, "user-name")
    elem.send_keys(user)

    elem = driver.find_element(By.ID, "password")
    elem.send_keys(pw)

    elem.send_keys(Keys.RETURN)

# Create a list of html elements for each 'Inventory Item' that we want to analyze for errors.
# Saved in CSV Format: 'inventory_item_name', 'inventory_item_desc', 'inventory_item_price', 'Boolean for In Cart', 'inventory_item_img'
def get_inventory_list(list):

    elements = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")

    for element in elements:
        list.append([element.find_element(By.CLASS_NAME, "inventory_item_name").text,
                               element.find_element(By.CLASS_NAME, "inventory_item_desc").text,
                               element.find_element(By.CLASS_NAME, "inventory_item_price").text,
                               'Add to cart',
                               element.find_element(By.TAG_NAME, "img").get_attribute("src")])


# Create a text file with the contents of inventory_list.
# The purpose of this would be to create a baseline for what the correct inventory_list should look like when logging in with 'standard_user'.
# Saved in CSV Format: 'inventory_item_name', 'inventory_item_desc', 'inventory_item_price', 'Boolean for In Cart', 'inventory_item_img'
def dump_inventory_list_to_txt_file(inventory_list):

    text_file = open("inventory_list.txt", "wt")
    
    for item in inventory_list:
        counter = 0
        for i in item:
            counter+=1
            if counter == len(list_descriptors):
                text_file.write(i)
            else:
                text_file.write(i + '&&')
        text_file.write('^^')

    text_file.close()
    

# Read inventory items from file into inventory_list
def load_inventory_items():

    f = open("inventory_list.txt")
    lines = f.read()
    lines = lines[:-2]
    lines = lines.split('^^')

    for line in lines:
        inventory_list.append(line.split('&&'))


# Sort items: Name A to Z, Name Z to A, Price L to H, Price H to L, respectively.
def sort_items(sort_by='name', reverse=False):

    if sort_by == 'name':
        if reverse == False:
            inventory_list.sort()
        else:
            inventory_list.sort(reverse=reverse)

    elif sort_by == 'price':
        if reverse == False:
            # Remove $ from price string, convert from string to float, sort by price with name as tie-breaker.
            inventory_list.sort(key = lambda x: (float(x[2][1:]), x[0]))
        else:
            # Same as above but not using name as tie-breaker due to reverse=True making the tie breaker be in reverse alphabetical order (based on saucedemo.com results we want alphabetical order in case of tie breaking).
            inventory_list.sort(key = lambda x: float(x[2][1:]), reverse=reverse)


# Sort by 
def select_sort(sort_by = 'az'):

    select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))

    if sort_by == 'az':
        select.select_by_visible_text("Name (A to Z)")
        sort_items()

    elif sort_by == 'za':
        select.select_by_visible_text("Name (Z to A)")
        sort_items(reverse = True)

    elif sort_by == 'lohi':
        select.select_by_visible_text("Price (low to high)")
        sort_items(sort_by = 'price')

    elif sort_by == 'hilo':
        select.select_by_visible_text("Price (high to low)")
        sort_items(sort_by = 'price', reverse = True)


# Add 0-indexed item to cart
def select_add_remove_button(index):
    
    pass
    


def print_inventory_items():

    for item in inventory_list:
        print (Fore.CYAN + "Item Name:          ", item[0])
        print ("Item Description:   ", item[1])
        print ("Item Price:         ", item[2])
        print ("In cart:            ", item[3])
        print ("Item Image Source:  ", item[4], '\n\n')
    print('\n\n\n' + Fore.WHITE)



def confirm_validity_of_inventory_items(valid = True):

        print(Fore.CYAN + "Beginning Confirmation of Inventory Items" + Fore.WHITE)
        current_inventory_list = []
        get_inventory_list(current_inventory_list)
        

        item_counter = 0
        for item in current_inventory_list:
            item_descriptor_counter = 0
            for val in item:
                if(val != inventory_list[item_counter][item_descriptor_counter]):
                    valid = False
                    print(Fore.RED + "Error Detected:" + Fore.WHITE + "\nExected Value: ", inventory_list[item_counter][item_descriptor_counter], "\nActual Value:  ", val, '\n')
                item_descriptor_counter += 1
            item_counter += 1


        #item_counter = 0
        #for item in current_inventory_list:
        #    if (item != inventory_list[item_counter]):
        #        valid = False
        #        print(Fore.RED + "Error Detected!" + Fore.WHITE + " Exected Value: ", inventory_list[item_counter], "\n\nActual Value: ", item, '\n')
        #    item_counter += 1


        if valid == True:
            print(Fore.GREEN + "Validity of Inventory Items Confirmed -- No Issues Detected" + Fore.WHITE)


def confirm_validity_of_cart(valid = True):

    print(Fore.CYAN + "Beginning Confirmation of Cart" + Fore.WHITE)
    
    if valid == True:
            print(Fore.GREEN + "Validity of Cart Confirmed -- No Issues Detected" + Fore.WHITE)


def confirm_validity_of_solo_item_info(valid = True):

    print(Fore.CYAN + "Beginning Confirmation of Singular Item Info" + Fore.WHITE)
    
    if valid == True:
            print(Fore.GREEN + "Validity of Singular Item Information Confirmed -- No Issues Detected" + Fore.WHITE)


# Inventory Values = Inventory, Cart, Singular
def confirm_validity_of_all_add_or_remove_buttons(valid = True, container = "Inventory"):

    print(Fore.CYAN + "Beginning Confirmation of Add/Remove Cart Button(s)" + Fore.WHITE)

    if container == "Inventory":
        buttons = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
    elif container == "Cart":
        buttons = driver.find_elements(By.XPATH, "//div[@class='cart_item']")
    elif container == "Singular":
        buttons = driver.find_element(By.TAG_NAME, "button")


    if valid == True:
            print(Fore.GREEN + "Validity of Add/Remove Items Confirmed -- No Issues Detected" + Fore.WHITE)


def confirm_validity_of_login(valid = True):

    if driver.current_url != "https://www.saucedemo.com/inventory.html":
        valid = False
        print(Fore.RED + "Error Detected!" + Fore.WHITE + " " + driver.find_element(By.TAG_NAME, "h3").text, '\n')

    if valid == True:
        print(Fore.GREEN + "Validity of Login Confirmed -- No Issues Detected" + Fore.WHITE)

    return valid


def test_case_x(valid = True):
    pass


# Use this to frame comprehensive test cases as a function of the other test cases in conjunction with each other.
def test_case_collective(user, valid = True):

    # Log in to saucedemo
    login_to_saucedemo(user = user)
    
    # If login was successful continue with testing, else exit
    if confirm_validity_of_login() == True:
        # Load in baseline data to compare against
        test_case_sort()
    

   
def test_case_sort(valid = True):

    select_sort()
    confirm_validity_of_inventory_items()

    select_sort('za')
    confirm_validity_of_inventory_items()

    select_sort('lohi')
    confirm_validity_of_inventory_items()

    select_sort('hilo')
    confirm_validity_of_inventory_items()


def test_case_3(valid = True):

    pass


def test_case_4(valid = True):

    pass






driver.get("http://www.saucedemo.com")



load_inventory_items()
#initialize()

test_case_collective(user = standard_username)
#test_case_collective(user = problem_username)
#test_case_collective(user = locked_username)





#test_case_2()

#test_case_3()

#test_case_4()





driver.close()




