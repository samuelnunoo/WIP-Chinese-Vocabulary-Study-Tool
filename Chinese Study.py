import os
from bs4 import BeautifulSoup
import re
import sqlite3


#Initialize/Update the Database
def Create_Databate():
    with sqlite3.connect("Articles.db") as con:
        c=con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Article
                    (name text, tags text, hsk real)''')


        for item in os.listdir("Articles"):
            os.chdir(r'C:\Users\Samuel\Documents\Chinese Study Software\Articles')
            with open(item,'rb') as file:
                try:
                    soup=BeautifulSoup(file,"html.parser")

                    #Tags
                    tags=soup.find('div',attrs={'class':'topcats hidden-md hidden-lg'}).text
                    
                    #HSK Level
                    hsk=soup.find('div',attrs={'class':'featured'})
                    value=re.findall('level bg_level_.',str(hsk))
                    hsk=soup.find('div',attrs={'class':value[0]}).text
                    
                    #Name
                    name=(file.name).split('.html')[0]


                    #Check and Insert
                    c.execute("SELECT * FROM Article WHERE name=?",(name,))
                    entry=c.fetchone()
                    if entry is None:
                        c.execute("INSERT INTO Article VALUES (?,?,?)",(name,tags,hsk))
                        print("{} || {} || {}".format(name,tags,hsk))
                    else:
                        return 'Item Already Exists'

                    
                except:
                    print("fake file")
                    continue


#Search
def Search_Database(name_="*",tags_="*",hsk="*"):
    with sqlite3.connect("Articles.db") as con:
        c=con.cursor()
        
        c.execute("SELECT * FROM Article WHERE tags LIKE ?",(tags_,))
        item=c.fetchall()
        print(item)
      
    

def Select_Database(selection):
    with sqlite3.connect("Vocabulary.db") as con:
        c=con.cursor()

        #Check if Column of name selection if not then create
        c.execute('CREATE TABLE IF NOT EXISTS Articles(name TEXT,text TEXT,vocab TEXT, idioms TEXT, grammar TEXT)')

        #Check if Empty
        c.execute('SELECT * FROM Articles WHERE name=?',(selection,))
        item=c.fetchone()
        
        if not item:
            #Open the File
            file_=selection+".html"
            with open(file_,'rb') as html:
                soup=BeautifulSoup(html,'html.parser')
            
                def Cleanify(args):
                    if args:
                        
                        argz=re.sub(r'[(\u200b)(\t)]',"",args.text).split('\r')
                        args_list=[re.sub(r'\r',"",items).split('-') for items in argz]
                        print(args_list)
                        return str(args_list)
                        
                    else:
                        return None 

                
                text=soup.find('div',attrs={'id':'news_article'}).get_text(strip=True)
                vocab=Cleanify(soup.find('div',attrs={'id':'tabs-k'}))
                grammar=Cleanify(soup.find('div',attrs={'id':'tabs-g'}))
                idioms=Cleanify(soup.find('div',attrs={'id':'tabs-i'}))
                 
                c.execute("INSERT INTO Articles VALUES (?,?,?,?,?)",(selection,text,vocab,idioms,grammar))  
                c.execute("SELECT * FROM Articles WHERE name=?",(selection,)) 
                item=c.fetchone()
                

        return item 
 



test=Select_Database(r'$100 Million Zhengzhou Overpass Increases Traffic Jams Instead of Reducing Them')

print(test)
working=test[1:len(test)-1]   

        #Extract Text

        #Extract Vocab | Grammar | Idoms 

        #Create Example Sentences 

        #Columns

        #|Name of Selection|


        #Rows

        #> Vocabulary w Example Sentences
        #> Text
        #> Grammar
        #> Idioms 
        

        ###Proposed Usage from Vocab iterate [{word,meaning,sentence},{...}]
        ### Usage Text |Just Show Text|
        ###Usage Grammar [{word,usage etc...},{...}]
        ###Usage Idioms [{idiom,usage etc...},{...}]










#Variables=[name_,tags_,hsk]
#Variables=[i for i in Variables if i!=None]