import os.path
import json
import shutil

import CompressFile
from Dictionary import Dictioary
import ReadCompressed
from multiprocessing import Process
from PostingList import PostingList

BLK = 1

def list_sort(test_list1, test_list2, first_list_freq, sec_list_freq):
    size_1 = len(test_list1)
    size_2 = len(test_list2)

    res = []
    res_freq = []
    i, j = 0, 0

    while i < size_1 and j < size_2:
        if test_list1[i] < test_list2[j]:
            res.append(test_list1[i])
            res_freq.append(first_list_freq[i])
            i += 1

        else:
            res.append(test_list2[j])
            res_freq.append(sec_list_freq[j])
            j += 1

    res = res + test_list1[i:] + test_list2[j:]
    res_freq = res_freq + first_list_freq[i:] + sec_list_freq[j:]
    return (res, res_freq)


def getTerms(dic):
    Terms = []
    for item in dic.arr:

        j = 0
        while j < BLK + 1:
            if j == 0:
                k = item[j]
            else:
                Terms.append(dic.dic[k: k + item[j]])
                # print(dic.dic[k: k +item[j]])
                k += item[j]
            j += 1
        # print("\n")
    i = 0
    while i < BLK:
        if Terms[-BLK + i] < Terms[-BLK - 1 + i]:
            Terms.pop(-BLK + i)
        i += 1
    return Terms


def getEncode(docIDs):
    byteStream = bytearray()
    for ID in docIDs:
        idEncode = getVariantEncode(ID)

        byteStream.extend(idEncode)

    return byteStream

def getVariantEncode( ID):
    byteStream = bytearray()
    while True:
        byteStream.insert(0, ID % 128)
        if ID < 128:
            break
        ID //= 128
    byteStream[len(byteStream) - 1] += 128
    return byteStream


def buildV(list_t):
    i = 1
    while i < len(list_t):
        list_t[i] -= list_t[i-1]
        i += 1
    return getEncode(list_t)


def addPostingList(from_index, fromfile, tofiles, i,posting_freq1_index1):
    from_ = open(fromfile + "/postingList", 'r+b')
    tofile = open(tofiles + "/postingList", "a+b")

    from_freq = open(fromfile + "/posting_freq_List", 'r+b')
    tofile_freq = open(tofiles + "/posting_freq_List", "a+b")

    start = from_index[i]
    start_freq = posting_freq1_index1[i]
    if len(from_index) <= i + 1:
        from_.seek(start, 0)
        n = from_.read()
        from_freq.seek(start_freq,0)
        n_freq = from_freq.read()
    else:
        stop = from_index[i + 1]
        stop_freq = posting_freq1_index1[i+1]
        from_.seek(start, 0)
        from_freq.seek(start_freq, 0)
        n = from_.read(stop - start)
        n_freq = from_freq.read(stop_freq-start_freq)
    k = tofile.seek(0, os.SEEK_END)
    k_freq = tofile_freq.seek(0,os.SEEK_END)
    tofile.write(n)
    tofile_freq.write(n_freq)
    from_freq.close()
    from_.close()
    tofile.close()
    tofile_freq.close()
    return (k,k_freq)


def mergeTwoPostingList(firspostingListFile, secPostingListFile, name, i, j, posting_index1, posting_index2, freq1,
                        freq2, posting_freq1_index1, posting_freq2_index2):

    tofile = open(name + "/postingList", "a+b")
    tofile_freq = open(name + "/posting_freq_List", "a+b")
    start1 = posting_index1[i]
    start2 = posting_index2[j]

    start1_freq = posting_freq1_index1[i]
    start2_freq = posting_freq2_index2[j]

    first_list_freq = ReadCompressed.get_posting_freqList_(firspostingListFile, start1_freq, freq1)
    sec_list_freq = ReadCompressed.get_posting_freqList_(secPostingListFile, start2_freq, freq2)
    first_list = ReadCompressed.get_postingList_(firspostingListFile, start1, freq1)

    sec_list = ReadCompressed.get_postingList_(secPostingListFile, start2, freq2)
    tupleS = list_sort(first_list, sec_list, first_list_freq, sec_list_freq)
    list3 = tupleS[0]
    list3_freq = tupleS[1]

    k = tofile.seek(0, os.SEEK_END)
    k_freq = tofile_freq.seek(0,os.SEEK_END)
    #print(list3)
    # tofile.write(bytearray(CompressFile.buildGV(list3)))
    tofile.write(CompressFile.buildV_temp(list3))
    tofile_freq.write(CompressFile.getEncode(list3_freq))
    tofile_freq.close()
    tofile.close()
    return (k,k_freq)

def processDic(name,dic):
    dic_file = open(name + "/dic", "w")
    dic_file.write(dic)
    dic_file.close()

def processArr(name,arr):
    dic_file = open(name + "/arr", "w+b")
    arrByteArray = bytearray()
    for i in arr:
        arrByteArray.extend(getEncode(i))
    dic_file.write(arrByteArray)
    dic_file.close()

def processFreq(name,freq3):
    dic_file = open(name + "/freqs", "w+b")
    dic_file.write(CompressFile.getEncode(freq3))
    dic_file.close()

def processPostingLocation(name,posting_index3):
    dic_file = open(name + "/postingListLocate", "w+b")
    dic_file.write(CompressFile.buildV_temp(posting_index3))
    dic_file.close()

def processFreqLoc(name, posting_freq3_index3):
    dic_file = open(name + "/posting_freq_ListLocate", "w+b")

    dic_file.write(CompressFile.buildV_temp(posting_freq3_index3))
    dic_file.close()


def processDic(name,dic):
    dic_file = open(name + "/dic", "w")
    dic_file.write(dic)
    dic_file.close()

def processArr(name,arr):
    dic_file = open(name + "/arr", "w+b")
    arrByteArray = bytearray()
    for i in arr:
        arrByteArray.extend(getEncode(i))
    dic_file.write(arrByteArray)
    dic_file.close()

def processFreq(name,freq3):
    dic_file = open(name + "/freqs", "w+b")
    dic_file.write(CompressFile.getEncode(freq3))
    dic_file.close()

def processPostingLocation(name,posting_index3):
    dic_file = open(name + "/postingListLocate", "w+b")
    dic_file.write(CompressFile.buildV_temp(posting_index3))
    dic_file.close()

def processFreqLoc(name, posting_freq3_index3):
    dic_file = open(name + "/posting_freq_ListLocate", "w+b")

    dic_file.write(CompressFile.buildV_temp(posting_freq3_index3))
    dic_file.close()




def Merge_Files(myDir, par1,par2,k):
    entries = [par1, par2]
    #myDir = 'Tempfiles/'
    e = os.listdir(myDir)
    if '.DS_Store' in e:
        e.remove('.DS_Store')
    #k = len(e) + 1
    #print(entries)


    #print(entries)

    name = myDir + "/Temp" + str(k)
    os.mkdir(name)
    dic1 = ReadCompressed.getDic(myDir + "/" + entries[0])
    dic2 = ReadCompressed.getDic(myDir + "/" + entries[1])
    Terms1 = getTerms(dic1)
    dic1 = None
    Terms2 = getTerms(dic2)
    dic2 = None
    freq1 = ReadCompressed.freq_read(myDir + "/" + entries[0])

    freq2 = ReadCompressed.freq_read(myDir + "/" + entries[1])

    posting_index1 = ReadCompressed.get_postingList_location(myDir + "/" + entries[0])
    posting_freq1_index1 =ReadCompressed.get_postingList_freq_location(myDir + "/" + entries[0])
    posting_index2 = ReadCompressed.get_postingList_location(myDir + "/" + entries[1])
    posting_freq2_index2 =ReadCompressed.get_postingList_freq_location(myDir + "/" + entries[1])
    i = 0
    j = 0
    Terms3 = []
    freq3 = []
    posting_index3 = []
    posting_freq3_index3 = []
    while i < len(Terms1) and j < len(Terms2):
        if Terms1[i] < Terms2[j]:
            Terms3.append(Terms1[i])
            freq3.append(freq1[i])
            # read from posting_index1[i] to posting_index1[i+1] then write it to posting_index3[lenofit]
            tupleS = addPostingList(posting_index1, myDir + "/" + entries[0], name, i ,posting_freq1_index1)
            posting_index3.append(tupleS[0])
            posting_freq3_index3.append(tupleS[1])
            i += 1
        elif Terms1[i] > Terms2[j]:
            Terms3.append(Terms2[j])
            freq3.append(freq2[j])
            tupleS = addPostingList(posting_index2, myDir + "/" + entries[1], name, j,posting_freq2_index2)
            posting_index3.append(tupleS[0])
            posting_freq3_index3.append(tupleS[1])
            j += 1
        else:
            Terms3.append(Terms1[i])
            freq3.append(freq1[i] + freq2[j])
            tupleS = mergeTwoPostingList(myDir + "/" + entries[0], myDir + "/" + entries[1], name, i, j, posting_index1,posting_index2, freq1[i], freq2[j],posting_freq1_index1,posting_freq2_index2)
            posting_index3.append(tupleS[0])
            posting_freq3_index3.append(tupleS[1])
            i += 1
            j += 1
    while i < len(Terms1):
        Terms3.append(Terms1[i])
        freq3.append(freq1[i])
        # read from posting_index1[i] to posting_index1[i+1] then write it to posting_index3[lenofit]
        tupleS = addPostingList(posting_index1, myDir + "/" + entries[0], name, i, posting_freq1_index1)
        posting_index3.append(tupleS[0])
        posting_freq3_index3.append(tupleS[1])
        i += 1
    while j < len(Terms2):
        Terms3.append(Terms2[j])
        freq3.append(freq2[j])
        tupleS = addPostingList(posting_index2, myDir + "/" + entries[1], name, j, posting_freq2_index2)
        posting_index3.append(tupleS[0])
        posting_freq3_index3.append(tupleS[1])
        j += 1


    shutil.rmtree(myDir + "/" + entries[0])

    shutil.rmtree(myDir + "/" + entries[1])

    dic3 = Dictioary(Terms3, ("BLK", BLK))

    proDic = Process(target=processDic, args=(name, dic3.dic))

    """
    dic_file = open(name + "/dic", "w")
    dic_file.write(dic3.dic)
    dic_file.close()"""
    proArr = Process(target=processArr,args=(name,dic3.arr))
    """
    dic_file = open(name + "/arr", "w+b")
    arrByteArray = bytearray()
    for i in dic3.arr:
        arrByteArray.extend(getEncode(i))
    dic_file.write(arrByteArray)
    dic_file.close()"""
    profreq = Process(target=processFreq,args=(name,freq3))
    """
    dic_file = open(name + "/freqs", "w+b")
    dic_file.write(CompressFile.getEncode(freq3))
    dic_file.close()"""
    proPostingLoc = Process(target=processPostingLocation,args=(name,posting_index3))
    """
    dic_file = open(name + "/postingListLocate", "w+b")

    dic_file.write(CompressFile.buildV_temp(posting_index3))
    dic_file.close()"""
    proFreqLoc = Process(target=processFreqLoc, args=(name,posting_freq3_index3))
    """
    dic_file = open(name + "/posting_freq_ListLocate", "w+b")

    dic_file.write(CompressFile.buildV_temp(posting_freq3_index3))
    dic_file.close()"""
    proDic.start()
    proArr.start()
    profreq.start()
    proPostingLoc.start()
    proFreqLoc.start()

    proDic.join()
    proArr.join()
    profreq.join()
    proPostingLoc.join()
    proFreqLoc.join()

    del posting_index1
    del posting_index2
    del posting_index3
    del dic3
    del dic1
    del dic2
    del Terms1
    del Terms2
    del Terms3
    del freq3
    del freq1
    del freq2
    k += 1


    entries = os.listdir(myDir)
    if '.DS_Store' in entries:
        entries.remove('.DS_Store')



def first_call_merge(myDir):
    entries = os.listdir(myDir)
    if '.DS_Store' in entries:
        entries.remove('.DS_Store')
    k =len(entries)
    #print(entries)
    while len(entries) != 1:
        if len(entries) > 3:
            p1 = Process(target=Merge_Files, args=(myDir, entries[0], entries[1],k+1),)
            p2 = Process(target=Merge_Files, args=(myDir, entries[2], entries[3],k+2))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            k+=2
        elif len(entries) >= 2:
            Merge_Files(myDir, entries[0], entries[1],k+1)
            k+=1

        entries = os.listdir(myDir)
        if '.DS_Store' in entries:
            entries.remove('.DS_Store')
        #print(entries)
