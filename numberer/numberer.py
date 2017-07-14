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
    if n==1:
        return "e"

    strink = hex(n)[2:]
    strink = strink[::-1]

    out = ""

    for k in range(len(strink)):
        digit = int(strink[k],16)

        if (digit == 0):
            continue

        if (k == len(strink)-1) and (digit == 1):
            pass
        else:

            out += numerals[digit] + " "
        
        if (k > 0):
            out += biggies[k] + " "

    out = out.replace("e ka", "ef ka")

    return out




for i in range(257):
    print i, "%x"%i, say(i)
