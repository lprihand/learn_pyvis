
routes = '''
*>i   4755:9829:10.9.136.60/30                           100         100       
      86.51.20.146                                       None        170100
      4755                                                           519013
*i    4755:9829:10.9.136.60/30                           100         100
      86.51.20.146                                       None        170100
      4755                                                           519013
'''
data = ' '
data = data.join(dict.fromkeys(routes.split()))
print (data)

print(' '.join(dict.fromkeys(routes.split())))
