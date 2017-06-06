import pandas as pd

print('Carregando...')
forearm = [pd.read_csv('../../../Documentos/defasados/1000ms/'+str(i)+'_forearm_1000ms.csv', index_col=0) for i in range(0, 12)]
print('Carregados!')

print('Concatenando...')
saida1 = pd.concat(forearm)
#saida2 = pd.concat(upperarm)
print('Concatenandos!')

print('Reindexando...')
saida1.index = [i for i in range(0, saida1.shape[0])]
#saida2.index = [i for i in range(0, saida2.shape[0])]
print('Reindexandos!')


vet = ['subject_1', 'gender_1', 'age_1', 'weight_1', 'height_1', 'duration_acc_1']
for i in range(0, 4):
    for j in vet:
        saida1 = saida1.drop(j + str(i), axis=1)

for i in list(saida1.columns):
    if 'duration' in i:
        saida1 = saida1.drop(i, axis=1)
    if 'activity' in i and '13' not in i:
        saida1 = saida1.drop(i, axis=1)

vet = ['subject', 'gender', 'age', 'weight', 'height']
for i in vet:
    saida1 = saida1.rename(columns={i + '_' + str(1): i})

saida1 = saida1.rename(columns={'activity_13': 'activity'})

print(list(saida1.columns))
saida1.to_csv('forearm_1000ms.csv')


"""
print('Salvando...')
saida1.to_csv('forearm.csv')
saida2.to_csv('upperarm.csv')
print('Salvos!')
"""
