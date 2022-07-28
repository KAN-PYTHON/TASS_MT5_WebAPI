from collections import Counter

i = ('12', '34')
list1 = ['12', '34', '23', '89']
list2 = ['12656776867987078762452343324']

print(any(map(i.__contains__, '123434652352312423524357547')))

common_items = list((Counter(list1) & Counter(list2)).elements())

print(common_items)