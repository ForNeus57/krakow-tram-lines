import pandas as pd

url = 'https://api.ttss.pl/vehicles/trams/'
dfs = pd.read_html(url)

print(len(dfs))

#for table in range(len(dfs)):
#  print(dfs[table])

vbLine = dfs[0]
vbType = dfs[1]
vbTtss = dfs[2]

print("vehicles by line :")
print(vbLine)

print(vbLine.info())

d = {

  }

df = pd.DataFrame(data=d)