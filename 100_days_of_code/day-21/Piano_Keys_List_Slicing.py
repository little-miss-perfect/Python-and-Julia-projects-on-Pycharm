piano_keys = ["a", "b", "c", "d", "e", "f", "g"]
piano_tuple = ("do", "re", "mi", "fa", "so", "la", "ti")

print(piano_keys[2:5])
print(piano_keys[2:])
print(piano_keys[:5])

print(piano_keys[:])

print(piano_keys[2:5:2])

print(piano_keys[::2])  # it now goes from the beginning to the end... but skips to every second element
print(piano_keys[::-1])  # nice... now it gets every element... but it puts it in reverse (going back by one)!

# what about for tuples?

print(piano_tuple[:])
print(piano_tuple[2:5])


