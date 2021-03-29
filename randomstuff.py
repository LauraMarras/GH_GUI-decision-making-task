my_dictionary = {1: ['1', '2', '3', '4', '5', '6', '7'], 2: ['Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct'], 3: ['Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct']}

my_list = my_dictionary[1]
my_len = len(my_dictionary[1]) - 3
accuracy = my_dictionary[1][(len(my_dictionary[1]) - 3):]
print(my_list)
print(my_len)
print(accuracy)
