class EmojiConverter(object):
    def __init__(self,path):
        with open(path, 'r') as f:
            ln = f.readline()
            emojis = list(ln)
        self.emojList = emojis
        self.chars = [chr(i) for i in range(ord('('), ord('(') + len(self.emojList))]
    def __repr__(self):
        return ''.join(self.emojList+self.chars)
    def sentence_to_emoji(self,msg)->str:
        newMsg = ''
        for chr in msg:
            cuc = ord(chr)-ord('(')
            emj = self.emojList[cuc]
            newMsg+=emj
        return newMsg
    def emoji_to_sentence(self,msg)->str:
        emSet = set(msg)
        edic = dict()
        newMsg=''
        for k in emSet:
            edic[k] = self.emojList.index(k)
        for chr in msg:
            chr_i = edic[chr]
            chr_c = self.chars[chr_i]
            newMsg+=chr_c
        return newMsg
    def is_emoji(self,chr)->bool:
        return chr in self.emojList

if __name__=='__main__':
    conv = EmojiConverter('emojList.txt')
    s = 'gAAAAABe6f9BdVCNEZ32u2OgQG1Q1y-s9JHua2wxNtt8BHkKt8bkPma6TEBBjPdkEVVqRSMDBVhZLcmxCQ9K-t1Oc4Gq1bBjIn3VQjGFV7JX9hOaBYKZXxLY4eKPiRhyHhpsgott5gmT'
    s2 = conv.sentence_to_emoji(s)
    s3 = conv.emoji_to_sentence(s2)
    print(s==s3)
    print(s)
    print(s3)