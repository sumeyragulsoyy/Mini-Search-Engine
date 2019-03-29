import os           
from pytrie import StringTrie as Trie
import re
import string


#Checking for valid path name until user enters a valid path name
while True:
    path = input('Enter a valid path that includes txt files : ')  
    if os.path.exists(path):
        all_files = os.listdir(path)
        break

#This function takes each word in the trie with the given prefix
#and prints the occurences in the txt files and positions
def printStr(param):
    #Printing the word
    print('WORD : ' + param[0])
    #Printing the positions and their corresponding strings from txt file
    for key in param[1]:
        #val variable holds the positions of the word
        val = param[1][key]
        #Opening the file
        file = open(path + '\\' + key,'r')
        #Printing the txt file name
        if val:
            print(str(key)+ ' : ')
        #By giving the file, positions and word, printing strings from txt file
        printWord(file, val, param[0])
        print()
    return

#This function prints the strings with the specified positions
def printWord(file, index, word):
    index = sorted(index)
    #Holds the index of the position index
    countInd=0
    #Reading txt file line by line
    for line in file:
        if countInd == len(index):
            break
        #Seperating the words by whitespaces
        words = line.split(' ')
        #Checking each word
        for iter in words:
            #If there are still positions to print
            if countInd <= len(index)-1:
                #Cleaning the word from ' char
                #iter2 = re.sub("'", '', iter)
                iter2 = iter.translate(str.maketrans('', '', string.punctuation))
                #Comparing the word and the current text which are the same or not
                if iter2.lower() == word or iter2.lower() == word + '\n':
                    #Printing the strings from specified positions on the txt file
                    if('\n' in iter):
                        iter = iter[:-1]
                    print(str(index[countInd]) + ' : ' + iter)
                    countInd += 1
            else: #All words are found
                break
    return

#This function returns the indexes of the words
def returnIndexofWord(normalline,words,n,counter):
    query=words[n]
    r = re.compile(query)
    indexx=[[m.start(),m.end()] for m in r.finditer(normalline)] #all matches characters
    newIndexx=indexx.copy()
    for h in range(len(indexx)):
        flag=1
        if  indexx[h][0] !=0 : #If the beginning of the word is is not zero index 
            if normalline[indexx[h][0]-1].isalpha() : #Checks whether previous char is letter or not
                flag=0 #This is a not a starting of the searched word, this is another word
                newIndexx.remove(indexx[h])
        if flag==1 and indexx[h][1] !=len(normalline): #Starting index is meaningful ,end check should be
            if normalline[indexx[h][1]].isalpha(): #It is not an end of word, this end index is meaningless
                newIndexx.remove(indexx[h])
        
    startingIndex=[]
    for s in range(len(newIndexx)): #Take the starting indexes of repeated same strings in one line, we are looking line by line
        startingIndex.append(newIndexx[s][0]+counter) #Take only starting index not the end index
    return startingIndex

#Creating empty trie for query1
firstTrie = Trie()
#Creating empty trie for query2
secondTrie = Trie()


#Building the trie for query 2 which is common words
for i in range(len(all_files)):
    with open(path + '\\' + all_files[i],'r') as f:
        
        for line in f:
            line = re.sub("'", '', line) #Removing ' char
            #Seperating the words
            res = re.findall(r'\w+',line) 
            #take list of words line by line ,convert lower and put with filename to trie

            for j in range(len(res)):
                #check the key existence in the trie
                if not secondTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    secondTrie[res[j].lower()] = {all_files[i]} # word-> set of file
                else:
                    secondTrie.get(res[j].lower()).add(all_files[i]) # if word is IN the trie add only file info to fileSET OF WORD

#Building the trie for the query 1 which is printing the all occurences of the given prefix
for i in range(len(all_files)):
    with open(path + '\\' + all_files[i],'r') as f:
        counter=0
        
        for line in f:
            normalLine = line #With ' characters
            line = re.sub("'", '', line) #Removing ' char
            line = re.sub('-', '', line) #Removing - char
            res = re.findall(r'\w+',line) #to get word one by one without punctional marks
            words=normalLine.split() #Split by whitespace to get indexes of each word 
            
            #Take list of words line by line ,convert lower and put with filename to trie
            for j in range(len(res)):
                index = returnIndexofWord(normalLine,words,j,counter)
                
                if not firstTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    firstTrie[res[j].lower()] = {all_files[i]:{index[0]}} # word-> set of file, index : set
                    if len(index) !=1:
                        for r in range(1,len(index)):
                            firstTrie.get(res[j].lower()).get(all_files[i]).add(index[r])
                
                elif all_files[i] in firstTrie[res[j].lower()].keys(): #Means that word is the same, file same and index is different
                    #Set is not empty so we try to add if not exist the indexes one by one 
                    for a in range(len(index)):    
                        firstTrie.get(res[j].lower()).get(all_files[i]).add(index[a]) #If word is IN the trie add only file info to fileSET OF WORD
                
                else: #Word is same, file is different so index doesn't exist
                    firstTrie.get(res[j].lower())[all_files[i]]={index[0]}
                    if len(index) !=1:
                        for n in range(1,len(index)):
                            firstTrie.get(res[j].lower()).get(all_files[i]).add(index[n])
            counter += len(line)-1    
#MENU 
while True:
    MENU = input('\nWhich query do you want to execute? Select a number. \n1.Search a prefix on the trie  \n2.Common words of files \n3.Exit\n')
    #If the chosen option is finding prefix
    if MENU == '1':
        pre = input('Enter a prefix to search words: ')
        pre = re.sub("'", '', pre)
        pre = re.sub("-", '', pre)
        X = firstTrie.items(prefix=pre.lower())  #Output list of the words, file names and index number in the files   
        if X:
            for g in range(len(X)):
                #Print method to print all occurences fiven prefix
                printStr(X[g])
        else:
            #Giving error
            print('There is no words starting with this prefix.') 
    #If the chosen option is common words
    elif MENU == '2':
        files = input('Enter file names to search common words: ').split() #seperated by whitespace
        common = 0 #Checks whether common words or not                   
        common_words = [] #Output list
        for word in secondTrie:
            flag = 1
            for z in range(len(files)):
                if not files[z] in secondTrie.get(word):
                    flag = 0
                    break
            if flag == 1: #means that this word exist in given files COMMONLY
                common_words.append(word)
                common = 1
        if common == 1:
            print(common_words)
        else:
            print('\nThere is no common word')
    #Exiting from the program
    elif MENU == '3':
        break 
    #Giving error for the invalid options
    else:
        print('Please enter a valid character 1,2 or 3')       



   


      