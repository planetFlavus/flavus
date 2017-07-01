import fontforge

# create empty font
font = fontforge.font()

# set font names
font.fontname = "FlavanGeometric"
font.fullname = "Flavan Geometric"
font.familyname = "Flavan"


# magic
font.addLookup('liga', 'gsub_ligature', (), (('liga', (('latn', ('dflt')), )), ))
font.addLookupSubtable('liga', 'liga')

extra = [u" ",u"-",u"h"]
consonants = [u"m",u"n",u"k",u"t",u"d",u"g",u"r",u"ng",u"s",u"l",u"shl",u"dh",u"dhl",u"p",u"b",u"rd",u"rb",u"f",u"sh",u"tt",u"dd",u"rk",u"ttl",u"dd",u"ttk",u"rg",u"gm",u"pd"]
vowels = [u"e",u"y",u"o"]

glyph_sizes = {
        u"gm" : 1.5,
        u"ttg" : 1.3,
        u"k": 0.8
        }

# combine vowel diacs
if True:
    import svgjoiner
    for c in consonants+[u"-"]:
        for v in vowels:
            try:
                svgjoiner.join_svgs("glyphs/%s.svg"%c, "glyphs/%s.svg"%v, "ligs/%s.svg"%(c+v))
            except IOError:
                print "no glyph %s %s"%(c,v)


glyphs = {}

for e in extra:
    glyphs[e] = e

for v in vowels:
    glyphs[v] = u"-"+v

glyphs[u"a"] = u"-"

for c in consonants:
    glyphs[c] = c
    glyphs[c+u"a"] = c
    if c in glyph_sizes:
        glyph_sizes[c+u"a"] = glyph_sizes[c]
    for v in vowels:
        glyphs[c+v] = c+v
        if c in glyph_sizes:
            glyph_sizes[c+v] = glyph_sizes[c]




# precreate glyphs to avoid error
for letter in ["s","h"]:
    if len(letter) == 1:
        glyph = font.createChar(ord(letter))



# import svgs
for letter,filename in glyphs.iteritems():
    
    if len(letter) > 1:
        glyph = font.createChar(-1,letter)
        glyph.addPosSub("liga", tuple(letter.encode('ascii')))
    else:    
        codepoint = ord(letter)
        glyph = font.createChar(codepoint)

    # import svg file into it
    fname_glyphs = "glyphs/%s.svg" % filename
    fname_ligs = "ligs/%s.svg" % filename
    try:
        glyph.importOutlines(fname_glyphs)
    except IOError:
        try:
            glyph.importOutlines(fname_ligs)
        except IOError:
            continue

    glyph.width = 1000

    if letter in glyph_sizes:
        glyph.width = int(1000*glyph_sizes[letter])

    # make the glyph rest on the baseline
    ymin = glyph.boundingBox()[1]
    #glyph.transform([1, 0, 0, 1, 0, -ymin])

    # set glyph side bearings, can be any value or even 0
#    glyph.left_side_bearing = glyph.right_side_bearing = 0

#font.generate("foobar.pfb", flags=["tfm", "afm"]) # type1 with tfm/afm
font.generate("flavangeometric.otf") # opentype
#font.generate("foobar.ttf") # truetype
