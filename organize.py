import pandas as pd
import  unidecode

leagues = ['ligue1','bund','prem','laliga','serieA']
categories = ['','AdvGK','Creativity','Defensive','GK','Misc','Passing','PassTypes','Possession','Shooting']

catColumns = []
allDfs = []
for c in categories:
    dfs = []
    colNames = []
    for l in leagues:
        name = l + c
        fileName = "Data/" + name + '.csv'
        file = pd.read_csv(fileName, header=1, encoding='latin1')
        dfs.append(file)

        cols = file.columns
        colNames.append(cols)
    catColumns.append(colNames)
    full = pd.concat(dfs, ignore_index=True)
    allDfs.append(full)

print(allDfs[0])

for i in range(len(categories)):
    temp = allDfs[i]
    uid = [name.split('\\')[1] for name in temp['Player']]
    temp['uid'] = uid
    filename = 'Data/consolidated'+categories[i]+".csv"
    allDfs[i].to_csv(filename, index=False, encoding='latin1')

final = pd.read_csv('Data/consolidated.csv')
for i in range(len(categories)):
    if i == 0:
        continue
    fileName = 'Data/consolidated'+categories[i]+'.csv'
    temp = pd.read_csv(fileName)
    colsToUse = temp.columns.difference(final.columns).tolist()
    colsToUse.append(['Player','Squad'])
    final = pd.merge(final, temp[colsToUse], on=['Player','Squad'], how='outer', suffixes=('','_remove'))
    final.drop(['Players_remove','Squad_remove'], inplace=True)

for x in final['Player']:
    print(x)
final['Player'] = [unidecode.unidecode(s) for s in final['Player']]
final['Squad'] = [unidecode.unidecode(s) for s in final['Squad']]
final.to_csv('finalData.csv', index=False)

    # for cols in colNames:
    #     print(cols)
    #     ligue1 = list(cols[0])
    #     bund = cols[1]
    #     prem = cols[2]
    #     laliga = cols[3]
    #     serieA = cols[4]

        #for idx in range(len(ligue1)):
            #print(ligue1[idx])
            #if ligue1[idx] == bund[idx] == prem[idx] == laliga[idx] == serieA:
                #print("Category: "+c+"\nColumn: "+ligue1[idx]+" Passed\n")
            #else:
                #print("Category: "+c+"\nColumn: "+ligue1[idx]+" Failed\n")