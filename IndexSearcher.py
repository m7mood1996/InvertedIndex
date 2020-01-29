import math
import time
from _operator import itemgetter

from IndexReader import IndexReader


def find_min_index(query_list):
    min1 = query_list[0][0]
    min1_index = 0
    i = 1
    while i < len(query_list):
        if min1 > query_list[i][0]:
            min1 = query_list[i][0]
            min1_index = i
        i += 1
    return min1_index


# Merges two subarrays of arr[].
# First subarray is arr[l..m]
# Second subarray is arr[m+1..r]
def merge(arr, l, m, r, arr2, arr3):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    L2 = [0] * (n1)
    L3 = [0] * (n1)
    R = [0] * (n2)
    R2 = [0] * (n2)
    R3 = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
        L2[i] = arr2[l + i]
        L3[i] = arr3[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
        R2[j] = arr2[m + 1 + j]
        R3[j] = arr3[m + 1 + j]

        # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            arr2[k] = L2[i]
            arr3[k] = L3[i]
            i += 1
        else:
            arr[k] = R[j]
            arr2[k] = R2[j]
            arr3[k] = R3[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        arr2[k] = L2[i]
        arr3[k] = L3[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        arr2[k] = R2[j]
        arr3[k] = R3[j]
        j += 1
        k += 1


# l is for left index and r is right index of the
# sub-array of arr to be sorted
def mergeSort(arr, l, r, arr2, arr3):
    if l < r:
        # Same as (l+r)/2, but avoids overflow for
        # large l and h
        m = int((l + (r - 1)) / 2)

        # Sort first and second halves
        mergeSort(arr, l, m, arr2, arr3)
        mergeSort(arr, m + 1, r, arr2, arr3)
        merge(arr, l, m, r, arr2, arr3)

    # Driver code to test above


# This code is contributed by Mohit Kumra


def intersect(list1, list2):
    i = 0
    j = 0
    list3 = []
    while i < len(list1) and j < len(list2):
        if list1[i][0] == list2[j][0]:
            list3.append(list1[i])

            i += 1
            j += 1
        elif list1[i][0] > list2[j][0]:
            j += 1
        else:
            i += 1
    return list3


def binarySearch(arr, l, r, x):
    # Check base case
    if r >= l:

        mid = int(l + (r - l) / 2)

        # If element is present at the middle itself
        if arr[mid][0] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid][0] > x:
            return binarySearch(arr, l, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)

    else:
        # Element is not present in the array
        return -1





def find_from_all_lists(param, posting_lists):
    list_po = []
    sum =0
    for item in posting_lists:
        num =1+math.log(item[binarySearch(item, 0, len(item), param)][1], 10)
        list_po.append(num)
        sum += num * num
    #print(list_po)
    return list_po, math.sqrt(sum)


def getScore(doc_wt, query_nlize,doc_wt_normal_var):
    score = 0
    i=0
    while i < len(doc_wt):
        score += (doc_wt[i]/doc_wt_normal_var) * query_nlize[i]
        i += 1
    return score


class IndexSearcher:
    def __init__(self, iReader):
        """Constructor.
    iReader is the IndexReader object on which the search should be performed"""
        self.ireader = iReader
        self.num_of_doc = iReader.getNumberOfDocuments()

    def vectorSpaceSearch(self, query, k):
        """Returns a tupple containing the id-s of the k most highly ranked reviews for the given query,
        using the vector space ranking function lnn.ltc (using the SMART notation). The id-s should be sorted by the ranking."""
        query_list = []
        term_query_freq = []
        data = ""
        for char in query:  # O(n)
            if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                data = data + char
            elif len(data) == 0:
                continue
            else:
                # self.addTokenToIndex((data.lower(), i))
                if data == 'AND':
                    data = ""
                else:
                    p = data.lower()
                    if p in query_list:
                        term_query_freq[query_list.index(p)] += 1
                        data = ""
                    else:
                        query_list.append(p)
                        term_query_freq.append(1)
                        data = ""
        p = data.lower()
        if p in query_list:
            term_query_freq[query_list.index(p)] += 1
        else:
            query_list.append(p)
            term_query_freq.append(1)
        #print(query_list)
        #print(term_query_freq)
        term_doc_freq = []
        for item in query_list:
            term_doc_freq.append(self.ireader.getTokenFrequency(item))
        #print(term_doc_freq)
        n = len(query_list)
        mergeSort(term_doc_freq, 0, n - 1, query_list, term_query_freq)
        #print(query_list)
        #print(term_query_freq)
        #print(term_doc_freq)

        f = 1

        query_nlize = self.get_nlize(term_query_freq, term_doc_freq)

        posting_lists = []
        for item in query_list:
            posting_lists.append(self.ireader.getDocsWithToken(item))

        temp = posting_lists[0]
        #print(temp)
        while f < len(query_list) and len(temp) != 0:
            # return the intersect between all the posting lists from the
            # smallest to the longest
            temp = intersect(temp, posting_lists[f])
            f += 1

        list_t = {}

        for item in temp:
            f = find_from_all_lists(item[0], posting_lists)
            list_t[item[0]] = getScore(f[0], query_nlize, f[1])

        """
        for key in list_t.keys():
            list_t[key] = getScore(list_t[key], query_nlize)"""
        list_t = list({s: v for s,v in sorted(list_t.items(), key=itemgetter(1))}.keys())
        list_t.reverse()

        #print((list_t.items()))

        #print(temp)
        return list_t[0:k]





    def get_nlize(self, tf, df):
        wtds = []  # each term in query has a wt
        sum = 0
        i = 0
        nlize = []
        while i < len(tf):
            wtd = (1 + math.log(tf[i], 10)) * math.log(self.num_of_doc / df[i], 10)
            wtds.append(wtd)  # length
            sum += wtd * wtd
            i += 1
        doc_len = math.sqrt(sum)
        for item in wtds:
            nlize.append(item / doc_len)
        return nlize  # wt normaled


start_time = time.time()
t = IndexReader("Test")
"""
print(t.getTokenFrequency("a"))
print(t.getDocsWithToken("a"))
print(t.getTokenCollectionFrequency("a"))
"""
indexSerarcher = IndexSearcher(t)
indexSerarcher.vectorSpaceSearch("a is a about", 10)

print("--- %s seconds ---" % (time.time() - start_time))
