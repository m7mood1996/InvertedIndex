import os
import shutil

import sys

import psutil as psutil

import CompressFile
import FileMerge
import time

start_time = time.time()
from Dictionary import Dictioary

MAX_Size = 1500000


class IndexWriter:
    def __init__(self, inputFile, dir):
        self.database = dict()
        self.dir = dir

        """Given a collection of documents, creates an on disk index
        inputFile is the path to the file containing the review data (the path includes the filename itself)
        dir is the name of the directory in which all index files will be created
        if the directory does not exist, it should be created"""
        os.makedirs(dir)
        self.CreatIndex(inputFile)

    def removeIndex(self, dir):
        """Delete all index files by removing the given directory
        dir is the name of the directory in which all index files are located. After removing the files, the directory should be deleted."""
        self.database = None
        self.dir = None
        shutil.rmtree(dir)
    """
    def addTokenToIndex(self, param):
        if param[0] in self.database:
            if self.database[param[0]][1][-1][0] == param[1]:
                self.database[param[0]][1][-1] = (param[1], self.database[param[0]][1][-1][1] + 1)
            else:
                self.database[param[0]][1].append((param[1], 1))
                self.database[param[0]] = (self.database[param[0]][0] + 1, self.database[param[0]][1])
        else:
            self.database[param[0]] = (1, list())
            self.database[param[0]][1].append((param[1], 1))"""

    def tokanization(self, file, i):  # O(n)
        data = ""
        for char in file:  # O(n)
            if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                data = data + char
            elif len(data) == 0:
                continue
            else:
                #self.addTokenToIndex((data.lower(), i))
                p = data.lower()

                if p in self.database:
                    if self.database[p][1][-1][0] == i:
                        self.database[p][1][-1] = (i, self.database[p][1][-1][1] + 1)
                    else:
                        self.database[p][1].append((i, 1))
                        self.database[p] = (self.database[p][0] + 1, self.database[p][1])
                else:
                    self.database[p] = (1, [])
                    self.database[p][1].append((i, 1))
                data = ""

    def CreatIndex(self, inputFile):

        f = open(inputFile, "r")
        temp = f.readline()
        temp = ' '
        i = 0
        size = 0
        k = 1
        while temp:
            file = ""  # each time has a file
            temp = f.readline()
            size += len(temp.encode('utf-8'))
            while temp != '*' * 80 + '\n':
                if not temp:
                    break
                if temp == "*" * 80 + '\n':
                    break
                file = file + temp
                temp = f.readline()
            i += 1
            self.tokanization(file, i)
            if size >= 1147400000:  # number of bytes allowed to get from inputfile at the same time 2GB
                # print(i)
                name = self.dir + "/Temp" + str(k)
                os.mkdir(name)
                if __name__ == '__main__':
                    CompressFile.compressIndex(name, self.database.items())
                self.database.clear()
                file = " "
                size = 0
                k += 1
        # print(i)
        del file
        name = self.dir + "/Temp" + str(k)
        # output = open(name, "w")
        os.mkdir(name)
        size = 0
        k += 1
        print("--- %s seconds ---" % (time.time() - start_time))
        #print((self.database))
        if __name__ == '__main__':
            CompressFile.compressIndex(name, self.database.items())
        self.database.clear()
        if __name__ == '__main__':
            FileMerge.first_call_merge(self.dir)
        entries = os.listdir(self.dir)
        if '.DS_Store' in entries:
            entries.remove('.DS_Store')
        f10 = open(self.dir + "/" + entries[0] + "/filesC", "w+b")
        k = CompressFile.getEncode([i])
        f10.write(k)
        f10.close()

        # print(size)
        f.close()

print("PID = ", os.getpid())

t = IndexWriter("100.txt", "Test")
print("--- %s seconds ---" % (time.time() - start_time))
print(sys.getsizeof(t))
# for it in t.database.items():
#    print(it)

print("--- %s seconds ---" % (time.time() - start_time))
#t.removeIndex("first")
