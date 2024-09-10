import os
import csv

import matplotlib.pyplot as plt

from ast import literal_eval

dataFile = os.path.join("data", "authorsFileTouches_file_rootbeer.csv")

# Read the data into a list using literal_eval

commitData = []

with open(dataFile) as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        try:
            commitData.append([row["Filename"], literal_eval(row["Touches"])])
        except:
            print("Error when parsing filename " + row["Filename"])

# Give each author their own color

authorColors = dict()

colorItems = [
    "aqua", "darkcyan", "indigo", "blue", "blueviolet",
    "brown", "coral", "crimson", "gray", "darkgreen",
    "darkorange", "gold", "lightpink", "lime", "olive",
    "lightslategray", "lightsteelblue", "peru", "royalblue", "pink",
    "tan", "teal", "tomato", "violet", "yellow",
    "darkorchid", "darkred", "darksalmon", "deeppink", "darkslateblue",
    "goldenrod", "khaki", "lightseagreen", "mediumblue", "mediumaquamarine",
    "mediumseagreen", "mediumslateblue", "mediumvioletred", "midnightblue", "navajowhite",
    "olivedrab", "orangered", "orchid", "purple", "saddlebrown",
    "salmon", "sienna", "seagreen", "skyblue", "silver"
]

# Counts the total amount of authors
authorCounter = 0

# Counts how many commits each author makes
authorCommitCounter = dict()

for row in commitData:
    for individualCommit in row[1]:
        # Increment author commit counter
        authorCommitCounter[individualCommit[0]] = authorCommitCounter.get(individualCommit[0], 0) + 1

        # Give the author a color if they don't have a color
        if individualCommit[0] not in authorColors:
            if authorCounter >= len(colorItems):
                authorColors[individualCommit[0]] = "black"
                print(individualCommit[0], "was assigned 'black' by default. More colors are needed.")
            else:
                authorColors[individualCommit[0]] = colorItems[authorCounter]

            authorCounter += 1

del colorItems

# Translate dates into weeks

def date_to_weeks(date: str) -> float:
    
    # Extract years

    delimitIndex = date.find('-')
    
    if delimitIndex == -1:
        return -1
    
    # Convert years to days and subtract a constant
    output = 365 * (float(date[:delimitIndex]) - 1950)

    date = date[delimitIndex+1:]

    # Extract months

    delimitIndex = date.find('-')

    if delimitIndex == -1:
        return -2

    output += float(date[:delimitIndex]) * 30.5

    date = date[delimitIndex+1:]

    # Extract days

    delimitIndex = date.find('T')

    if delimitIndex == -1:
        return -3
    
    output += float(date[:delimitIndex])

    return output / 7.0

# Get the earliest week to subtract from other dates

earliestWeek = date_to_weeks(commitData[len(commitData) - 1][1][0][1]) # Initialize the earliest week with the first found date

for file in commitData:
    for commit in file[1]:
        thisWeek = date_to_weeks(commit[1])

        if thisWeek < earliestWeek:
            earliestWeek = thisWeek

# Sort the data based on commit number
# This probably isnt needed, so it uses bubble sort
# Leave swap as false to skip this step

swap = False

while(swap):
    swap = False

    for i in range(0, len(commitData) - 2):
        if len(commitData[i][1]) < len(commitData[i + 1][1]):
            
            temp = commitData[i + 1]
            commitData[i + 1] = commitData[i]
            commitData[i] = temp

            swap = True

# Output a key for the graph into the console

# Print some data about the authors

print(f"Total Author Count: {authorCounter}\n")

authorCommitCounterList = [*authorCommitCounter.items()]

# Bubble sort to organize authors based on commit amount

swap = True

while(swap):
    swap = False
    for index in range(0, len(authorCommitCounterList) - 2):
        if authorCommitCounterList[index][1] < authorCommitCounterList[index + 1][1]:
            temp = authorCommitCounterList[index]
            authorCommitCounterList[index] = authorCommitCounterList[index + 1]
            authorCommitCounterList[index + 1] = temp
            swap = True

for author in authorCommitCounterList:
    print(f"Author: {author[0]}\nColor: {authorColors[author[0]]}\nCommits: {author[1]}\n")

# Plot all of the data

x = []
y = []
colors = []

for index, file in enumerate(commitData):
    for commit in file[1]:
        
        # Adds the file index to the x list
        x.append(index)

        # Adds the date difference to the y list
        y.append(date_to_weeks(commit[1]) - earliestWeek)

        # Adds the color to the c list
        colors.append(authorColors[commit[0]])

plt.scatter(x, y, c=colors, s=25)

plt.xlabel("File")
plt.ylabel("Week")

plt.show()



