# import jieba

# text = '我来到北京清华大学'
# seg_list = jieba.cut(text)
# print('Full Mode: ' + '/'.join(seg_list))

import json

d1 = {
    '你': [1, 2],
    '我': [3, 4]
}
str1 = json.dumps(d1, ensure_ascii=False)
print(type(str1), str1)

d2 = {
    '你': [1, 2],
    '我': [3, 4]
}
d2['你'] = json.dumps(d2['你'], ensure_ascii=False)
d2['我'] = json.dumps(d2['我'], ensure_ascii=False)
print(type(d2), d2)