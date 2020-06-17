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