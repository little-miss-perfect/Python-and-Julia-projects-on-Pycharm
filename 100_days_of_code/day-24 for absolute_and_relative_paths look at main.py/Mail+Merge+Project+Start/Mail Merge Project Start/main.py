# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".
#
# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
#     Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
#         Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

PLACEHOLDER = "[name]"  # it's a placeholder that's written in the format we want our outcome letters to have
 #create a list of the names needed:
with open("./Input/Names/invited_names.txt") as names_file:  # 'in the current working directory of "main.py" (which is "Mail Merge Project Start")' is equivalent to writing './'
    names = names_file.readlines()  # a list
    print(names)

# create/write the letters:
with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    for name in names:  # we're iterating over the Python "list" of names we defined above
        stripped_name = name.strip()  # so... this actually removes spaces and "\n"? I think it does...
        new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)  # we do this for each new letter
        # print(new_letter)
        with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", mode="w") as completed_letter:  # the "w" ("write") mode only replaces whatever was in the original files. but since they didn't exist, then we'd be creating them, and they would start blank and then have this "new_letter" text added. nice.
            completed_letter.write(new_letter)
