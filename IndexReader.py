import os
import time

import  ReadCompressed
from Dictionary import Dictioary
class IndexReader:
    def __init__(self, dir):
        """Creates an IndexReader which will read from the given directory
        dir is the name of the directory in which all index files are located."""
        ent = os.listdir(dir)
        #print(ent)
        self.indexer = dir + "/" + ent[0]
        self.dic = ReadCompressed.getDic(self.indexer)
        self.freq = ReadCompressed.freq_read(self.indexer)
        self.posting_list_loc = ReadCompressed.get_postingList_location(self.indexer)
        self.posting_freq_loc = ReadCompressed.get_postingList_freq_location(self.indexer)
        posting_list_locate = []


        f7 = open(self.indexer + '/filesC', "r+b")
        ss = f7.seek(0)
        t = 1
        i = 0
        n = int.from_bytes(bytes(f7.read(1)), "big")
        while i < 1:
            s = 0
            while n < 128:
                s += n
                s = s * 128
                n = int.from_bytes(bytes(f7.read(1)), "big")
            s += (n - 128)
            posting_list_locate.append(s)
            n = int.from_bytes(bytes(f7.read(1)), "big")
            i += 1
        k = 1
        while k < len(posting_list_locate):
            posting_list_locate[k] += posting_list_locate[k - 1]
            k += 1
        f7.close()
        self.filesC = posting_list_locate[0]




    def getTokenFrequency(self, token):
        """Return the number of documents containing a given token (i.e., word)
        Returns 0 if there are no documents containing this token"""
        i =ReadCompressed.getTermIndex(self.dic,token) -1
        if i ==-1:
            return 0
        return self.freq[i]


    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given token (i.e., word) appears in the whole collection.
        Returns 0 if there are no documents containing
        this token"""
        i = ReadCompressed.getTermIndex(self.dic,token) -1
        if i ==-1:
            return 0
        sum = 0
        place = self.posting_freq_loc[i]
        posting_freq = ReadCompressed.get_posting_freqList_(self.indexer, place,self.freq[i])
        for i in posting_freq:
            sum += i

        return sum


    def getDocsWithToken(self, token):
        """Returns a series of integers of the form id- 1, freq-1, id-2, freq-2, ... such
        that id-n is the n-th document containing the given token and freq-n is the
        number of times that the token appears in doc id-n
        Note that the integers should be sorted by id. Returns an empty Tuple if there are no documents containing this token"""
        i = ReadCompressed.getTermIndex(self.dic,token) -1
        if i <= -1:
            return ()
        place_posting = self.posting_list_loc[i]
        place = self.posting_freq_loc[i]
        posting_list = ReadCompressed.get_postingList_(self.indexer,place_posting,self.freq[i])
        posting_freq = ReadCompressed.get_posting_freqList_(self.indexer, place, self.freq[i])
        list_t = []
        k = 0
        while k < len(posting_freq):
            list_t.append((posting_list[k],posting_freq[k]))
            k += 1
        return list_t


    def getNumberOfDocuments(self):
        """Return the number of documents in the
        collection"""
        return self.filesC







start_time = time.time()
t = IndexReader("Test")

print(t.getTokenFrequency("zealand"))

print(t.getDocsWithToken("zealand"))
print(t.getNumberOfDocuments())
print(t.getTokenCollectionFrequency("zealand"))

print("--- %s seconds ---" % (time.time() - start_time))

