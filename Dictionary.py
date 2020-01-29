def findpre(a, b):
    i = 0;
    while (i < len(a) and i < len(b)):
        if a[i] != b[i]:
            break
        i += 1
    return i


class Dictioary:
    def __init__(self, TermList = "", type = " "):
        """Given sorted list of terms, creates a data structure which holds a compressed dictionary
        TermList is the sorted list of terms Type is one of the following tupples: ("STR"), ("BLK", k),
         ("FC", k) where k is the size of the block"""

        self.dic = ""
        self.type = type
        self.arr = []

        if type == "STR":  # dictionary-as-a-string
            self.buildDic(TermList)
        elif type[0] == "BLK":  # Blocking
            self.buildBLKdic(TermList)
        elif type[0] == "FC":
            self.buildFCdic(TermList)
        return


    def GetString(self):
        """Returns the dictionary's string"""
        if self.type == "STR" or self.type[0] == "BLK":
            return self.dic
        elif self.type == "FC":
            pass

    def GetInfo(self, term):
        """ Returns relevant data about term.For "STR" it returns the location of the termin the string
        For "BLK" it returns a tuple containing the location of the container block and the lengths of its
        terms For "FC" it returns a tuple containing the location of the container block and pairs containing the lengths and prefixes sizes of its terms"""

        if self.type == "STR":

            f = self.binarySearch(0, len(self.arr) - 1, term)
            if (f == -1):
                return ("string not found in this dic")
            else:
                return (self.arr[f])
        elif self.type[0] == "BLK":

            f = self.binarySearchBLK(0, len(self.arr) - 1, term)
            if (f == -1):
                last = self.arr[-1]
                #print(last)
                t=0
                sum =0;
                while t <len(last)-1:
                    sum += last[t]
                    termlast = self.dic[sum:sum + last[t+1]]
                    #print(termlast)
                    t +=1
                    if term == termlast:
                        return last

                return -1 #("string not found in this dic")

            else:
                return (self.arr[f])

        elif self.type[0] == "FC":
            f = self.binarySearchFC(0, len(self.arr) - 1, term)
            if (f == -1):
                return ("string not found in this dic")
            else:
                return self.arr[f]

    def buildDic(self, TermList):  # ￼￼￼dictionary-as-a-string
        i = 0

        for item in TermList:
            self.arr.append(len(self.dic))
            self.dic += item
            i += 1

        return

    def buildBLKdic(self, TermList):
        k = self.type[1]
        i = 0
        j = 0
        t = []
        s = 0
        for item in TermList:

            if j == 0:
                t.append(len(self.dic))
                s = len(self.dic)
                j += 1
            elif j <= k:
                re = 0
                for ite in t:
                    re += ite

                t.append(len(self.dic) - re)
                j += 1
            self.dic += item
            s += len(item)
            if (j == k):
                re = 0
                for ite in t:
                    re += ite

                t.append(len(self.dic) - re)
                tu = tuple(t)
                self.arr.append(tu)
                t = []
                j = 0

            i += 1
        t.append(len(item))
        tu = tuple(t)
        self.arr.append(tu)
        return

    def buildFCdic(self, TermList):
        k = self.type[1]

        j = 0
        newTerms = ""
        prefix = []
        leng =0;
        while j < int(len(TermList)/k):
            temp = []
            i=0
            while i<k:
                if (i + (j * k)) % 4 == 0:
                    newTerms += (TermList[i + (j * k)])
                    if i == 0 and j == 0:
                        leng += len(TermList[i + (j * k)])
                        temp3 = [len (TermList[i + (j * k)]),0]
                    #temp0 = [leng,tuple(temp3)]
                        temp.append(leng)
                        temp.append(tuple(temp3))
                    #print(item)
                    else:
                        temp.append(leng)
                        leng += len(TermList[i + (j * k)])
                        temp3 = [len(TermList[i + (j * k)]), 0]
                        temp.append(tuple(temp3))
                else:
                    x = findpre(TermList[i + (j * k)], TermList[i + (j * k) - 1])

                    temp2 = [len(TermList[i + (j * k)]) , x]
                    temp.append(tuple(temp2))
                    newTerms += (TermList[i + (j * k)][x:])
                    leng += len(TermList[i + (j * k)][x:])
                i += 1
            prefix.append(tuple(temp))

            j += 1
        self.arr = prefix
        self.dic = newTerms

    def binarySearch(self, l, r, x):  # searching for x in Dictioary(self) type of "STR"

        # Check base case
        if r >= l:
            mid = l + int((r - l) / 2)

            # If element is present at the middle itself
            if mid == len(self.arr) - 1 and self.dic[self.arr[mid]:len(self.arr)] == x:
                return mid
            elif mid == len(self.arr) - 1 and self.dic[self.arr[mid]:len(self.arr)] != x:
                return -1
            elif self.dic[self.arr[mid]:self.arr[mid + 1]] == x:
                return mid

            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif self.dic[self.arr[mid]:self.arr[mid + 1]] > x:
                return self.binarySearch(l, mid - 1, x)

            # Else the element can only be present
            # in right subarray
            else:
                return self.binarySearch(mid + 1, r, x)

        else:
            # Element is not present in the array
            return -1

    def binarySearchBLK(self, l, r, x):  # searching for x in Dictioary(self) type of "BLK"
        if r >= l:
            mid = l + int((r - l) / 2)

            # If element is present at the middle itself
            if self.dic[self.arr[mid][0]:self.arr[mid][0] + self.arr[mid][1]] == x:
                return mid

            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif self.dic[self.arr[mid][0]:self.arr[mid][0] + self.arr[mid][1]] > x:

                return self.binarySearchBLK(l, mid - 1, x)

            # Else the element can only be present
            # in right subarray
            else:
                y = self.arr[mid][0]
                i = 1
                while i < self.type[1]+1:

                    if x == self.dic[y:y + self.arr[mid][i]]:
                        return mid
                    y = y + self.arr[mid][i]
                    i += 1
                return self.binarySearchBLK(mid + 1, r, x)

        else:
            # Element is not present in the array
            return -1

    def binarySearchFC (self,l,r,x):
        if r >= l:
            mid = l + int((r - l) / 2)

            # If element is present at the middle itself
            if self.dic[self.arr[mid][0]:self.arr[mid][0] + self.arr[mid][1][0] ] == x:
                return mid

            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif self.dic[self.arr[mid][0]:self.arr[mid][0] + self.arr[mid][1][0]] > x:

                return self.binarySearchFC(l, mid - 1, x)
            # Else the element can only be present
            # in right subarray
            else:
                k = self.type[1] + 1
                y = self.arr[mid][0]
                my_list = []
                i = 0
                for t in self.arr[mid]:
                    if i == 0:
                        my_list.append("")
                        i+= 1;
                        continue
                    if i == 1:
                        size , pre = t
                        my_list.append(self.dic[y:y + size-pre])
                        i += 1
                        y += size-pre
                    else:
                        size, pre = t
                        my_list.append(my_list[i-1][0:pre] + self.dic[y: y +size-pre])
                        y+=size-pre
                        i += 1
                if x in my_list:
                    return mid

                elif x > my_list[len(my_list)-1]:
                    return self.binarySearchFC(mid + 1, r, x)
                else:
                    # Element is not present in the array
                    return -1