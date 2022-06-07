import random 

lower_case = 'abcdefghijklmnopqrstuvwxyz'
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
number = '1234567890'
symbol = '!@#$%^&*.?'

use_for = lower_case + upper_case + number + symbol
length = 8

password = "".join(random.sample(use_for, length))

print (password)