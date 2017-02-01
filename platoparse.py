import xml.etree.ElementTree as ET
import os
from os import path

c_dialogues = {}

for filename in os.listdir('xml'):
    if filename.endswith('.xml'):
        tree=ET.parse(os.path.join('xml',filename))
        texts = tree.getroot().find('text').find('group')

        # first we want to compile a memory of all the character lists
        if texts is None:
            continue

        else:
            for text in texts:
                dialogueName = text.attrib['n']
                c_dialogues[dialogueName] = []
                cast = text.find('body').find('castList')
                if cast is not None:
                    for item in cast:
                        c_dialogues[dialogueName].append(item.find('role').text)

print c_dialogues # dialogue cast lists