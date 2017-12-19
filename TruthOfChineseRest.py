#Eric Mok, Siddhant Singh, Ruotong Wang
#COMP 123 Lian Duan
# This is a Program that helps recommend Chinese restaurants in Twin Cities
# Based on user's preference.

# ------------------Import Modules---------------- #

from tkinter import *
import csv
import string
from PIL import Image, ImageTk
import tkinter as tk
from scraping import *

# ------------------Global Variables---------------- #

# User Preference Weights
priceWeight = 0
authWeight = 0
spicyWeight = 0

# GUI Global
mainWindow=None
firstChoiceWindow=None
secondChoiceWindow=None
thirdChoiceWindow=None
fourthChoiceWindow=None
resultWindow=None
run = True

# ------------------Import Raw Dataset---------------- #
# The data we collected by scraping data from Yelp! was saved in a csv file.
# So we need to import the csv file as a list of dictionary. Each restaurant is a dictionary,
# Within the dictionary, each key is one of the variables. (price, review,... etc.)

resList = []
with open('names.csv', newline='',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        resList.append({"priceRange": row['priceRange'], "review": row['review'],
                         "aggregateRating": row['aggregateRating'], "address": row['address'], "name": row['name'],
                         "telephone": row['telephone']})

# ------------------Functions: Prepare Dataset---------------- #
# After having the dataset (resList), we score each restaurant
# in aspects of Yelp!review, authenticity, spiciness and price.
# The calculation was accomplished by functions. Each aspects of scoring is normalized to a scale of 0-10

def addreview(dictList):
    """This function takes a list of dictionary(each dict is a restaurant) as input.
        The function extracts Yelp! review score of each restaurant, and return the
        new list of dictionary with each dictionary having a new key: reviewscore.
        The reviewscore is normalized to a scale of 0-10"""
    revlist = []
    for res in range(len(dictList)):
        string = dictList[res]["aggregateRating"]
        string = string.strip(" '@type': 'AggregateRating'}").strip("{'reviewCount':")
        string = string[6:len(string)]
        string = string.strip(",'ratingValue':").strip()
        string = string[0:3]
        reviewscore = float(string)
        revlist.append(reviewscore)
    for res in range(len(dictList)):
        dictList[res]["reviewscore"] = 10 * (revlist[res] - min(revlist)) / (max(revlist) - min(revlist))
    return dictList

def addauthentic(dictList):
    """This function takes a list of dictionary(each dict is a restaurant) as input.
    The function calculates the authenticity score of the restaurant, and return the
    new list of dictionary with each dictionary having a new key: authenticity.
    The authenticity is calculated as:
     frequency of 'authentic'/ total word count.
     The higher the score is the more likely the restaurant is authentic."""
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

def addprice(dictList):
    """This function takes a list of dictionary(each is a restaurant) as input.
    The function calculates the price score of the restaurant, and return the
    new list of dictionary with each dictionary having a new key: price, which
    is the score we assign to each priceRange.
    The higher the score is, the higher is the restaurant's price range"""
    for res in range(len(dictList)):
        if dictList[res]["priceRange"] == "$11-30":
            dictList[res]["price"] = 7.5
        elif dictList[res]["priceRange"] == "Under $10":
            dictList[res]["price"] = 5
        else:
            dictList[res]["price"] = 10
    return dictList

def addspicy(dictList):
    """This function takes a list of dictionary(each is a restaurant) as input.
    The function calculates the spiciness score of the restaurant, and return the
    new list of dictionary with each dictionary having a new key: spiciness.
    The authenticity is calculated as:
     frequency of 'spiciness'/ total word count.
     The higher the score is, the spicier the dishes in the restaurant are. """
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

# ------------------Functions: Recommending Algorithm---------------- #

def score(dictList):
    """This functions takes the full list of restaurant and user's preference,
    and calculate scores for each restaurant based on user's indicated preference.
    Final score = authWeight * authScore
                +priceWeight * priceScore
                +SpicyWeight * spicyScore
                +10 * reviewScore
    The function returns a list of dictionary with each restaurant has score saved as a key:score.
    """
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
    based on user's preference. The function returns the restaurant with the hightest score.
    A list containing the name, address and telephone of the restaurant will be returned"""
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

# ------------------Functions: Main GUIs---------------- #
def TitlePage():
    """Takes no input. Create a title page."""
    global mainWindow

    # create window
    mainWindow = Tk()
    mainWindow.title("Truth of Chinese Restaurants")
    mainWindow.config(bg="black")

    # add image to the title page
    image = Image.open('chinfood.jpg')
    photo_image = ImageTk.PhotoImage(image)
    photoLabel = tk.Label(mainWindow, image=photo_image)
    photoLabel.grid(row=2, column=0)

    # add welcome message to the title page
    label1 = Label(
        text="\n\n\n\tWelcome! We recommend good Chinese restaurants in the Twin Cities. For this is -\t\n THE TRUTH OF CHINESE RESTAURANTS\n\n\n\n\n",
        font="Garamond 16 bold", bg="black", fg="white")
    label1.grid(row=0, column=0)

    # add button "next" to the title page.
    # The next button will take user to the next page where user can answer the first question .
    button1 = Button(mainWindow)
    button1["text"] = "Next"
    button1["font"] = "Garamond 14 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = exitMainScreen
    button1.grid(row=1, column=0)

    # adds button "Update Database" to the title page.
    # The button updates the file names.csv by doing the webscraping of some select Chinese restaurants from yelp.com
    button2 = Button(mainWindow)
    button2["text"] = "Update Database"
    button2["font"] = "Garamond 14 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = updateDatabase
    button2.grid(row=1, column=1)
    mainWindow.mainloop()


def firstChoice():
    """Takes no input.
    The function creates a page where user can indicate their preference on authenticity"""
    global firstChoiceWindow

    # create window
    firstChoiceWindow = Tk()
    firstChoiceWindow.minsize(width=1100, height=250)
    firstChoiceWindow.maxsize(width=1000, height=250)
    firstChoiceWindow.title("Authenticity")
    firstChoiceWindow.config(bg="black")

    # add question prompt to the page
    label1 = Label(
        text="How much do you care for authenticity of the food?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)

    # add three choice buttons to the page
    button1 = Button(firstChoiceWindow)
    button1["text"] = "I want good, authentic food!"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = authentic1
    button1.grid(row=1, column=0)

    button2 = Button(firstChoiceWindow)
    button2["text"] = "The food should be authentic enough but other things matter more!"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = authentic2
    button2.grid(row=1, column=1)

    button3 = Button(firstChoiceWindow)
    button3["text"] = "You could serve me Italian for all I know. Other things matter more!"
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = authentic3
    button3.grid(row=1, column=2)

    firstChoiceWindow.mainloop()

def secondChoice():
    """Takes no input.
        The function creates a page where user can indicate their preference on price"""
    global secondChoiceWindow

    # create window
    secondChoiceWindow = Tk()
    secondChoiceWindow.minsize(width=1100, height=250)
    secondChoiceWindow.maxsize(width=1000, height=250)
    secondChoiceWindow.title("Price")
    secondChoiceWindow.config(bg="black")

    # add question prompt to the page
    label1 = Label(
        text="How much do you care for price?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)

    # add three choice buttons to the page
    button1 = Button(secondChoiceWindow)
    button1["text"] = "I want the cheapest food"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = price1
    button1.grid(row=1, column=0)

    button2 = Button(secondChoiceWindow)
    button2["text"] = "I am not Uncle Scrooge but I don't mind paying a little extra for better quality food"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = price2
    button2.grid(row=1, column=1)

    button3 = Button(secondChoiceWindow)
    button3["text"] = "Price does not matter at all to me."
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = price3
    button3.grid(row=1, column=2)

    secondChoiceWindow.mainloop()

def thirdChoice():
    """Takes no input.
            The function creates a page where user can indicate their preference on spiciness"""
    global thirdChoiceWindow

    # create window
    thirdChoiceWindow = Tk()
    thirdChoiceWindow.title("Spicy")
    thirdChoiceWindow.config(bg="black")

    # add question prompt to the page
    label1 = Label(
        text="How spicy do you want the food to be?",
        font="Garamond 11 bold", bg="black", fg="white")
    label1.grid(row=0, column=1)

    # add three choice buttons to the page
    button1 = Button(thirdChoiceWindow)
    button1["text"] = "I don't like spicy food"
    button1["font"] = "Garamond 11 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = spice1
    button1.grid(row=1, column=0)

    button2 = Button(thirdChoiceWindow)
    button2["text"] = "Mildly spicy"
    button2["font"] = "Garamond 11 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = spice2
    button2.grid(row=1, column=1)

    button3 = Button(thirdChoiceWindow)
    button3["text"] = "Bring it on"
    button3["font"] = "Garamond 11 bold"
    button3["bg"] = "white"
    button3["fg"] = "black"
    button3["command"] = spice3
    button3.grid(row=1, column=2)

    secondChoiceWindow.mainloop()

def result():
    """Takes no input.
                The function creates a result page where users get the recommendation for restaurant"""
    global dictMain
    global resultWindow

    # calculate the result
    finalDictList=score(dictMain)
    resultList=topn(finalDictList)

    # create window
    resultWindow = Tk()
    resultWindow.title("The restaurant you want")
    resultWindow.config(bg="black")

    # add image to the page
    image = Image.open('noodle.jpg')
    photo_image = ImageTk.PhotoImage(image)
    photoLabel = tk.Label(resultWindow, image=photo_image)
    photoLabel.grid(row=4, column=0)

    # add prompt message to the page
    label1 = Label(
        text="\n\n\n\tThe restaurant you want is -\t\n",
        font="Garamond 16 bold", bg="black", fg="white")
    label1.grid(row=0, column=0)

    # add name of the result restaurant to the page
    labelName = Label(
        text=resultList[0],
        font="Garamond 12 bold", bg="black", fg="white")
    labelName.grid(row=1, column=0)

    # add address of the result restaurant to the page
    labelAddress = Label(
        text=resultList[1].strip("{").strip("}"),
        font="Garamond 12 bold", bg="black", fg="white")
    labelAddress.grid(row=2, column=0)

    # add telephone of the result restaurant to the page
    labelTelephone = Label(
        text="Telephone:"+resultList[2],
        font="Garamond 12 bold", bg="black", fg="white")
    labelTelephone.grid(row=3, column=0)

    # add button 'Go Again' to the page
    button1 = Button(resultWindow)
    button1["text"] = "Go again"
    button1["font"] = "Garamond 14 bold"
    button1["bg"] = "white"
    button1["fg"] = "black"
    button1["command"] = goAgain
    button1.grid(row=5, column=0)

    # add button 'Quit' to the page
    button2 = Button(resultWindow)
    button2["text"] = "Quit"
    button2["font"] = "Garamond 14 bold"
    button2["bg"] = "white"
    button2["fg"] = "black"
    button2["command"] = exitResultScreen
    button2.grid(row=5, column=1)
    resultWindow.mainloop()

def exitMainScreen():
    """Takes no input. Brings the user to the first choice page.
    Triggered by 'Next' button on the title page."""
    mainWindow.destroy()
    firstChoice()

def updateDatabase():
    """Takes no input. This functions scrapes yelp.com (need to package beautifulsoup4 installed) and creates a file
    names.csv which stores the data we need. """
    global mainWindow
    restCompile()
    scraping()
    scrapeLabel=Label(mainWindow,text="Database updated!",bg="white",fg="black")
    scrapeLabel.grid(row=0,column=1)

def exitResultScreen():
    """Takes no input. Exit the program.
    Triggered by 'Quit' Button on the result page."""
    resultWindow.destroy()

def goAgain():
    """Takes no input. Bring the user to the title page.
    Triggered by 'Go Again' Button on the result page"""
    resultWindow.destroy()
    TitlePage()

# ------------------Functions: GUIs Buttons taking user's preference---------------- #
def authentic1():
    """Takes no input.
    If the user choose 'I want good, authentic food!', the function assign
     weight of authenticity as 10.
     The function also bring user to the next page."""
    global authWeight
    authWeight=10
    firstChoiceWindow.destroy()
    secondChoice()

def authentic2():
    """Takes no input.
        If the user choose 'The food should be authentic enough but other things matter more!',
        the function assign weight of authenticity as 5.
        The function also bring user to the next page."""
    global authWeight
    authWeight=5
    firstChoiceWindow.destroy()
    secondChoice()

def authentic3():
    """Takes no input.
            If the user choose 'You could serve me Italian for all I know. Other things matter more!',
            the function assign weight of authenticity as -10. So the higher the authentic score is
            for the restaurant, the lower the final score for the restaurant is.
    The function also bring user to the next page."""
    global authWeight
    authWeight=-10
    firstChoiceWindow.destroy()
    secondChoice()

def price1():
    """Takes no input.
               If the user choose 'I want the cheapest food',
               the function assign weight of price as -10. So the higher the price score is
               for the restaurant, the lower the final score for the restaurant is.
        The function also bring user to the next page."""
    global priceWeight
    priceWeight = -10
    secondChoiceWindow.destroy()
    thirdChoice()

def price2():
    """Takes no input.
                  If the user choose 'I am not Uncle Scrooge but
                  I don't mind paying a little extra for better quality food',
                  the function assign weight of price as -5.
        The function also bring user to the next page."""
    global priceWeight
    priceWeight = -5
    secondChoiceWindow.destroy()
    thirdChoice()

def price3():
    """Takes no input.
                      If the user choose 'Price does not matter at all to me',
                      the function assign weight of price as 10.
        The function also bring user to the next page."""
    global priceWeight
    priceWeight = 10
    secondChoiceWindow.destroy()
    thirdChoice()

def spice1():
    """Takes no input.
                If the user choose 'I don't like spicy food',
                the function assign weight of price as -10. So the spicier the food in the
                 restaurant is, the lower the socre is for the restaurant.
        The function also bring user to the next page."""
    global spicyWeight
    spicyWeight=-10
    thirdChoiceWindow.destroy()
    result()

def spice2():
    """Takes no input.
                    If the user choose 'Mildly Spicy',
                    the function assign weight of price as -1.
        The function also bring user to the next page."""
    global spicyWeight
    spicyWeight=1
    thirdChoiceWindow.destroy()
    result()

def spice3():
    """Takes no input.
                If the user choose 'Bring it On',
                the function assign weight of price as 10.
        The function also bring user to the next page."""
    global spicyWeight
    spicyWeight=10
    thirdChoiceWindow.destroy()
    result()

# ------------------Process Dataset---------------- #
# After processed by the four functions, the dataset includes
# authenticity score, price score, spicy score and review score.

dictMain = addreview(addspicy(addauthentic(addprice(resList))))

# ------------------Script Element---------------- #
if __name__ == '__main__':
    TitlePage()