# This file was created by: Vivaan Jagtiani(Copied from Mr. Cozort)

import random

# write a function that selects a name randomly from user input via an append list
def random_name_picker(message):
    # Using global to make mylist available outside the scope of the function
    # Global shuold be used any time you want to define a variable inside a function
    # That variable only becomes available when the function is available
    global mylist
    mylist[]
    # getting user input in the terminal
    x = input(message)
    # appending the empty list with values
    mylist.append(x)
    y = input(message)
    mylist.append(y)
    z = input(message)
    mylist.append(z)
    r = random.choice(mylist)
    ## returning is the last thig a function does
    return r

    # random_name_picker
    print(mylist)

    print(random_name_picker("give me the rizzliest bunch of names you can think of..."))
    print(mylist)
