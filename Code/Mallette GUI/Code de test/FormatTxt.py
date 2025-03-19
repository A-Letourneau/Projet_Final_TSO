# Open the file in read mode
goodText = []
with open('badFormat.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Print each line
        goodText.append(line[5:])
with open('goodFormat.txt', 'a') as file:
    for line in goodText:
        file.write(line)

    
