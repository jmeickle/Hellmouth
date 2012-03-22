import copy
import re

class Descriptions():
    dict = {
    "dmg-sever-cut-neck" : "decapitate",
    "dmg-cripple-cut-neck" : "partially decapitate",
    "dmg-sever-crush-neck" : "crush the windpipe",
    "dmg-cut" : "slice",
    "dmg-pierce" : "stab",
    "dmg-impale" : "spear",
    "dmg-crush" : "whack",
    "dmg" : "hit",
    "dmg-crit" : "skillfully hit",
}
    hits = {}
    fail = {}

def base_stat(value):
    str = ""

    if value > 20:
        str = "godly"
    elif value > 14:
        str = "amazing"
    elif value > 12:
        str = "exceptional"
    elif value > 10:
        str = "above-average"
    elif value is 10:
        str = "average"
    elif value > 7:
        str = "below-average"
    elif value is 7:
        str = "poor"
    else:
        str = "crippling"

    return str

#def damage_amount(value):

#def size(value):

#def reach(value):

def build(terms):
    str = ""
    for term in terms:
        if term != "":
            if str == "":
                str += term
            else:
                str += "-%s" % term
#    print str
    return str

# Get a string from parts
def g(str):
    Descriptions.hits[str] = True
    return Descriptions.dict.get(str, None)

# Get whether the string failed already
def f(str):
    return Descriptions.fail.get(str, False)

def describe(str):
    exact = g(str)
    if exact is not None:
        return exact
    else:
        terms = re.split('-',str)
#        print "TERMS: %s" % terms
        ret = None
        for i in range(len(terms)):
            ret = indexed_remove(terms, i, ret)
        return ret

def indexed_remove(terms, n, ret):
#    work = terms[:]
#    print "len terms: %s" % len(terms)
    # The indices to be possibly removed in this pass:
#    print [x for x in reversed(range(len(terms)-n, len(terms)))]
    for x in reversed(range(len(terms)-n, len(terms))):
        copy = terms[:]
        copy[x]=""
        string = build(copy)
        if f(string) is False:
            query = g(string)
            if query is None:
                Descriptions.fail[string] = True
            else:
                ret = query
                return ret

    if n > 1:
        ret = indexed_remove(copy, n-1, ret)

    return ret


#        if n > 1:
#            for j in range(1, len(terms)):
#                indexed_remove(terms, j)

#        print "%s," % x,
#        if terms[x] == "":
#            continue;
#        else:
#            terms[x] = ""
#    g(terms)
#    print "/",

#    if n > 1:
#        indexed_remove(terms, n-1)
def dict(name, dict):
    print "--%s--" % name
    for k,v in dict.iteritems():
        print "| %s: %s" % (k,v)
    print "--%s--" % ("-" * len(name))

if __name__ == '__main__':
    dict("Text Database", Descriptions.dict)

    print "\nResults:"
    strs = ['dmg-sever-cut-neck-crit', 'dmg-nonsense-herp-derp', 'dmg-cut-crit',
            'dmg-cripple-neck', 'dmg-cripple-cut-neck', "dmg-sever-cut-neck"]
    for str in strs:
        print "%s => %s" % (str, describe(str))

    print ""
    dict("DB Hits", Descriptions.hits)
    print ""
    dict("DB Misses", Descriptions.fail)
