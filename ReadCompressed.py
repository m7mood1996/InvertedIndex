import math

from Dictionary import Dictioary

BLK = 1


def isKthBitSet(n, k):
    if n & (1 << (k - 1)):
        return True
    else:
        return False


def extractKBits(num, k, p):
    # convert number into binary first
    binary = bin(num)

    # remove first two characters
    binary = binary[2:]

    end = len(binary) - p
    start = end - k + 1

    # extract k  bit sub-string
    kBitSubStr = binary[start: end + 1]

    # convert extracted sub-string into decimal again
    return (int(kBitSubStr, 2))


def freq_read(dir):
    f4 = open(dir +"/freqs", "r+b")

    # freq read compressed data
    freq = []

    n = int.from_bytes(bytes(f4.read(1)), "big")
    while n:
        s = 0
        while n < 128:
            if n == 0:
                break
            s += n
            s = s * 128
            n = int.from_bytes(bytes(f4.read(1)), "big")
        s += (n - 128)
        freq.append(s)

        n = int.from_bytes(bytes(f4.read(1)), "big")

    f4.close()
    return freq
    """
    # print(int.from_bytes( gropsize,byteorder="big"))
    while gropsize:

        i = 0
        index = 8
        group_size_int = int.from_bytes(gropsize, byteorder="big")

        list = []
        while i < 4:

            if isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # 11 so 4 bytes
                k = bytearray(f4.read(4))
                if isKthBitSet(k[3], 8):
                    k[3] = (k[3] - 128)
                if k[2] % 2 == 1:
                    k[2] = k[2] >> 1
                    k[3] = (k[3] + 128)
                else:
                    k[2] = k[2] >> 1
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if k[1] % 2 == 1:
                    k[1] = k[1] >> 1
                    k[2] = (k[2] + 128)
                else:
                    k[1] = k[1] >> 1
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            elif isKthBitSet(group_size_int, index) and not isKthBitSet(group_size_int, index - 1):  # its 10 so 3 bytes
                k = bytearray(f4.read(3))
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if k[1] % 2 == 1:
                    k[1] = k[1] >> 1
                    k[2] = (k[2] + 128)
                else:
                    k[1] = k[1] >> 1
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            elif not isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # its 01 so 2 bytes
                k = bytearray(f4.read(2))
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            else:  # its only 0 so 1 byte
                first_number = f4.read(1)
                list.append(int.from_bytes(first_number, byteorder="big"))
            i += 1
            index -= 2
        gropsize = f4.read(1)
        # print(list)
        freq = freq + list

    # print(freq)
    f4.close()"""



# uncompress dic.arr data about the terms in the index

def uncompr_index_arr(BLK,dir):  # k is the block size
    f3 = open(dir + '/arr', 'r+b')
    temp_arr = []
    final_arr = []

    i = 0
    n = int.from_bytes(bytes(f3.read(1)), "big")
    while n:
        s = 0
        while n < 128:
            if n == 0:
                break
            s += n
            s = s * 128
            n = int.from_bytes(bytes(f3.read(1)), "big")
        s += (n - 128)
        temp_arr.append(s)
        if len(temp_arr) == BLK+1:
            final_arr.append(tuple(temp_arr))
            temp_arr = []
        n = int.from_bytes(bytes(f3.read(1)), "big")
        i += 1
    f3.close()


    """
    while gropsize:
        i = 0
        index = 8
        group_size_int = int.from_bytes(gropsize, byteorder="big")
        list = []
        while i < 4:

            if isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # 11 so 4 bytes
                k = bytearray(f3.read(4))
                if isKthBitSet(k[3], 8):
                    k[3] = (k[3] - 128)
                if k[2] % 2 == 1:
                    k[2] = k[2] >> 1
                    k[3] = (k[3] + 128)
                else:
                    k[2] = k[2] >> 1
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if k[1] % 2 == 1:
                    k[1] = k[1] >> 1
                    k[2] = (k[2] + 128)
                else:
                    k[1] = k[1] >> 1
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            elif isKthBitSet(group_size_int, index) and not isKthBitSet(group_size_int, index - 1):  # its 10 so 3 bytes
                k = bytearray(f3.read(3))
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[1] = k[1] + 128
                k[0] = k[0] >> 1
                if k[1] % 2 == 1:
                    k[2] = k[2] + 128
                k[1] = k[1] >> 1
                if k[0] % 2 == 1:
                    k[1] = k[1] + 128
                k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            elif not isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # its 01 so 2 bytes
                k = bytearray(f3.read(2))
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            else:  # its only 0 so 1 byte
                first_number = f3.read(1)
                list.append(int.from_bytes(first_number, byteorder="big"))
            i += 1
            index -= 2
        gropsize = f3.read(1)
        index_arr = index_arr + list
        while (len(index_arr) > 2 and index_arr[-1] == 0):
            index_arr.pop(-1)
        if len(index_arr) >= BLK + 1:
            # print(index_arr[0:BLK+1])
            final_arr.append(tuple(index_arr[0:BLK + 1]))
            t = 0
            while t < BLK + 1:
                index_arr.pop(0)
                t += 1

    f3.close()"""
    return final_arr


def getDic(dir):
    fileTerm = open(dir +"/dic")
    d = Dictioary()
    d.dic = fileTerm.read()
    d.arr = uncompr_index_arr(BLK,dir)
    d.type = ("BLK", BLK)
    fileTerm.close()
    return d



def getTermIndex(dic,Term):
    #f6 = open(dir +"/postingList", "r+b")
    data = dic.GetInfo(Term)
    #print(data)
    if data == -1:
        return -1
    t = 0
    sum = 0;
    while t < len(data) - 1:
        sum += data[t]
        termlast = dic.dic[sum:sum + data[t + 1]]
        #print(termlast)
        t += 1
        if Term == termlast:
            break

    index = dic.arr.index(data) * BLK + t
    #f6.close()
    #print(index)
    return index



def get_postingList_location(dir):
    posting_list_locate = []
    f7 = open(dir + "/postingListLocate", "r+b")
    n = bytearray(f7.read(1))
    while n:
        if n[0] >= 128:
            n[0] = n[0] - 128
            posting_list_locate.append(int(n[0]))
        else:
            temp = []
            temp.append(n[0])
            n = bytearray(f7.read(1))
            while n[0] < 128:
                temp.append(n[0])
                n = bytearray(f7.read(1))
            n[0] = n[0] -128
            temp.append(n[0])
            k =len(temp)-1
            i=0
            num =0
            #print(temp)
            while i < len(temp):
                num += int(temp[i] * math.pow(128,k))
                k -= 1
                i += 1
            #print(i)
            posting_list_locate.append(num)
            #print(temp,num)
        n = bytearray(f7.read(1))
        if len(posting_list_locate) > 1:
            posting_list_locate[-1] = posting_list_locate[-1] + posting_list_locate[-2]
    return posting_list_locate

def get_postingList_(dir, start,freq):
    posting_list_locate = []
    f7 = open(dir +'/postingList', "r+b")
    ss =f7.seek(start)
    t=1
    i=0
    n = int.from_bytes(bytes(f7.read(1)),"big")
    while i < freq:
        s =0
        while n < 128:
            s += n
            s = s*128
            n = int.from_bytes(bytes(f7.read(1)),"big")
        s += (n-128)
        posting_list_locate.append(s)
        n = int.from_bytes(bytes(f7.read(1)),"big")
        i += 1
    k =1
    while k < len(posting_list_locate):
        posting_list_locate[k] += posting_list_locate[k-1]
        k+=1
    f7.close()
    return posting_list_locate




def getPostingList(dir,start,end):
    file = open(dir,"r+b")
    file.seek(start)
    index_arr = []
    final_arr = []
    gropsize = file.read(1)
    readlimit = 1
    while readlimit < end-start:
        i = 0
        index = 8
        group_size_int = int.from_bytes(gropsize, byteorder="big")
        list = []
        while i < 4:

            if isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # 11 so 4 bytes
                k = bytearray(file.read(4))
                readlimit +=4
                if isKthBitSet(k[3], 8):
                    k[3] = (k[3] - 128)
                if k[2] % 2 == 1:
                    k[2] = k[2] >> 1
                    k[3] = (k[3] + 128)
                else:
                    k[2] = k[2] >> 1
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if k[1] % 2 == 1:
                    k[1] = k[1] >> 1
                    k[2] = (k[2] + 128)
                else:
                    k[1] = k[1] >> 1
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                #print(first_number)
                list.append(first_number)
            elif isKthBitSet(group_size_int, index) and not isKthBitSet(group_size_int, index - 1):  # its 10 so 3 bytes
                k = bytearray(file.read(3))
                readlimit += 3
                if isKthBitSet(k[2], 8):
                    k[2] = (k[2] - 128)
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[1] = k[1] + 128
                k[0] = k[0] >> 1
                if k[1] % 2 == 1:
                    k[2] = k[2] + 128
                k[1] = k[1] >> 1
                if k[0] % 2 == 1:
                    k[1] = k[1] + 128
                k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                #print(first_number)
                list.append(first_number)
            elif not isKthBitSet(group_size_int, index) and isKthBitSet(group_size_int, index - 1):  # its 01 so 2 bytes
                k = bytearray(file.read(2))
                readlimit += 2
                if isKthBitSet(k[1], 8):
                    k[1] = (k[1] - 128)
                if k[0] % 2 == 1:
                    k[0] = k[0] >> 1
                    k[1] = (k[1] + 128)
                else:
                    k[0] = k[0] >> 1
                first_number = int.from_bytes(k, "big")
                list.append(first_number)
            else:  # its only 0 so 1 byte
                first_number = file.read(1)
                readlimit += 1
                #print(first_number)
                list.append(int.from_bytes(first_number, byteorder="big"))
            i += 1
            index -= 2
        gropsize = file.read(1)
        readlimit += 1
        index_arr = index_arr + list


    file.close()
    return index_arr

def get_posting_freqList_(dir, start,freq):
    posting_list_locate = []
    f7 = open(dir +'/posting_freq_List', "r+b")
    ss =f7.seek(start)
    t=1
    i=0
    n = int.from_bytes(bytes(f7.read(1)),"big")
    while i < freq:
        s =0
        while n < 128:
            if n == 0:
                return []
            s += n
            s = s*128
            n = int.from_bytes(bytes(f7.read(1)),"big")
        s += (n-128)
        posting_list_locate.append(s)
        n = int.from_bytes(bytes(f7.read(1)),"big")
        i += 1

    f7.close()
    return posting_list_locate


def get_postingList_freq_location(dir):
    posting_list_locate = []
    f7 = open(dir + "/posting_freq_ListLocate", "r+b")
    n = bytearray(f7.read(1))
    while n:
        if n[0] >= 128:
            n[0] = n[0] - 128
            posting_list_locate.append(int(n[0]))
        else:
            temp = []
            temp.append(n[0])
            n = bytearray(f7.read(1))
            while n[0] < 128:
                temp.append(n[0])
                n = bytearray(f7.read(1))
            n[0] = n[0] -128
            temp.append(n[0])
            k =len(temp)-1
            i=0
            num =0
            #print(temp)
            while i < len(temp):
                num += int(temp[i] * math.pow(128,k))
                k -= 1
                i += 1
            #print(i)
            posting_list_locate.append(num)
            #print(temp,num)
        n = bytearray(f7.read(1))
        if len(posting_list_locate) > 1:
            posting_list_locate[-1] = posting_list_locate[-1] + posting_list_locate[-2]
    return posting_list_locate


"""
dic = getDic("first/sec/therd/Temp1")
print(dic.dic)
print(dic.arr)
s = get_postingList_location("first/sec/therd/Temp1")
print(s)

k = get_postingList_freq_location("first/sec/therd/Temp1")
fr = freq_read("first/sec/therd/Temp1")
print(fr)
i=0
pos_list_t = []
list_t =[]
while i < len(k)-1:
    #print(k[i],fr[i])
    pos_list_t.append(get_postingList_("first/sec/therd/Temp1",s[i],fr[i]))
    list_t.append(get_posting_freqList_("first/sec/therd/Temp1", k[i],fr[i]))
    i +=1

print(pos_list_t)
print(list_t)
"""