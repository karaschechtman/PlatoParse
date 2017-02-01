import xml.etree.ElementTree as ET

tree=ET.parse('Perseus_text_1999.01.0176.xml')

texts = tree.getroot().find('text').find('group')


# first we want to compile a memory of all the character lists
if texts is None:
    print 'Not a group!'

else:
    c_dialogues= {}
    for text in texts:
        print '\n' + text.attrib['n'].upper()
        print '---------------------------------'
        cast = text.find('body').find('castList')
        print 'CHARACTER LIST'
        for item in cast:
            print item.find('role').text

