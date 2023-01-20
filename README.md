# WikiGame
The Wiki Game is a hypertextual game designed to work specifically with Wikipedia. Objective is to start on the randomly selected article and navigate to another pre-selected target article but this Python script does searching instead of you and provides path from start to destination article.

The game is based of uninformed search algorithm *Breadth First Search*.



After goal article is found, there is possibility to visualize graph diagram using d3.js functionallity. 
It is required to add content of treeData.json (which is essentially nested dictionary turned into json dump file) to variable treeData in index.html file. There are two examples of json dictionaries, one is Cat to Dog connection and the other is failed attempt to connect Archerfish to Santa Maria Rupes, which has 4 degrees of connection based on [Six Degrees of Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia)

