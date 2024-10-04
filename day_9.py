# This file was created by: Vivaan Jagtiani

# This piece of code is a while loop
Bueller = 0
while Bueller < 10:
  print("Bueller")
  if Bueller == 10:
    break
  Bueller += 1

# This piece of code is a for loop

for x in range(5): 
  print("anyone")
  if x == 5: break
  print()


list = {"Riley", "Sol", "Vivaan"}

import random 

randomperson = (random.choice(list))

#creating the function with random choice
def nameoflists():
  print((randomperson))

nameoflists()

def myFunc(name): 
  name = input ("give me yo name")
  print(greeting+name)

  askingforname = True
  if askingforname: 
    myFunc("Hello there...")
