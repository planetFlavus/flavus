# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

char_tilde = u'\u0303'
               
import re      
               
text = u""      

while True:
    inp = raw_input()

    if inp == "":
        break

    text += unicode(inp + "\n",'utf-8')

text = text.lower()

replacements_demorog = [
       ( "y" , "ɨ"),
       ( "tt" , "tː"),
       ( "dd" , "dː"),
       ( "sh" , "ʃ"),
       ( u"ng" , u"ŋ"),
       ( u"ŋ([aeyo])" , "ŋ\\1"+char_tilde),
       ( "dh" , "ð"),
       ( u"ː\\b" , "ːə")
        ]

replacements_pp = []
#        "~o":"õ",
#        "~a":"ã",
#        "~e":"ẽ",
#        "~y":"ỹ"
#        }

replacements = replacements_demorog + replacements_pp

#print replacements

for key, value in replacements:
    text = re.sub(key, value, text,re.UNICODE)

print text
