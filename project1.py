import os           
from pytrie import StringTrie as Trie
import re

def printStr(param):
    print(param[0])
   
    for key in param[1]:
        val = param[1][key]
        file = open(path + '\\' + key,'r')
        print(str(key) + ':' + str(val) + ' value:' + printWord(file, val, param[0]))
    return

def printWord(file, index, word):
    fileInd = 0
    for item in index:
        for line in file:
            words = re.findall(r'\w+',line)
            if item-fileInd < len(line):
                print(line[item])
            else:
                fileInd += len(line)-1

firstTrie = Trie() #create empty trie FOR QUERY1
secondTrie = Trie() # create empty trie FOR QUERY2
# path = input('Hello, \nFirstly,Enter a path that includes txt files : ')  
# all_files = os.listdir(path) 

#Checking for valid path name
while True:
    path = input('Enter a valid path that includes txt files : ')  
    if os.path.exists(path):
        all_files = os.listdir(path)
        break


#BUİLD TRİE FOR QUERY 2
for i in range(len(all_files)):
    with open(path + '\\' + all_files[i],'r') as f:
        
        for line in f:
            line = re.sub("'", '', line) #Removing ' char
            res = re.findall(r'\w+',line) 
            #take list of words line by line ,convert lower and put with filename to trie

            for j in range(len(res)):
                #check the key existence in the trie
                if not secondTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    secondTrie[res[j].lower()] = {all_files[i]} # word-> set of file
                else:
                    secondTrie.get(res[j].lower()).add(all_files[i]) # if word is IN the trie add only file info to fileSET OF WORD

#BUİLD TRİE FOR QUERY 1
for i in range(len(all_files)):
    with open(path + '\\' + all_files[i],'r') as f:
        counter=0
        
        for line in f:
            normalLine = line #With ' characters
            line = re.sub("'", '', line) #Removing ' char
            res = re.findall(r'\w+',line)
            
            #take list of words line by line ,convert lower and put with filename to trie
            for j in range(len(res)):
                #check the key existence in the trie
                #need index data
                # if all_files[i] == 'sum.txt':
                index = counter + normalLine.index(res[j]) #take index of each word
                
                if not firstTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    firstTrie[res[j].lower()] = {all_files[i]:[index]} # word-> set of file
                
                elif all_files[i] in firstTrie[res[j].lower()].keys(): #means that word same, file same, index different
                    firstTrie.get(res[j].lower()).get(all_files[i]).append(index) # if word is IN the trie add only file info to fileSET OF WORD
                
                else: #word same,file different so index doesn't exist
                    firstTrie.get(res[j].lower())[all_files[i]]=[index]
            counter += len(line)-1    

while True:
    MENU = input('\nWhich query do you want to execute? Select a number. \n1.Search a prefix on the trie  \n2.Common words of files \n3.Exit\n')
    if MENU == '1':
        pre = input('Enter a prefix to search words: ')
        X = firstTrie.items(prefix=pre.lower())  #LİST OF WORD,FİLE NAME,İNDEX NUMBER IN FILES   
        if X:
            for g in range(len(X)):
                printStr(X[g])
                #print(str(X[g]) + "\n")
        else:
            print('There is no words starting with this prefix.') 
    
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
    elif MENU == '3':
        break 
    else:
        print('Please enter a valid character 1,2 or 3')       



   


      