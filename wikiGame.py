# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:58:48 2020

@author: Vukasin Vasiljevic

 Project: WikiGame
 
 Description: 
     
     Inputs: Wikipedia article (start article), goal topic (goal article).
     Output: Path from start article to goal article.
     
     Example:
         Enter start article: Cat

         Enter goal article: Dog
         Begining search
         
         Goal article found!
         
         ['Cat', 'Domestication', 'Cat_anatomy', 'Near_East', 'en.wikipedia.org', 
         'Old_English', 'en.wiktionary.org', 'Scientific_name', 
         'International_Commission_on_Zoological_Nomenclature', 'Family_(biology)', 
         'Taming', 'Preadaptation', 'Cat_breeds', 'European_wildcat', 'Cervical_vertebrae',
         'Eye_socket', 'Digitigrade', 'Dewclaw']
         
         Diameter of graph is 2
         
         Eccentricity of graph is {'Cat': 1, 'Domestication': 2, 'Cat_anatomy': 2, 'Near_East': 2,
         'Old_English': 2, 'Scientific_name': 2, 'International_Commission_on_Zoological_Nomenclature': 2, 
         'Family_(biology)': 2, 'Taming': 2, 'Preadaptation': 2, 'Cat_breeds': 2, 'European_wildcat': 2, 
         'Cervical_vertebrae': 2, 'Eye_socket': 2, 'Digitigrade': 2, 'Dewclaw': 2}
         
         
    Note: This algorithm does not provide the shortest path, it is based on uninformed search
          algorithm (Breadth First Search). Also, this is not optimal nor complete algorithm i.e. 
          this algorithm doesn't always find path


"""

import re
import requests
from bs4 import BeautifulSoup
import sys
import networkx as nx
import json



startArticle = str(input('Enter start article: '))
goalArticle = str(input('Enter goal article: '))
startArticle = startArticle.replace(" ", "_")
goalArticle = goalArticle.replace(" ", "_")
visited = [startArticle]



# Function that gets all hyperlinks from /wiki/article page
def getLinksFrom(article):
    page = "https://en.wikipedia.org/wiki/" + article # string concatenation for url
    r = requests.get(page)
    data = r.content  # Content of response
    soup = BeautifulSoup(data, "html.parser")
    
    hyperlinks = {}
    for i in soup.find_all('p'):
       try:
           link = i.find('a',href=True)['href']
           if re.search('^#',link) or re.search('/wiki/Help:IPA', link) or re.search('/wiki/en.wiktionary.org', link) or re.search('/wiki/index.php', link):
               pass
           else:
               
               hyperlinks[link.split('/')[2]] = {} # set al linkks to be dictionaries by default
       except:
          continue
    return hyperlinks



# Converting nested ditionary to networkx graph
def toGraph(dictionary):
    graph = nx.from_dict_of_dicts(dictionary,multigraph_input=True)
    return graph

# Convert to graphable format for JSON dumps
    
def convert(d):
    for k, v in d.items():
        return {"name": k, "children": convert_helper(v)}

def convert_helper(d):
    if isinstance(d, dict):
        return [{"name": k, "children": convert_helper(v)} for k, v in d.items()]
    else:
        return [{"name": d}]


# Adding nesting levels 3 levels
        
def secondLevel(dictionary):
    for new_tree in dictionary.values():
        for parent_tree in new_tree.values():
            for parent in parent_tree:
                wikiSearchBfs(parent_tree, parent, recursion=1)
def thirdLevel(dictionary):
    for new_tree in dictionary.values():
        for parent_tree in new_tree.values():
            for parent in parent_tree.values():
                for kid in parent:
                        wikiSearchBfs(parent, kid, recursion=1)
    

# wikiSearchBfs function is based on Breacth first Search algorithm 
def wikiSearchBfs(tree_dict1, parent, recursion=0):
    try:
        for i in tree_dict1[parent]: # iterating through children from parent node            
            if i not in visited: # if node already exists, don't iterate again
                visited.append(i)
                children = getLinksFrom(i)
                if goalArticle in children: # if goal node found -> end program and print parents
                    print('Goal article found!\n')
                    print(visited) # Print visited nodes
                    print('/n')
                    tree_dict1[parent][i] = children # Append last article into visited nodes
                    G = toGraph(tree_dict)
                    print("Diameter of graph is {}".format(nx.diameter(G)))
                    print("\nEccentricity of graph is {}".format(nx.eccentricity(G)))
                    
                    # load nested ditionaty into json file 
                    with open('treeData.json', 'w') as outfile:
                        json.dump(convert(tree_dict), outfile)

                    sys.exit(0)
                
                for k in list(children): # check if node has already been visited
                    if k in visited:
                        del children[k]  # if so, delete that node from children list
                tree_dict1[parent][i] = children
                
              
        if recursion==0:
            for new_tree in tree_dict1.values():
                for parent_tree in tree_dict[parent]:
                    wikiSearchBfs(new_tree, parent_tree, recursion=1)
                    
            secondLevel(tree_dict)
            thirdLevel(tree_dict)
             
                    
    except:
        sys.exit(0)
        pass

# Function that checks if the goal hyperlink (article) is already in the start article hyperlinks
# If not then calls wikiSearchBfs function
def checkDict(tree_dict, start=startArticle):
    for items in tree_dict.values():
        if goalArticle in items:
                print('The goal topic is in the first article!!')
                break
        else:
            print('Begining search')
            wikiSearchBfs(tree_dict, start)
            
def checkArticles(start, goal):
    
    if start=="" or goal=="":
        return False   
    
    
    
    startPage = "https://en.wikipedia.org/wiki/" + start
    goalPage = "https://en.wikipedia.org/wiki/" + goal
    rS = requests.get(startPage)
    rG = requests.get(goalPage)
    dataS = rS.content
    dataG = rG.content
    soupS = BeautifulSoup(dataS, "html.parser")
    soupG = BeautifulSoup(dataG, "html.parser")

    # check each article if it exists on Wikipedia
    def checkEach(soups, title=''):
        for i in soupS.find_all('b')[0]:
            try:
                if i.getText()=='Wikipedia does not have an article with this exact name.':
                    print("Wikipedia does not have an {} article with this exact name".format(title))
                    return False
                else:
                    continue
            except:
                pass
        return True
    
       

         
    if checkEach(soupS, 'start') and checkEach(soupG, 'goal'):
        return True
    return False
    
        

if __name__=="__main__":
    # set initial dictionary to be from start article
    tree_dict = {startArticle: getLinksFrom(startArticle)}
    if checkArticles(startArticle, goalArticle):
        checkDict(tree_dict, startArticle)
     
    print("Couldn't find connection with goal article, sorry...")
    

            

    
