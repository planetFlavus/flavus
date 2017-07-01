numerals = [
        "kydh",
        "e",
        "ka",
        "pok",
        "demo",
        "fam",
        "eka",
        "rbargar",
        "mom",
        "dhlarma",
        "darma",
        "kodany",
        "kardeny",
        "pottke",
        "kargar",
        "dhlarda",
        "garda"]

biggies = [
        "ERR",
        "garda",
        "dhonga",
        "kottla",
        "gardakottla",
        "dhongakottla"
        ]



def say(n):

    if n==0:
        return "kydh"

    strink = hex(n)[2:]
    strink = strink[::-1]

    out = ""

    for k in range(len(strink)):
        out += numerals[int(strink[k],16)]
        out += " "

    return out




for i in range(200):
    print i, say(i)
