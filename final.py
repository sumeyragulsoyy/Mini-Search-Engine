import os           
from pytrie import StringTrie as Trie
import re


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
        print(str(key)+ ' : ')
        #print(str(printWord(file, val, param[0])))
        #By giving the file, positions and word, printing strings from txt file
        printWord(file, val, param[0])
        print()
    return

#This function prints the strings with the specified positions
def printWord(file, index, word):
    #fileInd holds the character index in the file to
    #fileInd = 0
    #Holds the index of the position index
    countInd=0
    #for item in index:
    #Reading txt file line by line
    for line in file:
        #words = re.findall(r'\w+',line)
        #Seperating the words by whitespaces
        words = line.split(' ')
        #Checking each word
        for iter in words:
            #If there are still positions to print
            if countInd <= len(index)-1:
                #Cleaning the word from ' char
                iter2 = re.sub("'", '', iter)
                #if index[countInd]-fileInd < len(line) and iter2.lower() == word:
                #Comparing the word and the current text which are the same or not
                if iter2.lower() == word or iter2.lower() == word + '\n':
                    #print(line[index[countInd]-fileInd: index[countInd]-fileInd+len(word)])
                    #Printing the strings from specified positions on the txt file
                    print(str(index[countInd]) + ': ' + iter)
                    #------------! filelist artık set ,list değil bastırırken hata geliyor bakılacak
                   # print(+ fileInd)
                    countInd += 1
        
        #fileInd += len(line)-1
    return

def returnIndexofWord(ormalline,words,n,counter):
    query=words[n]
    r = re.compile(query)
    indexx=[[m.start(),m.end()] for m in r.finditer(ormalline)] #all matches characters
    newIndexx=indexx.copy()
    for h in range(len(indexx)):
        flag=1
        if  indexx[h][0] !=0 : # başlangıç 0 dan farklıysa önceki char kontrolü
            if ormalline[indexx[h][0]-1].isalpha() : #start index check for 17 ,ıt is not a starting index of line
                flag=0 # this is a not a starting of the searched word, this is another word
                newIndexx.remove(indexx[h])
        if flag==1 and indexx[h][1] !=len(ormalline): # starting index is meaningful ,end check should be
            if ormalline[indexx[h][1]].isalpha(): # It is not an end of word ,this end index is meaningless
                newIndexx.remove(indexx[h])
        
    #newIndexx    # exact match indexes from original txt word by word
    startingIndex=[]
    for s in range(len(newIndexx)): # take starting index of repeated string in one line ,we are looking line by line
        startingIndex.append(newIndexx[s][0]+counter) # take only starting index
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
            res = re.findall(r'\w+',line) #to get word one by one without punctional marks
            words=normalLine.split() #split by whitespace to get indexes of each word 
            
            #take list of words line by line ,convert lower and put with filename to trie
            for j in range(len(res)):
                #check the key existence in the trie
                #need index data
                
                #index = counter + line.index(res[j]) #take index of each word
                index=returnIndexofWord(normalLine,words,j,counter)
                
                if not firstTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    firstTrie[res[j].lower()] = {all_files[i]:{index[0]}} # word-> set of file, index : set
                    if len(index) !=1:
                        for r in range(1,len(index)):
                            firstTrie.get(res[j].lower()).get(all_files[i]).add(index[r])
                
                elif all_files[i] in firstTrie[res[j].lower()].keys(): #means that word same, file same, index different
                    # set is not empty so we try to add if not exist the indexes one by one 
                    for a in range(len(index)):    
                        firstTrie.get(res[j].lower()).get(all_files[i]).add(index[a]) # if word is IN the trie add only file info to fileSET OF WORD
                
                else: #word same,file different so index doesn't exist
                    firstTrie.get(res[j].lower())[all_files[i]]={index[0]}
                    if len(index) !=1:
                        for n in range(1,len(index)):
                            firstTrie.get(res[j].lower()).get(all_files[i]).add(index[n])
                        
            counter += len(line)-1    

while True:
    MENU = input('\nWhich query do you want to execute? Select a number. \n1.Search a prefix on the trie  \n2.Common words of files \n3.Exit\n')
    #If the chosen option is finding prefix
    if MENU == '1':
        pre = input('Enter a prefix to search words: ')
        #eğer girilen input ozge's is ozges yap öyle trie da arat !!!!!!!! bu eklenecek
        X = firstTrie.items(prefix=pre.lower())  #LİST OF WORD,FİLE NAME,İNDEX NUMBER IN FILES   
        if X:
            for g in range(len(X)):
                #Print method to print all occurences fiven prefix
                printStr(X[g])
                #print(str(X[g]) + "\n")
        else:
            #Giving error
            print('There is no words starting with this prefix.') 
    #If the chosen option is common words
    elif MENU == '2':
        files = input('Enter file names to search common words: ').split() #seperated by whitespace
                            
        for word in secondTrie:
            flag = 1
            for z in range(len(files)):
                if not files[z] in secondTrie.get(word):
                    flag = 0
                    break
            if flag == 1: #means that this word exist in given files COMMONLY
                print(word)
    #Exiting from the program
    elif MENU == '3':
        break 
    #Giving error for the invalid options
    else:
        print('Please enter a valid character 1,2 or 3')       



   


      