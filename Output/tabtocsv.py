import pandas as pd


D = pd.read_csv('D.tab', delimiter=' ')
ND = pd.read_csv('ND.tab', delimiter=' ')

D.to_csv('D.csv')
ND.to_csv('ND.csv')
