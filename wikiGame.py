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

import requests
from bs4 import BeautifulSoup
import sys
import networkx as nx
import json
import wikipedia
from time import sleep
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# set language on wikipedia
wikipedia.set_lang('sr')
# Entering start and goal article 
startArticle = str(input('Enter start article: '))
goalArticle = str(input('Enter goal article: '))
startArticle = startArticle.replace(" ", "_")
goalArticle = goalArticle.replace(" ", "_")
visited = [startArticle]
hyperlinks={}
path=[startArticle]
level=0


# Function that gets all hyperlinks from article page
def getLinksFrom(article):

    try:
        page = wikipedia.page(article)
        links = page.links
        hyperlinks = {}
        
        for link in links:
            
            hyperlinks[link] = {}
        
            
    except wikipedia.exceptions.PageError:
        hyperlinks=None
    except wikipedia.exceptions.DisambiguationError as e:
        for name in e.options:
            try:
                page = wikipedia.page(name)
                links = page.links
                hyperlinks = {}
                for link in links:
                    hyperlinks[link] = {}
                return hyperlinks
            except wikipedia.exceptions.DisambiguationError:
                hyperlinks=None
                pass
    except KeyError:
        hyperlinks=None
            
    return hyperlinks

# Converting nested ditionary to networkx graph
def toGraph(dictionary):
    graph = nx.from_dict_of_dicts(dictionary,multigraph_input=True)
    return graph

# Convert nested dictionary to graphable format for JSON dumps   
def convert(d):
    for k, v in d.items():
        return {"name": k, "children": convert_helper(v)}

def convert_helper(d):
    if isinstance(d, dict):
        return [{"name": k, "children": convert_helper(v)} for k, v in d.items()]
    else:
        return [{"name": d}]


# Adding more nesting levels using recursion
        
def deeperLevel(dictionary, level=0):
    for new_tree in dictionary.values():
        if level==0:
            for parent_tree in new_tree:
                path.append(parent_tree)
                wikiSearchBfs(new_tree, parent_tree, recursion=1)
                path.pop()
        elif level==1:
            for parent_tree in new_tree.values():
                for parent in parent_tree:
                    #wikiSearchBfs(parent_tree, parent, recursion=1)
                    print(parent)
                    print(parent_tree)
                    break
                break
            
def thirdLevel(dictionary):
    for new_tree in dictionary.values():
        for parent_tree in new_tree.values():
            for parent in parent_tree.values():
                for kid in parent:
                        wikiSearchBfs(parent, kid, recursion=1)
    

# wikiSearchBfs function is based on Breacth first Search algorithm 
def wikiSearchBfs(tree_dict1, parent, recursion=0, level=0):
    try:
        for i in tree_dict1[parent]: # iterating through children from parent node            
            if i not in visited:# if node already exists, don't iterate again
                visited.append(i)
                path.append(i)
                children = getLinksFrom(i)
                sleep(1)
                if children!=None:
                    if goalArticle in children: # if goal node found -> end program and print parents
                        print('Goal article found!\n')
                        print("Full path from start article to goal article is {}".format(path)) # Print path to goal article
                        print('\n')
            
                        tree_dict1[parent][i] = children # Append last article into visited nodes
                        
                        G = toGraph(tree_dict) # Convert nested dictionary to graph
                        print("Diameter of a graph is {}".format(nx.diameter(G)))
                        #print("\nEccentricity of graph is {}".format(nx.eccentricity(G)))                  
                        # load nested ditionaty into json file 
                        with open('treeData.json', 'w') as outfile:
                            json.dump(convert(tree_dict), outfile)
    
                        sys.exit(0)
                    path.pop()
                
                    for k in list(children): # check if node has already been visited
                        if k in visited:
                            del children[k]  # if so, delete that node from children list
                    tree_dict1[parent][i] = children
                
                    
              
        if recursion==0:
            
            try:
                # Second degree
                print("Second Degree!")
                deeperLevel(tree_dict1)
                print("Third Degree!")
                deeperLevel(tree_dict1,level=1)
                

            except:
                print("Unexpected error in recursion:", sys.exc_info()[0])
                pass
                    
    except KeyError:
        pass
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Unexpected error in wikiS:", sys.exc_info()[0])
        sys.exit()
        pass   
        
       

# Function that checks if the goal hyperlink (article) is already in the start article hyperlinks
# If not then calls wikiSearchBfs function
def checkDict(tree_dict, start=startArticle):
    for items in tree_dict.values():
        if goalArticle in items:
                print('The goal topic is in the first article!!')
                sys.exit()
        else:
            print('Begining search')
            wikiSearchBfs(tree_dict, start, recursion=0)
# Function that checks if the start and goal article is valid
def checkPage(start, goal):
    if start=="" or goal=="":
        return False
    try:
         wikipedia.page(start)
         wikipedia.page(goal)
         return True
    except wikipedia.exceptions.PageError:
        print("Invalid page name!")
        return False
    except wikipedia.exceptions.DisambiguationError as e:
        print("Choose specific article from this list and try again.")
        print(e.options)
        
# function that uses directlyy beautifoul soup and requests to check goal and start article               
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
    
    if checkPage(startArticle, goalArticle):
        # set initial dictionary to be from start article
        tree_dict = {startArticle: getLinksFrom(startArticle)}
        try:
            checkDict(tree_dict, startArticle)
        except:
            pass
    

            

    
