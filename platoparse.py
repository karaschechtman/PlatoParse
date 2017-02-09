import xml.etree.ElementTree as ET
import os
import networkx as nx
import matplotlib.pyplot as plt
import re




c_dialogues = {}

# storing the characters and their dialogues

for filename in os.listdir('xml'):
    if filename.endswith('.xml'):
        tree=ET.parse(os.path.join('xml',filename))
        texts = tree.getroot().find('text').find('group')

        # first we want to compile a memory of all the character lists
        if texts is None:
            if filename == 'Perseus_text_1999.01.0168.xml':
                dialogueName = 'Republic'
            else:
                dialogueName = 'Laws'

            cast = tree.getroot().find('text').find('front').find('castList')
            if cast is not None:
                for item in cast:
                    name = item.find('role').text
                    if name.endswith('of '):
                        name = name[:-3]

                    if '\n' not in name:
                        if name not in c_dialogues.keys():
                            c_dialogues[name] = []
                        c_dialogues[name].append(dialogueName)
        else:
            for text in texts:
                dialogueName = text.attrib['n']
                cast = text.find('body').find('castList')
                if cast is not None:
                    for item in cast:
                        name = item.find('role').text
                        if name is not None and name.endswith('of '):
                            name = name[:-3]

                        if name is not None and name not in c_dialogues.keys():
                            c_dialogues[name] = []
                        if name is not None:
                            c_dialogues[name].append(dialogueName)

# now, to establish a dictionary of mentions


c_mentions = {}

for filename in os.listdir('xml'):
    if filename.endswith('.xml'):
        tree=ET.parse(os.path.join('xml',filename))
        texts = tree.getroot().find('text').find('group')

        dialogueName = ''

        # checking for case of Republic/Laws
        if texts is None:
            if filename == 'Perseus_text_1999.01.0168.xml':
                dialogueName = 'Republic'
            else:
                dialogueName = 'Laws'

        else:
            for text in texts:
                dialogueName = text.attrib['n']
        lines = text.find('body').findall('sp')
        for line in lines:
            for character in c_dialogues.keys():
                if character is not None and line.find('p').text is not None and character in line.find('p').text and dialogueName not in c_dialogues[character]:
                    if character not in c_mentions.keys():
                        c_mentions[character] = []
                    if dialogueName not in c_mentions[character]:
                        c_mentions[character].append(dialogueName)


# UNDIRECTED
mentionGraph = nx.Graph()

for character in c_mentions.keys():
    for dialogue in c_mentions[character]:
        mentionGraph.add_node(dialogue)
        for dialoguein in c_dialogues[character]:
            mentionGraph.add_node(dialoguein)
            mentionGraph.add_edge(dialogue,dialoguein)

nx.draw(mentionGraph, with_labels = True)
plt.show()
plt.savefig( "undirectedlabels.png" )

# DIRECTED
mentionGraph2 = nx.DiGraph()

for character in c_mentions.keys():
    for dialogue in c_mentions[character]:
        mentionGraph2.add_node(dialogue)
        for dialoguein in c_dialogues[character]:
            mentionGraph2.add_node(dialoguein)
            mentionGraph2.add_edge(dialogue,dialoguein)

nx.draw(mentionGraph2,pos=nx.spring_layout(mentionGraph2),with_labels=True)
plt.show()
plt.savefig("directedlabels.png")



