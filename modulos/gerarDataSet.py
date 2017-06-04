import pandas as pd
import numpy as np

QTDFRAME = 13
forearm = [pd.read_csv('../../Documentos/sensores/'+str(i)+'_forearm.csv', index_col=0) for i in range(1, 2)]
#print(np.sum([forearm[0].loc[forearm[0].duration_acc == i].duration_acc.count() for i in range(15, 26)])/forearm[0].shape[0])

#upperarm = [pd.read_csv('../../Documentos/sensores/'+str(i)+'_upperarm.csv') for i in range(1, 3)]
print('Leitura -- ok')

move_str = ['climbingdown', 'climbingup', 'jumping', 'lying', 'running', 'sitting', 'standing', 'walking']
move = [forearm[0].loc[forearm[0].activity == j] for j in move_str]

test2 = []
for i in range(0, 1):
    cont = 0
    dataMove = []
    for j in range(0, move[i].shape[0]):
        if (move[i].loc[j].duration_acc >= 15) and (move[i].loc[j].duration_acc <= 25):
            cont += 1
            if cont == QTDFRAME:
                test2.append(move[0].loc[j-QTDFRAME:j-1])
                cont = 0
        else:
            cont = 0
    print('Series geradas')
    for j in range(0, 2):
        dic = []
        for k in range(0, QTDFRAME):
            dic.append({'a': list(test2[j].loc[k].index), 'b': list(test2[j].loc[k].values)})

        for k in range(0, len(dic)):
            for l in range(0, len(dic[k]['a'])):
                dic[k]['a'][l] = dic[k]['a'][l] + '_' + str(k + 1)
        print('Nomes editados ', j)
        aux = pd.concat([pd.DataFrame(dic[k]).T for k in range(0, QTDFRAME)], axis=1)
        print('Transpose')
        aux.columns = aux.loc['a']
        aux = aux.drop('a')
        print('Reindex')
        for k in aux.columns:
            if ('subject' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
            elif ('gender' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
            elif ('age' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
            elif ('weight' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
            elif ('height' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
            elif ('activity' in k) and not ('1' in k):
                aux = aux.drop(k, axis=1)
        print('Colunas eliminadas')
        dataMove.append(aux)

result = pd.concat(dataMove)
result.to_csv('teste.csv')
