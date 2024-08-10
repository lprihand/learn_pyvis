from prettytable import PrettyTable

Table = PrettyTable(['Name', 'Age', 'Occupation', 'City'])

Table.add_row(['Lukman','35','Network Engineer','Riyadh'])
Table.add_row(['Prihandika','30','Civil Engineer','Khobar'])
Table.add_row(['Abbas','15','Student','Japan'])
Table.add_row(['Fattah','20','Student','Berlin'])

print(Table)