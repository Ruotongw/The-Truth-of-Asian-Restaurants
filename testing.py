# Eric Mok, Siddhant Singh, Ruotong Wang
# COMP 123 Lian Duan
# This is a Program that test functions in the program Comp 123 Project.

# ========================================================================
# Set Up the Environment
from TruthOfChineseRest import *
import csv

global spicyWeight
global priceWeight
global authWeight

# ========================================================================
# Main tester function.
def doTest():
    """"""
    testadddreview()
    testadddauthentic()
    testaddspicy()
    testaddprice()
    testscore()
    testtopn()
    print("\nTests are over.")

# import dataset

# ========================================================================
# Test for addreview.
def testadddreview():
    """This function tests addreview. It tests whether the scaled score is within the range 0-10.
    The details will only be printed if the function is not working properly"""
    print("\n******************\n")
    print("Testing addreview()")
    good=True

    testingDict=addreview(resList)
    for i in range(len(testingDict)):
        if(testingDict[i]["reviewscore"]>=0 and testingDict[i]["reviewscore"]<=10):
            good=True
        else:
            good=False
    if good:
        print("\naddreview() is working properly!")
    else:
        print("\naddreview() is not working properly.")
        for res in range(len(testingDict)):
            print(testingDict[res]["name"], "\t", testingDict[res]["reviewscore"])

    cho=input("\nPress a key to go on")

# ========================================================================
# Test for addauthentic.

def testadddauthentic():
    """This function tests addauthentic. It tests whether the scaled score is within the range 0-10.
        The details will only be printed if the function is not working properly"""
    print("\n******************\n")
    print("Testing addauthentic()")
    good=True

    testingDict=addauthentic(resList)
    for i in range(len(testingDict)):
        if(testingDict[i]["authenticity"]>=0 and testingDict[i]["authenticity"]<=10):
            good=True
        else:
            good=False
    if good:
        print("\naddauthentic() is working properly!")
    else:
        print("\naddauthentic() is not working properly.")
        for res in range(len(testingDict)):
            print(testingDict[res]["name"], "\t", testingDict[res]["authenticity"])
    cho=input("\nPress a key to go on")

# ========================================================================
# Test for addspicy.
def testaddspicy():
    """This function tests addspicy. It tests whether the scaled score is within the range 0-10.
         The details will only be printed if the function is not working properly"""
    print("\n******************\n")
    print("Testing addspicy()")
    good=True

    testingDict=addspicy(resList)
    for i in range(len(testingDict)):
        if(testingDict[i]["spiciness"]>=0 and testingDict[i]["spiciness"]<=10):
            good=True
        else:
            good=False
    if good:
        print("\naddspicy() is working properly!")
    else:
        print("\naddspicy() is not working properly.")
        for res in range(len(testingDict)):
            print(testingDict[res]["name"], "\t", testingDict[res]["spiciness"])
    cho=input("\nPress a key to go on")

# ========================================================================
# Test for addprice
def testaddprice():
    """This function tests addprice. It tests whether the price is converted correctly.
    The details will only be printed if the function is not working properly"""
    print("\n******************\n")
    print("Testing addprice()")
    good=True

    testingDict=addprice(resList)
    for i in range(len(testingDict)):
        if(testingDict[i]["priceRange"]=="Under $10" and testingDict[i]["price"]==5):
            good=True
        elif (testingDict[i]["priceRange"] == "$11-30" and testingDict[i]["price"] == 7.5):
            good = True
        elif (testingDict[i]["price"]==10):
            good = True
        else:
            good=False
    if good:
        print("\naddprice() is working properly!")
    else:
        print("\naddprice() is not working properly.")
        for res in range(len(testingDict)):
            print(testingDict[res]["name"], "\t", testingDict[res]["priceRange"], "\t", testingDict[res]["price"])
    cho=input("\nPress a key to go on")

# ========================================================================
# Test for score.
def testscore():
    """This function tests score. It tests whether the score is calculated correctly
    under the situation spicyWeight = 10,priceWeight = 0,authWeight = 10.
    The details will be printed for user to check"""
    global spicyWeight
    global priceWeight
    global authWeight

    print("\n******************\n")
    print("Testing topn()")
    print("Testing when user's preference is spicyWeight = 10,priceWeight = 0,authWeight = 10.")
    spicyWeight = 10
    priceWeight = 0
    authWeight = 10
    testingDict = score(resList)
    for res in range(len(testingDict)):
        print(testingDict[res]["name"], "\t", testingDict[res]["score"])
    cho = input("\nPress a key to go on")

# ========================================================================
# Test for topn.
def testtopn():
    """This function tests score. It tests whether the top choice is calculated correctly
        under the situation spicyWeight = 10,priceWeight = 0,authWeight = 10.
        The details will only be printed if the function does not function properly"""
    print("\n******************\n")
    print("Testing topn()")
    print("Testing when user's preference is spicyWeight = 10,priceWeight = 0,authWeight = 10.")
    good=True

    global spicyWeight
    global priceWeight
    global authWeight

    spicyWeight = 10
    priceWeight = 0
    authWeight = 10
    dictMain = addreview(addspicy(addauthentic(addprice(resList))))
    testingResult=topn(score(dictMain))
    if(testingResult[0]=="Cheng Heng Restaurant" or testingResult[0]=="Sidewalk Kitchen"):
        good=True
    else:
        good=False

    if good:
        print("\ntopn() is working properly!")
    else:
        print("\ntopn() is not working properly. It shoud return 'Cheng Heng Restaurant', but it returns:", testingResult[0])

    cho=input("\nPress a key to go on")

# ========================================================================
# Calling the Main tester function.
doTest()


