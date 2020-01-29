import math


class PostingList:
    def __init__(self, DocIDs, type):
        """Given sorted list of DocIDs, creates a
        compressed posting list according to the
        compression type.
        The compressed posting list should be stored as
        byte array"""
        self.Docs = bytearray()
        self.type = type
        if type == "V":
            list = self.buildVDoc(DocIDs)
            print(list)
            for item in list:
                self.Docs.append(item)
        elif type == "LP":
            list = self.buildLPV(DocIDs)
            for item in list:
                self.Docs.append(item)
        elif type == "GV":
            list = self.buildGV(DocIDs)
            for item in list:
                self.Docs.append(item)

    def buildVDoc(self, DocIDs):
        docList = []
        j = len(DocIDs) - 1;
        while j >= 0:
            i = 0
            list = []
            if j != 0:
                DocIDs[j] = DocIDs[j] - DocIDs[j - 1]

            while DocIDs[j] > 128:
                temp = int(DocIDs[j] / 128)
                temp2 = DocIDs[j] - temp * 128
                list.insert(len(list) - i, temp2)
                DocIDs[j] = temp
                i += 1
            list.insert(0, DocIDs[j])
            list[len(list) - 1] = 128 + list[len(list) - 1]
            j -= 1
            docList = list + docList
        #print(DocIDs)
        return docList
        # print(bytearray(docList))

    def buildLPV(self, DocIDs):
        docList = []
        j = len(DocIDs) - 1
        while j >= 0:
            list = []
            if j != 0:
                item = DocIDs[j] - DocIDs[j - 1]
            else:
                item = DocIDs[j]

            if (64 * 128 * 128 * 128) > item >= (64 * 128 * 128):
                i = 3
            elif (64 * 128 * 128) > item >= (64 * 128):
                i = 2
            elif 128 * 64 > item >= 64:
                i = 1
            else:
                i = 0
            if i == 0:
                list.append(item)
            elif i == 1:
                b_6 = int(item / 128)
                m_6 = item % 128
                list.append(b_6 + 64)
                list.append(m_6 + 128)
            elif i == 2:
                b_6 = int(item / (128 * 128))
                m_6 = item % (128 * 128)
                b_7 = int(m_6 / 128)
                m_7 = m_6 % 128
                list.append(b_6 + 128)
                list.append(b_7 + 128)
                list.append(m_7 + 128)
            else:
                b_7 = int(item / (128 * 128 * 128))  # 1
                m_7 = item % (128 * 128 * 128)
                b_7_2 = int(m_7 / (128 * 128))  # 2
                m_7_2 = m_7 % (128 * 128)
                b_7_3 = int(m_7_2 / 128)  # 3
                m_7_3 = m_7_2 % 128
                list.append(b_7 + 192)
                list.append(b_7_2 + 128)
                list.append(b_7_3 + 128)
                list.append(m_7_3 + 128)

            docList = list + docList
            j = j - 1
        return docList

    def buildGV(Dself, DocIDs):
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
                if j == 0:
                    if len(DocIDs) != 0:
                        item = k[j] - DocIDs[len(DocIDs) - 1]
                    else:
                        item = k[j]
                else:
                    item = k[j] - k[j - 1]
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

    def GetList(self):
        """Returns a byte-array containing the
        compressed string"""
        return self.Docs

