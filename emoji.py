import re


class EmojiConverter(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            emojis = f.readlines()
        self.emojList = list(map(lambda x: x.strip('\n'), emojis))
        self.chars = [chr(i) for i in range(ord('('), ord('(') + len(self.emojList))]
        self.exp = re.compile(r':[^:]*:')
        
    def __repr__(self):
        return ''.join(self.emojList + self.chars)

    def sentence_to_emoji(self, msg) -> str:
        newMsg = ''
        for chr in msg:
            cuc = ord(chr) - ord('(')
            emj = self.emojList[cuc]
            newMsg += emj
        return newMsg

    def emoji_to_sentence(self, msg) -> str:
        emjList = re.findall(self.exp,msg)
        eset = set(emjList)
        edic = dict()
        for k in eset:
            edic[k] = self.emojList.index(k)
        newMsg = ''
        for emj in emjList:
            c = self.chars[edic[emj]]
            newMsg += c
        return newMsg


    def is_emoji(self, chr) -> bool:
        return chr == ':'

# test
# if __name__ == "__main__":
#     conv = EmojiConverter("emojList.txt")
#     tgt_str = input('Enter string:')
#     emoji_text = conv.sentence_to_emoji(tgt_str)
#     print(tgt_str)
#     print(emoji_text)
#     print(conv.is_emoji(emoji_text))
#     print(conv.emoji_to_sentence(emoji_text))
