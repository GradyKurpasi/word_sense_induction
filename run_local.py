from  services.semeval2015_import import  *


# g.V().hasLabel('lemma').group().by('id').by(out('hasSense').count())



# import_semeval2015_lemma()

# import_semeval2015_keys()


# class PadList(list):
#     def ljust(self, n, fillvalue=''):
#         return self + [fillvalue] * (n - len(self))

#     def rjust(self, n, fillvalue=''):
#         return [fillvalue] * (n-len(self)) + self

# a = PadList()

# a.append('1')

# b = a.rjust(5, '')
# print(b)


# sent = "this is a really long fucking sentence that I'm writing right now because I need a reallly fuckiung long esententnence to stest ssome shit with"
# lsent = sent.split()
# print (lsent[-5:])



# preprocess_semeval2015_documents()

create_centered_contexts()




# s = ["doc", "1", "this is a sentence"]
# s1 = ["ass", "2", "you are an ass"]

# ls = [s, s1]
# print(ls)

# s = set()
# # s.add(('me', 'you'))
# s.add(('you', 'me'))
# f = ('me', 'you')


# m = 'me'
# y = 'you'

# s.add((m, y))
# print(s)
# f = (m, y)
# # print(f)
# s.add(f)

# print((m, y) not in s)


# s = []
# s.append('asdf')
# s.append('asd')
# s.append(' ')
# print(s)
# t = []
# t.append('asdf')
# t.append('asd')
# t.append(' ')
# t.append('asdfaeerer')
# print(t)
# ls = [s, t]

# print(ls)

# print(ls[1][3])

# import json

# with open("file.json", 'w') as f:
#     json.dump(ls, f, indent = 2)




# d = {}
# d['asdf'] = 'd0.s1'
# print(d)

# l = []
# l.append('d-0.s1')
# print(l[0])