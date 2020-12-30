#Makena Trust - 11875871
#CS 301 Finals

# issue where counting all queries in find even if no output



from __future__ import print_function
from collections import OrderedDict
import re
import operator

collection = OrderedDict()
IDCollection = OrderedDict()
findComp = OrderedDict()


def createCollections(lines):

    p = 0

    for singleLine in line:
        pairs = singleLine.split(' ')
        singleE = OrderedDict()
        for i in range(len(pairs)/2):
            if "\n" in pairs[(i * 2)+1]:
                singleE[pairs[i*2][0]] = pairs[(i*2)+1].split("\n")[0]
            else:
                singleE[pairs[i*2][0]] = pairs[(i*2)+1]
        collection[p] = singleE
        # print(collection[p])
        IDCollection[p] = (p+1)
        p +=1

    return collection, IDCollection

def findCommand(query):
    global queryCount
    for i in range(len(query)):
        cmd = query[i].split('\n')
        if cmd[0] == 'SORT':
            singleS = query[i]
            sorting(singleS)
        elif cmd[0] == 'FIND':
            singleF = query[i]
            finding(singleF)
        else:
            queryCount = queryCount + 1
            print("\n//Query " + str(queryCount))
            print("ERROR: Invalid Command")

def finding(singleF):
    global queryCount
    queryCount = queryCount + 1
    sepFCommand = singleF.split('\n')

    global qCountHelp
    qCountHelp = 0

    for j in range(len(collection)):
        single = collection[j].keys()
        val = collection[j].values()
        first = 0
        match = 0
        error = 0
        for p in range(len(single)):
            for i in range(1, len(sepFCommand)-1):
                # print(sepFCommand[i])
                if(sepFCommand[i][0] == 'A' and first == 0):
                    # print("check A")
                    pair = re.split(' ', sepFCommand[i])
                    # print(pair[2])
                    # print(j+1)
                    if(pair[1] == '='):
                        # print("A EQUAL")
                        first = 1
                        if(pair[2] == str(j+1)):
                            # print("MATCH: " + str(match))
                            # print(collection[j])
                            match = match + 1
                        else:
                            # print("why error")
                            error = error + 1
                    elif(pair[1] == '>'):
                        if(pair[2] < str(j+1)):
                            # print("nothier")
                            match = match + 1
                        else:
                            # print("why error")
                            error = error + 1
                    elif(pair[1] == '<'):
                        if(pair[2] > str(j+1)):
                            # print("should print this line")
                            match = match + 1
                        else:
                            # print("why error")
                            error = error + 1
                    else:
                        error = error + 1
                elif(sepFCommand[i] != 'Y'):
                    if(sepFCommand[i][0] == single[p]):
                        pair = re.split(' ', sepFCommand[i])
                        if pair[1] == '=':          #letters match and is an equal comparison
                            if(pair[2] == val[p]):  #values are equal
                                # print("hi1")
                                match = match + 1
                            else:                   #letters match but the equal doesnt
                                error = error + 1
                        elif (pair[1] == '>'):      #letters match and is a GT comparison
                            if(pair[2] < val[p]):   #comparison is correct
                                match = match + 1
                                # print("hi2")
                            else:                   #comparison is incorrect
                                error = error + 1

                        elif (pair[1] == '<'):      #letters match and is LT comparison
                            if(pair[2] > val[p]):   #comparison is correct
                                match = match + 1
                                # print("hi3")
                            else:                   #comparison is incorrect
                                error = error + 1

                        else:                       #comparison is unknown
                            error = error + 1
                elif(sepFCommand[i] == 'Y'):
                    error = 0

        if(error == 0):
            # print(match)
            # print(i)
            if(match == i):                   #every field matched
                qCountHelp = qCountHelp + 1
                # queryCount = queryCount + 1
                printingFind(sepFCommand, collection[j], j)
            elif(sepFCommand[i] == 'Y'):    #has no fields
                qCountHelp = qCountHelp + 1
                # queryCount = queryCount + 1
                printingFind(sepFCommand, collection[j], j)
            else:                              #field does not exist in document
                print(end = "")
                s = len(collection) - 1
                if(qCountHelp == 0 and j == s):
                    queryCount = queryCount - 1
        # elif(error>0):
        #     print("error" + str(error))


def sorting(singleS):
    global queryCount
    sOrders = OrderedDict()
    sepSCommand = singleS.split('\n')

    if(sepSCommand[1] == ''):
        return

    queryCount = queryCount + 1

    cmdKey = sepSCommand[1].split(' = ')
    print("\n//Query " + str(queryCount))


    k = cmdKey[0]
    order = cmdKey[1]


    for i in range(len(collection)):
        keyChecker = collection[i].keys()
        valKeep = collection[i].values()
        for v in range(len(keyChecker)):
            if(keyChecker[v] == cmdKey[0] and cmdKey!= 'A'):
                sOrders.update({i: valKeep[v]})

    if(cmdKey[0]== 'A'):
        first = 0
        if(cmdKey[1] == '1'):
            for i in range(len(collection)):
                first = 0
                print("")
                if(first == 0):
                    aCount = i + 1
                    print("A: ", end= '')
                    print(aCount, end = ' ')
                    first = 1
                cKeys = collection[i].keys()
                cVals = collection[i].values()
                for p in range(len(cKeys)):
                    print(cKeys[p] + ": " + cVals[p], end = ' ')
        elif(cmdKey[1] == '-1'):
            for i in reversed(range(len(collection))):
                first = 0
                print("")
                if(first == 0):
                    aCount = i + 1
                    print("A: ", end= '')
                    print(aCount, end = ' ')
                    first = 1
                cKeys = collection[i].keys()
                cVals = collection[i].values()
                for p in range(len(cKeys)):
                    print(cKeys[p] + ": " + cVals[p], end = ' ')

        else:
            print("Sort must be by either -1 or 1")
        print("\n")

    elif(cmdKey[1] == '1'):
        first = 0
        my_list = list(sOrders.items())
        for q in range(len(my_list)-1, 0, -1):
            swapped = False
            for i in range(q):
                if int(my_list[i+1][1]) < int(my_list[i][1]):
                    # print(my_list[i][1] + " " + my_list[i+1][1])
                    my_list[i], my_list[i+1] = my_list[i+1], my_list[i]
                    # my_list[i+1], my_list[i] = my_list[i], my_list[i+1]
                    swapped = True
            if not swapped:
                break
        for p in range(len(my_list)):
            first = 0
            q = my_list[p][0]
            cKeys  = collection[q].keys()
            cVals = collection[q].values()
            for i in range(len(cKeys)):
                if(first == 0):
                    count = q + 1
                    print("A: ", end = "")
                    print(count, end = ' ')
                    first = 1
                print(cKeys[i] + ": " + cVals[i], end = ' ')
            print("")
        print("")

    elif(cmdKey[1] == '-1'):
        first = 0
        my_list = list(sOrders.items())
        for q in range(len(my_list)-1, 0, -1):
            swapped = False
            for i in range(q):
                if int(my_list[i][1]) < int(my_list[i+1][1]):
                    # print(my_list[i][1] + " " + my_list[i+1][1])
                    my_list[i], my_list[i+1] = my_list[i+1], my_list[i]
                    swapped = True
            if not swapped:
                break

        for p in range(len(my_list)):
            first = 0
            q = my_list[p][0]
            print("")
            cKeys  = collection[q].keys()
            cVals = collection[q].values()
            for i in range(len(cKeys)):
                if(first == 0):
                    count = q + 1
                    print("A: ", end = "")
                    print(count, end = ' ')
                    first = 1
                print(cKeys[i] + ": " + cVals[i], end = ' ')
        print("\n")

    else:
        print("Error: must either sort by -1 or 1 ")
print("\n")


def printingFind(printingLine, printingVals, j):
    if(qCountHelp == 1):
        print("\n//Query " + str(queryCount))
    # else:
    #     queryCount = queryCount - 1
    # print("Q COUNT" + str(queryCount))
    # print("J " + str(j))

    first = 0
    queryPrint = 0
    key = printingVals.keys()
    val = printingVals.values()
    curr = printingLine[len(printingLine)-1].split(" ")
    for i in range(len(key)):
        noNew = 0
        for v in range(0, len(curr)):
            # if(qCountHelp == 1 and queryPrint == 0):
            #     queryCount = queryCount + 1
            #     print("\n//Query " + str(queryCount))
            #     queryPrint = 1
            if(curr[v] == 'A' and first == 0):
                print("A: ",end = "")
                print(j+1, end = " ")
                first = 1
                # noNew = 0
            elif(key[i] == curr[v]): #need to write function for A
                print(key[i] + ": " + val[i], end = " ")
                # print("1")
                # noNew = 0
            elif(curr[v] == 'Z'):
                if(first == 0):
                    print("A: ",end = "")
                    print(j+1, end = " ")
                    first = 1
                    print(key[i] + ": " + val[i], end = " ")
                    # print("2")
                    # noNew = 0
                else:
                    print(key[i] + ": " + val[i], end = " ")
                    # print("3")
                    # noNew = 0
            else:                   # should be if letter is not in document
            # this was giving me spacing errors except for this case
                if(curr[v]!=key[i] and printingLine[1]=='Y' and printingLine[2]!='A'):
                    noNew = 1

    if(noNew!=1 or printingLine[len(printingLine) - 1] == 'T S'):
        print("")

try:

    queryCount = 0
    # opens data file and splits by line
    data = open('data.txt', 'rt')
    line = data.read().splitlines()


    createCollections(line)

    # opens command file and splits into list of queries
    final = open('final.txt', 'rt')
    queries = final.read().strip()
    query = queries.split(' ;')


    # ensures that there are is empty query at the end
    if query[len(query)-1] == "":
        query.pop()

    # make sure queries dont start with new line
    for i in range(len(query)):
       if "\n" in query[i][0]:
           query[i] = query[i][1:]


    findCommand(query)

    data.close()
    final.close()

except:
    print("ERROR")
