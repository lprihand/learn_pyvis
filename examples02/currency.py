import json
import sys
import urllib.request

if (len(sys.argv[2]) & len(sys.argv[3])) != 3:
    print("Usage: ./currencyrates.py lookup_currency base_currency. Example: ./currencyrates.py 10 cad usd")
    sys.exit()

value = sys.argv[1]
currency = sys.argv[2]
basecurrency = sys.argv[3]

currencyurl = "http://freecurrencyrates.com/api/action.php?do=cvals&iso=" + currency + "&f=" + basecurrency + "&v=1&s=cbr"
f = urllib.request.urlopen(currencyurl)
obj = json.loads(f.read())
result = f"{value} " + currency.upper() + " is "
result+="{:,.2f}".format(int(value)/obj[currency.upper()]) + " " + basecurrency.upper()

print(result);

'''
https://mkaz.blog/code/python-string-format-cookbook/
'''

'''
&q  is your main query.
&dq is ISSN/LCCN/OCLCnum query, it is the standard name of the book.
&f  is the bool for sidebar. false value shows the sidebar, true value hides it. Basically setting it to true will tell the API to not to bother to add the sidebar HTML in the HTML coding.
&redir_esc accepts two values, y or n, though I've seen it with empty values in some urls. I'm not sure about its purpose.
#v=onepage is the parameter that sets view of the Book in the browser. onepage sets the view to Single Page View. snippet sets it to Snippet View.
'''

'''
&s is represent request to DB
[\\?&] is a character class. It matches a single character which is either & or ?. (The question mark is a special character in JavaScript regexes, so it must be escaped by preceding it with a backslash. The backslash is a special character in JavaScript strings, so it must be escaped also, hence the double backslash. That's fairly common in regular expressions.)
v= matches the literal string v=.
( begins a capturing group, so everything until the next ) will be placed into a separate entry in the returned array.
[^&#]* any number of characters (including none) until a & or # is found. The brackets indicate a character class as above, and the ^ inverts the class so it includes all characters except those listed before the end bracket. The * indicates that the preceding character class is to be matched zero or more times.
The ) ends the capturing group.
'''