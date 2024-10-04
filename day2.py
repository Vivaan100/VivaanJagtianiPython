# Create code that randomly selects names from your table
#https://www.w3schools.com/python/python_lists.asp
# https://www.w3schools.com/python/python_lists.asp
# libraries are imported using the import keyword
# we import libraries to use their functions and methods
import random

# Lists are used to store multiple items in a single variable
mylist = ["Rohan", "Vivaan","Riley", "Sol"]

person = random.choice(mylist)
print(person)
