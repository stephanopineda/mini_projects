#
#   This program would slice the string into  
#   the starting character configured in the  
#   variable 'word' without using RegEx
#

# # The string to be searched at
# sentence = "Michael Jackson was a singer and known as the 'King of Pop'"

# # The word to search for
# word = "i"

# # Temporary variables
# log_index = []
# count = 0

# for slice_index in range(len(sentence)):
#     if word in sentence[slice_index : slice_index + len(word)]:
#         log_index.append(slice_index)
#         count += 1

# for index in range(len(log_index)):
#     if index != len(log_index) - 1:
#         print(sentence[log_index[index]:log_index[index + 1]])
#     else:
#         print(sentence[log_index[index]:])

# ------------ ChatGPT ------------------
# The string to be searched in
sentence = "Michael Jackson was as singer and known as the 'King of Pop'"

# The word to search for
word = "as"

# Variables to store indices and results
start = 0
log_index = []

# Find all occurrences of the word
while True:
    print(log_index)
    start = sentence.find(word, start)
    if start == -1:  # No more occurrences
        break
    log_index.append(start)
    start += len(word)  # Move past the current match

# Print slices between occurrences
for i, index in enumerate(log_index):
    if i != len(log_index) - 1:
        print(sentence[index:log_index[i + 1]])
    else:
        print(sentence[index:])

print(sentence.find("a", 5))


