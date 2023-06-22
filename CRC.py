import copy
import random as rand
from random import *


# function that performs XOR method
def xor(a, b):
    # initialize result
    result = []

    # Traverse all bits, if bits are
    # same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def modulo2(Divident, Divisor):
    # Number of bits to be XORed at a time.
    pick = len(Divisor)

    # Slicing the divident to appropriate
    # length for particular step
    temp = Divident[0: pick]

    while pick < len(Divident):
        if temp[0] == '1':
            # replace the divident by the result
            # of XOR and pull 1 bit down
            temp = xor(Divisor, temp) + Divident[pick]
        else:
            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor
            temp = xor('0' * pick, temp) + Divident[pick]
        pick += 1

    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds
    if temp[0] == '1':
        temp = xor(Divisor, temp)
    else:
        temp = xor('0' * pick, temp)

    return temp


# Function used at the sender side to encode
# data by appending remainder of modular division
# at the end of data.
def setData(data, key):
    appended_data = data + '0' * (len(key) - 1)

    remainder = modulo2(appended_data, key)

    codeword = data + remainder

    return codeword


# function that generates random D sequence
def MessageGenerator(number_of_bits):
    list_integers = []
    converter = []
    # Generating random numbers (0 or 1)
    for i in range(number_of_bits):
        list_integers.append(randint(0, 1))
    # Converting int to chars, then return the list as string
    for i in range(number_of_bits):
        converter.append(str(list_integers[i]))

    return ''.join(converter)


# function that generates the altered message using the bit error rate
def MessageWithNoise(Message, bit_error):
    message_with_noise = copy.deepcopy(Message)
    flag = False
    for i in range(len(message_with_noise)):
        # choosing random number between 0 and 1 (float numbers only)
        random_number = rand.uniform(0, 1)
        # if the generated number is smaller than the bit error, we alter the i_th bit
        # of the message
        if random_number < bit_error:
            flag = True
            if message_with_noise[i] == '1':
                message_with_noise = message_with_noise[:i] + '0' + message_with_noise[i + 1:]
            else:
                message_with_noise = message_with_noise[:i] + '1' + message_with_noise[i + 1:]
    return message_with_noise, flag


# Function to check the string has
# all same characters(zeros) or not .
def allCharactersZero(s):
    n = len(s)
    for i in range(n):
        if s[i] != '0':
            return False

    return True


# Main program
k = 20  # number of bits in D sequence
messages = 100 # number of transmitted messages
D = []  # list of D parameters
T = []  # list of T parameters
P = input("Enter bits of P parameter(0 or 1 bits only accepted): ")
BER = float(input("Enter bit error(floating number between (0,1)): "))
count_true = 0 # variable that counts how many messages have been altered due to bit error rate
count_spotted_by_crc = 0
# Generating D parameters and put them in List
for i in range(messages):
    D.append(MessageGenerator(k))
# Generating T parameters(D message + CRC)
for i in range(messages):
    T.append(setData(D[i], P))
for i in range(messages):
    T_with_noise, flag = MessageWithNoise(T[i], BER)
    if flag:
        # message has been altered
        count_true += 1
        remainder = modulo2(T_with_noise, P)
        if not allCharactersZero(remainder):
            count_spotted_by_crc += 1

print("Number of transmitted messages: ", messages)
print("Number of Messages with errors(using the bit error rate): ", count_true, " out of ", messages,
      "\n Percentage-> ",(count_true / messages) * 100, "%")
print("\nNumber of Messages with errors spotted by the crc: ", count_spotted_by_crc, " out of ", count_true,
      "\n Percentage-> ",(count_spotted_by_crc / count_true) * 100, "%")
print("\nNumber of Messages with errors not spotted by the crc: ", count_true - count_spotted_by_crc,
      " out of ", count_true,
      "\n Percentage-> ", ((count_true - count_spotted_by_crc) / messages) * 100,"%")