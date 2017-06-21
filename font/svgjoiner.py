import lxml.etree as et

def ns(e):
    out = e.nsmap
    del out[None]
    return out

def join_svgs(fname1,fname2,fnameout):
    e1 = et.parse(fname1).getroot()
    e2 = et.parse(fname2).getroot()




    for nicer in e2.findall("{*}*"):
        print "joind"
        e1.append( nicer )

    

    out_tree = et.ElementTree(e1)
    with open(fnameout,'wb') as file:
        file.write(et.tostring(e1,pretty_print=True))
    


#join_svgs("glyphs/m.svg","glyphs/ .svg","ligs/test.svg")
