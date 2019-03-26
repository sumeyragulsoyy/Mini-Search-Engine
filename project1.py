import os           
from pytrie import StringTrie as Trie
import re
myTrie=Trie() # create empty trie FOR QUERY2
myTrie1=Trie() #create empty trie FOR QUERY1
path=input('Hello, \nFirstly,Enter a path that includes txt files : ')  
all_files = os.listdir(path) 

#BUİLD TRİE FOR QUERY 2
for i in range(len(all_files)):
    with open(all_files[i],'r') as f:
        for line in f:
            res = re.findall(r'\w+',line) 
            #take list of words line by line ,convert lower and put with filename to trie
            for j in range(len(res)):
                #check the key existence in the trie
                if not myTrie.has_key(res[j].lower()): #  word is NOT in the trie
                    myTrie[res[j].lower()]={all_files[i]} # word-> set of file
                else:
                    myTrie.get(res[j].lower()).add(all_files[i]) # if word is IN the trie add only file info to fileSET OF WORD

#BUİLD TRİE FOR QUERY 1
for i in range(len(all_files)):
    with open(all_files[i],'r') as f:
        counter=0
        for line in f:
            res = re.findall(r'\w+',line) 
            #take list of words line by line ,convert lower and put with filename to trie
            for j in range(len(res)):
                #check the key existence in the trie
                #need index data
                index=counter + line.index(res[j]) #take index of each word
                if not myTrie1.has_key(res[j].lower()): #  word is NOT in the trie
                    myTrie1[res[j].lower()]={all_files[i]:[index]} # word-> set of file
                elif all_files[i] in myTrie1[res[j].lower()].keys(): #means that word same, file same, index different
                    myTrie1.get(res[j].lower()).get(all_files[i]).append(index) # if word is IN the trie add only file info to fileSET OF WORD
                else: #word same,file different so index doesn't exist
                    myTrie1.get(res[j].lower())[all_files[i]]=[index]
            counter +=len(line)-1    





while True:
    MENU=input('Which do you want to query? Select number. \n1.SEARCH with PREFİX on the TRIE  \n2.COMMON WORDS OF FILES \n3.EXIT\n')
    if MENU == '1':
        pre=input('Enter a prefix to search words: ')
        X=myTrie1.items(prefix=pre.lower())  #LİST OF WORD,FİLE NAME,İNDEX NUMBER IN FILES   
        for g in range(len(X)):
            print(X[g])
        
    elif MENU == '2':
        files=input('Enter file names to search common words: ').split() #seperated by whitespace
                            
        for word in myTrie:
            flag=1
            for z in range(len(files)):
                if not files[z] in myTrie.get(word):
                    flag=0
                    break
            if flag==1: #means that this word exist in given files COMMONLY
                print(word)
    elif MENU == '3':
        break        



   


      