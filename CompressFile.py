import time

from Dictionary import Dictioary
from PostingList import PostingList
import math
from multiprocessing import Process
start_time = time.time()
BLK = 1


def buildGV( DocIDs):
    docList = []

    while len(DocIDs) % 4 != 0:
        DocIDs.append(0)
    sp = int(len(DocIDs) / 4)
    while len(DocIDs) - 4 >= 0:
        k = DocIDs[len(DocIDs) - 4:len(DocIDs)]
        DocIDs = DocIDs[0:len(DocIDs) - 4]
        list = []
        j = len(k) - 1
        gLength = 0
        while j >= 0:

            item = k[j]
            if item < 0:
                item = 0
            if (128 * 128 * 128 * 128) > item >= (128 * 128 * 128):
                i = 3
            elif (128 * 128 * 128) > item >= (128 * 128):
                i = 2
            elif 128 * 128 > item >= 128:
                i = 1
            else:
                i = 0
            if j == 0:
                gLength += int(i * (math.pow(2, 6)))
            elif j == 1:
                gLength += int(i * (math.pow(2, 4)))
            elif j == 2:
                gLength += int(i * (math.pow(2, 2)))
            else:
                gLength += i
            j -= 1

            if i == 0:
                list.insert(0, item)
            elif i == 1:
                b_6 = int(item / 128)
                m_6 = item % 128

                list.insert(0, m_6 + 128)
                list.insert(0, b_6)
            elif i == 2:
                b_6 = int(item / (128 * 128))
                m_6 = item % (128 * 128)
                b_7 = int(m_6 / 128)
                m_7 = m_6 % 128

                list.insert(0, m_7 + 128)
                list.insert(0, b_7 + 128)
                list.insert(0, b_6)
            else:
                b_7 = int(item / (128 * 128 * 128))  # 1
                m_7 = item % (128 * 128 * 128)
                b_7_2 = int(m_7 / (128 * 128))  # 2
                m_7_2 = m_7 % (128 * 128)
                b_7_3 = int(m_7_2 / 128)  # 3
                m_7_3 = m_7_2 % 128

                list.insert(0, m_7_3 + 128)
                list.insert(0, b_7_3 + 128)
                list.insert(0, b_7_2 + 128)
                list.insert(0, b_7)

        list.insert(0, gLength)

        docList = list + docList
    return docList

def buildV_noGaps(DocIDs):
    docList = []
    j = len(DocIDs) - 1;
    while j >= 0:
        i = 0
        list = []
        while DocIDs[j] >= 128:
            temp = int(DocIDs[j] / 128)
            temp2 = DocIDs[j] - temp * 128
            list.insert(len(list) - i, temp2)
            DocIDs[j] = temp
            i += 1
        list.insert(0, DocIDs[j])
        list[len(list) - 1] = 128 + list[len(list) - 1]
        j -= 1
        docList = list + docList
    return docList


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


def buildV_temp(list_t):
    i= len(list_t) -1
    while i > 0:
        list_t[i] -= list_t[i-1]
        i -= 1
    return getEncode(list_t)

def process_5(dir,postings_listByteArray):
    f5 = open(dir + "/postingList", "a+b")
    f5.write(postings_listByteArray)
    f5.close()
    pass

def process_7(dir,posting_freq_listByteArray ):
    f7 = open(dir + "/posting_freq_List", "a+b")
    f7.write(posting_freq_listByteArray)
    f7.close()
    pass

def process_6(dir,postings_list_locating ):
    f6 = open(dir + "/postingListLocate", "w+b")
    f6.write(getEncode(postings_list_locating))
    f6.close()

def process_8(dir,posting_freq_list_Locating):
    f8 = open(dir + "/posting_freq_ListLocate", "w+b")
    f8.write(getEncode(posting_freq_list_Locating))
    f8.close()
def compressIndex(dir,databaseItemes):

    terms = []
    freqs = []
    postings_list = []
    posting_freq_list = []
    postings_list_locating = [0]
    start_time = time.time()


    postings_listByteArray = bytearray()
    posting_freq_listByteArray = bytearray()
    posting_freq_list_Locating = [0]

    for key, value in sorted(databaseItemes):
        terms.append(str(key))
        freqs.append(value[0])
        list_t = value[1]
        pos_temp = []
        pos_fre_temp = []

        for item in list_t:
            pos_temp.append(item[0])
            pos_fre_temp.append(item[1])

        k = buildV_temp(pos_temp)
        k2 = getEncode(pos_fre_temp)
        postings_listByteArray.extend(k)
        posting_freq_listByteArray.extend(k2)

        postings_list_locating.append(len(k))
        posting_freq_list_Locating.append(len(k2))

    print("after writing",  round((time.time() - start_time), 5))
    p5 = Process(target=process_5,args=(dir,postings_listByteArray ))
    p7 = Process(target=process_7,args=(dir,posting_freq_listByteArray ))
    p6 = Process(target=process_6, args=(dir, postings_list_locating))
    p8 = Process(target=process_8, args=(dir, posting_freq_list_Locating))

    p5.start()
    p6.start()
    p7.start()
    p8.start()



    #f5 = open(dir + "/postingList", "a+b")
    #f7 = open(dir + "/posting_freq_List", "a+b")
    #f5.write(postings_listByteArray)
    #f7.write(posting_freq_listByteArray)


    #f6 = open(dir + "/postingListLocate", "w+b")
    #f6.write(getEncode(postings_list_locating))
    #f8 = open(dir + "/posting_freq_ListLocate", "w+b")
    #f8.write(getEncode(posting_freq_list_Locating))

    start_time = time.time()
    #print(terms)
    #print(freqs)
    #print(postings_list)
    #print(posting_freq_list)
    listT = []
    dic = Dictioary(terms, ("BLK", BLK))
    f2 = open(dir + '/dic', 'w')
    f2.write(dic.dic)
    f3 = open(dir + '/arr', 'w+b')
    # f3.write(dic.arr)
    #print(dic.arr)

    arrByteArray = bytearray()
    for i in dic.arr:
        while len(i) < BLK+1:
            i =  i + (0,)
        arrByteArray.extend(getEncode(i))
    f4 = open(dir + "/freqs", "w+b")
    f3.write(arrByteArray)
    f4.write(getEncode(freqs))

    print("arr writing",  round((time.time() - start_time), 5))

    postings_list_locating = [0]
    posting_freq_list_Locating = [0]
    temp = 0

    p5.join()
    p6.join()
    p7.join()
    p8.join()

    """
    i = 0
    while i < len(postings_list):
        k = buildV(postings_list[i])
        k2 = buildV_noGaps(posting_freq_list[i])
        f5.write(bytearray(k))
        f7.write(bytearray(k2))
        postings_list_locating.append(len(k) + postings_list_locating[-1])
        posting_freq_list_Locating.append(len(k2) + posting_freq_list_Locating[-1])
        i += 1
    """

    f2.close()
    f3.close()
    f4.close()
    #f5.close()
    #f6.close()
    #f7.close()
    #f8.close()

"""
f1 = open("Temp1", 'r')
t = f1.readline()

terms = []
freqs = []
postings_list = []
while t:
    t_list = t.split(" ", 2)
    terms.append(t_list[0])
    freqs.append(int(t_list[1]))
    postings_list.append(eval(t_list[2]))
    t = f1.readline()
print(postings_list)
print(terms)
print(freqs)
print("hello")
BLK =4
listT = []
dic = Dictioary(terms, ("BLK", BLK))
f2 = open('Tempfiles/dic', 'w')
f2.write(dic.dic)
f3 = open('Tempfiles/arr', 'w+b')
# f3.write(dic.arr)
print(dic.arr)
for i in dic.arr:

    if len(i) <BLK +1:
        listT = list(i)
        while len(listT)<BLK+1:
            listT.append(listT[-1])
        i = tuple(listT)
    f3.write(bytearray(buildGV(list(i))))


#for freqs

f4 = open("Tempfiles/freqs","w+b")
f4.write(bytearray(buildGV(list(freqs))))



#for postinglist
f5 = open("Tempfiles/postingList","a+b")
postings_list_locating = [0]

for i in postings_list:
    k = PostingList(i,"GV").Docs
    f5.write(PostingList(i,"GV").Docs)
    postings_list_locating.append(len(k) + postings_list_locating[-1])
f6 = open("Tempfiles/postingListLocate","wb")
print(postings_list_locating)
f6.write(PostingList(postings_list_locating,"V").Docs)
f1.close()
f2.close()
f3.close()
f4.close()
f6.close()

"""
