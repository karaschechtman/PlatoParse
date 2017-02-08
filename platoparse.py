import xml.etree.ElementTree as ET
import os
import networkx as nx
import matplotlib

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
                    if '\n' not in item.find('role').text:
                        if item.find('role').text not in c_dialogues.keys():
                            c_dialogues[item.find('role').text] = []
                        c_dialogues[item.find('role').text].append(dialogueName)
        else:
            for text in texts:
                dialogueName = text.attrib['n']
                cast = text.find('body').find('castList')
                if cast is not None:
                    for item in cast:
                        if item.find('role').text not in c_dialogues.keys():
                            c_dialogues[item.find('role').text] = []
                        c_dialogues[item.find('role').text].append(dialogueName)

# character lists - demonstrates I'll need to fix some of these (the ones that have " of"
for key in c_dialogues.keys():
    print key
    print '----------'
    for character in c_dialogues[key]:
        print character
    print ''

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



mentionGraph = nx.DiGraph()

for character in c_mentions.keys():
    for dialogue in c_mentions[character]:
        mentionGraph.add_node(dialogue)
        for dialoguein in c_dialogues[character]:
            mentionGraph.add_node(dialoguein)
            mentionGraph.add_edge(dialogue,dialoguein)

nx.draw(mentionGraph)