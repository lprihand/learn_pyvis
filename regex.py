import re 

routes = '''
*>i   4755:9829:10.9.136.60/30                           100         100       
      86.51.20.146                                       None        170100
      4755                                                           519013
*i    4755:9829:10.9.136.60/30                           100         100
      86.51.20.146                                       None        170100
      4755                                                           519013
'''

trusted = ['9828', '9897']

data = ' '
data_routes = data.join(dict.fromkeys(routes.split()))

'''
# Alternative solution 
routes_result_1 = re.compile(r"(?<=:)[0-9]+(?=:)") 
matches = routes_result_1.finditer(routes)

for i in matches: 
    print (i)
'''

routes_result = re.findall("(?<=:)\d+(?=:)", data_routes)
print (routes_result)

def jalan():
    a = "Sip route e ora conflict ki ..."
    return print (a)

if any(x in trusted for x in routes_result):
    print (f'Prefix conflict with below routes: \n {routes}')
else:
    jalan()


'''
https://regex101.com/r/HGGsyW/3

/
(?<=>)[\+\-]?\d+\.?\d*(?=<)
/

Positive Lookbehind (?<=>)
Assert that the Regex below matches
> matches the character > with index 6210 (3E16 or 768) literally (case sensitive)
Match a single character present in the list below [\+\-]
? matches the previous token between zero and one times, as many times as possible, giving back as needed (greedy)
\+ matches the character + with index 4310 (2B16 or 538) literally (case sensitive)
\- matches the character - with index 4510 (2D16 or 558) literally (case sensitive)
\d matches a digit (equivalent to [0-9])
+ matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
\. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
? matches the previous token between zero and one times, as many times as possible, giving back as needed (greedy)
\d matches a digit (equivalent to [0-9])
* matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
Positive Lookahead (?=<)
Assert that the Regex below matches
< matches the character < with index 6010 (3C16 or 748) literally (case sensitive)
Global pattern flags 
g modifier: global. All matches (don't return after first match)
'''
