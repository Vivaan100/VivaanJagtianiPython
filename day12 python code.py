# This file was created by: Vivaan Jagtiani


'''
First, we get two pieces of bread.
We then take out a pan and put it over a stove. 
Wait until the pan gets warm enough. 
When the pan is warm enough, put a piece of butter in the pan. 
While the butter melts, get two slices of bread and put two slices of cheese in between. 
Afer that, you would put the sandwich in the pan, and wait for three minutes, and then flip,
and then wait another three minutes. 
When you are done, get a plate out and put the sandwich on it. 
Take a sharp knife and cut diagnolly.
And then...............cheese pull.
'''
#n = 1
#for n in range(20):
    #print((n), "people")
    #if n == 14: break
    #print()




# counting by twos
# Odd number of occupants
# Assumptions - know the number of people in the room
#N = 0
#people_in_room = 3

# loop that counts by two until N is equal to the number of people in the room
#while N < people_in_room:
    #N+=2
    # the difference is one (meaning odd) then add one at a time...
    #if people_in_room - N ==1:
        #N+=1
    #print(N)


level1 = ["hello",
          "world",
          "thing",
          "pasta"]

for row in level1: 
    print(row)
    for col in row:
        print(col)

enum_level = enumerate(level1)

for i in enum_level: 
    print(i)