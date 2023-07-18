import jieba

text = '我来到北京清华大学'
seg_list = jieba.cut(text)
print('Full Mode: ' + '/'.join(seg_list))
