from tkinter import *
import csv
import string


# ------------------Global Variable---------------- #

# Final score = ax1+bx2+cx3+review
priceWeight = 0
authWeight = 0
spicyWeight = 0


# ------------------Import Raw Dataset---------------- #
# The data we collected by scraping data from Yelp! was saved in a csv file.
# We import the csv file as a list of dictionary. Each restaurant is a dictionary,
# Within the dictionary, each key is one of the variables.
# The dataset includes information for 29 restaurants;
# Each restaurant, priceRange, review, aggregatedRating, address, name and telephone are included.

resList = []
with open('names.csv', newline='',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        resList.append({"priceRange": row['priceRange'], "review": row['review'],
                         "aggregateRating": row['aggregateRating'], "address": row['address'], "name": row['name'],
                         "telephone": row['telephone']})


# ------------------Functions: Prepare Dataset---------------- #
# After having the dataset (resList), we will calculate scores for each restaurant.
# The calculation was accomplished by functions. Each aspects of scoring is normalized to a scale of 0-10
def addreview(dictList):
    revlist = []
    for res in range(len(dictList)):
        string = dictList[res]["aggregateRating"]
        string = string.strip(" '@type': 'AggregateRating'}").strip("{'reviewCount':")
        string = string[6:len(string)]
        string = string.strip(",'ratingValue':").strip()
        reviewscore = float(string)
        revlist.append(reviewscore)
    for res in range(len(dictList)):
        dictList[res]["reviewscore"] = 10 * (revlist[res] - min(revlist)) / (max(revlist) - min(revlist))
    return dictList

def addauthentic(dictList):
    """This function takes a list of dictionary(each is a restaurant) as input.
    The function calculates the authenticity score of the restaurant, and return the
    new list of dictionary with each dictionary having a new key: authenticity.
    The authenticity is calculated as:
     frequency of 'authentic'/ total word count. """
    authlist = []
    for res in range(len(dictList)):
        auth = 0
        cleanStr = (dictList[res]["review"])
        wordList = cleanStr.lower().strip(string.punctuation).split(" ")
        authentic = ["authentic", "authenticity", "real", "original", "genuine", "true"]
        for j in range(len(wordList)):
            if wordList[j] in authentic:
                auth = auth + 1
        authlist.append(auth/len(wordList))
    for res in range(len(dictList)):
        dictList[res]["authenticity"] = 10*(authlist[res] - min(authlist))/(max(authlist)-min(authlist))
    return dictList

def addspicy(dictList):
    """This function takes a list of dictionary(each is a restaurant) as input.
    The function calculates the spiciness score of the restaurant, and return the
    new list of dictionary with each dictionary having a new key: spiciness.
    The authenticity is calculated as:
     frequency of 'spiciness'/ total word count. """
    spylist = []
    for res in range(len(dictList)):
        spy = 0
        cleanStr = (dictList[res]["review"])
        wordList = cleanStr.lower().strip(string.punctuation).split(" ")
        spiciness = ["spiciness", "spicy", "hot", "hotness", "pepper", "fiery"]
        for j in range(len(wordList)):
            if wordList[j] in spiciness:
                spy = spy + 1
        spylist.append(spy/len(wordList))
    for res in range(len(dictList)):
        dictList[res]["spiciness"] = 10*(spylist[res] - min(spylist))/(max(spylist)-min(spylist))
    return dictList


def addprice(dictList):
    """This function converts the price into a varaible that has integer values.It returns a newlist"""
    for res in range(len(dictList)):
        if dictList[res]["priceRange"] == "$11-30":
            dictList[res]["price"] = 7.5
        elif dictList[res]["priceRange"] == "Under $10":
            dictList[res]["price"] = 5
        else:
            dictList[res]["price"] = 10
    return dictList

#
# dictionary=addspicy(addprice(addauthentic(resList)))
# print(dictionary[0].keys())

dictMain = addreview(addspicy(addauthentic(addprice(resList))))

# ------------------Functions: GUI---------------- #

mainWindow=None
firstChoiceWindow=None
secondChoiceWindow=None
thirdChoiceWindow=None
fourthChoiceWindow=None
resultWindow=None
run = True
def TitlePage():
    global mainWindow
    mainWindow = Tk()
    mainWindow.title("Truth of Asian Restaurants")
    mainWindow.config(bg="black")
    label1 = Label(
        text="\n\n\n\tWelcome! If good Chinese restaurants is what you were looking for, then you have come to the right place. For this is -\t\n THE TRUTH OF ASIAN RESTAURANTS\n\n\n\n\n",
        font="Garamond 16 bold", bg="black", fg="white")
    label1.grid(row=0, column=0)
    button1 = Button(mainWindow)
    button1["text"] = "Next"
    button1["font"] = "Garamond 14 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = exitMainScreen
    button1.grid(row=1, column=0)
    mainWindow.mainloop()

    # at this point I want to change frames


def firstChoice():
    global firstChoiceWindow
    firstChoiceWindow = Tk()
    firstChoiceWindow.minsize(width=1100, height=250)
    firstChoiceWindow.maxsize(width=1000, height=250)
    firstChoiceWindow.title("Authenticity")
    firstChoiceWindow.config(bg="black")
    label1 = Label(
        text="How much do you care for authenticity of the food?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)
    button1 = Button(firstChoiceWindow)
    button1["text"] = "I want good, authentic food!"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = authentic1  # change
    button1.grid(row=1, column=0)
    button2 = Button(firstChoiceWindow)
    button2["text"] = "The food should be authentic enough but other things matter more!"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = authentic2  # change
    button2.grid(row=1, column=1)
    button3 = Button(firstChoiceWindow)
    button3["text"] = "You could serve me Italian for all I know. Other things matter more!"
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = authentic3  # change
    button3.grid(row=1, column=2)
    firstChoiceWindow.mainloop()


def secondChoice():
    global secondChoiceWindow
    secondChoiceWindow = Tk()
    secondChoiceWindow.minsize(width=1100, height=250)
    secondChoiceWindow.maxsize(width=1000, height=250)
    secondChoiceWindow.title("Truth of Asian Restaurants")
    secondChoiceWindow.config(bg="black")
    label1 = Label(
        text="How much do you care for price?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)
    button1 = Button(secondChoiceWindow)
    button1["text"] = "I want the cheapest food"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = price1  # change
    button1.grid(row=1, column=0)
    button2 = Button(secondChoiceWindow)
    button2["text"] = "I am not Uncle Scrooge but I don't mind paying a little extra for better quality food"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = price2  # change
    button2.grid(row=1, column=1)
    button3 = Button(secondChoiceWindow)
    button3["text"] = "Price does not matter at all to me."
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = price3  # change
    button3.grid(row=1, column=2)
    secondChoiceWindow.mainloop()

def thirdChoice():
    global thirdChoiceWindow
    thirdChoiceWindow = Tk()
    thirdChoiceWindow.title("Truth of Asian Restaurants")
    thirdChoiceWindow.config(bg="black")
    label1 = Label(
        text="How spicy do you want the food to be?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)
    button1 = Button(thirdChoiceWindow)
    button1["text"] = "I don't like spicy food"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = spice1  # change
    button1.grid(row=1, column=0)
    button2 = Button(thirdChoiceWindow)
    button2["text"] = "Mildly spicy"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = spice2  # change
    button2.grid(row=1, column=1)
    button3 = Button(thirdChoiceWindow)
    button3["text"] = "Bring it on"
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = spice3  # change
    button3.grid(row=1, column=2)
    secondChoiceWindow.mainloop()

# ------------------Functions: Recommending---------------- #
def score(dictList):
    """This functions takes the full list of restaurant and user's preference,
    and give scores to restaurants based on user's preference. """
    global spicyWeight
    global priceWeight
    global authWeight
    for res in range(len(dictList)):
        authenticity = authWeight * dictList[res]["authenticity"]
        spiciness = spicyWeight * dictList[res]["spiciness"]
        price = priceWeight* dictList[res]["price"]
        reviewscore = 10*dictList[res]["reviewscore"]
        score = authenticity + price + spiciness + reviewscore
        dictList[res]["score"] = int(score)
    return dictList

def topn(dictList):
    """This function takes in the list of restaurant with each restaurant scored
    based on user's preference. We then return the single restaurant with the highest score."""
    highscore = dictList[0]["score"]
    name = ""
    for res in range(len(dictList)):
        if dictList[res]["score"] > highscore:
            highscore = dictList[res]["score"]
            name = dictList[res]["name"]
            address = dictList[res]["address"]
            telephone = dictList[res]["telephone"]
    userList=[name,address,telephone]
    return userList

def result():
    global dictMain
    global resultWindow
    finalDictList=score(dictMain)
    resultList=topn(finalDictList)
    resultWindow = Tk()
    resultWindow.title("Truth of Asian Restaurants")
    resultWindow.config(bg="black")
    label1 = Label(
        text="\n\n\n\tThe restaurant you want is -\t\n",
        font="Garamond 16 bold", bg="black", fg="white")
    label1.grid(row=0, column=0)
    labelName = Label(
        text=resultList[0],
        font="Garamond 12 bold", bg="black", fg="white")
    labelName.grid(row=1, column=0)
    labelAddress = Label(
        text=resultList[1].strip("{").strip("}"),
        font="Garamond 12 bold", bg="black", fg="white")
    labelAddress.grid(row=2, column=0)
    labelTelephone = Label(
        text="Telephone:"+resultList[2],
        font="Garamond 12 bold", bg="black", fg="white")
    labelTelephone.grid(row=3, column=0)
    button1 = Button(resultWindow)
    button1["text"] = "Go again"
    button1["font"] = "Garamond 14 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = goAgain
    button1.grid(row=5, column=0)
    button2 = Button(resultWindow)
    button2["text"] = "Quit"
    button2["font"] = "Garamond 14 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = exitResultScreen
    button2.grid(row=5, column=1)
    resultWindow.mainloop()

def exitMainScreen():
    mainWindow.destroy()
    firstChoice()



def exitResultScreen():
    resultWindow.destroy()

def authentic1():
    #this is where we call scoring function 1
    global authWeight
    authWeight=10
    firstChoiceWindow.destroy()
    secondChoice()

def authentic2():
    #this is where we call scoring function 2
    global authWeight
    authWeight=5
    firstChoiceWindow.destroy()
    secondChoice()
def authentic3():
    #this is where we call scoring function 3
    global authWeight
    authWeight=-10
    firstChoiceWindow.destroy()
    secondChoice()
def price1():
    #this is where we call scoring function 1
    global priceWeight
    priceWeight = -10
    secondChoiceWindow.destroy()
    thirdChoice()

def price2():
    #this is where we call scoring function 2
    global priceWeight
    priceWeight = -5
    secondChoiceWindow.destroy()
    thirdChoice()
def price3():
    #this is where we call scoring function 3
    global priceWeight
    priceWeight = 10
    secondChoiceWindow.destroy()
    thirdChoice()
def spice1():
    #this is where we call scoring function 1
    global spicyWeight
    spicyWeight=-10
    thirdChoiceWindow.destroy()
    result()
def spice2():
    #this is where we call scoring function 2
    global spicyWeight
    spicyWeight=1
    thirdChoiceWindow.destroy()
    result()
def spice3():
    #this is where we call scoring function 3
    global spicyWeight
    spicyWeight=10
    thirdChoiceWindow.destroy()
    result()
def goAgain():
    resultWindow.destroy()
    TitlePage()
TitlePage()


for res in range(len(dictMain)):
    print(dictMain[res]["spiciness"], "\t", dictMain[res]["name"],"\t", dictMain[res]["score"])