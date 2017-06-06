import pandas as pd

QTDFRAME = 25
QTDSUBJECT = 16
vet = [1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15]
forearm = [pd.read_csv('../../../Documentos/sensores_separados/'+str(i)+'/'+str(i)+'_forearm.csv', index_col=0) for i in vet]
print('Leitura -- ok')

NOMES = ['climbingdown', 'climbingup', 'jumping', 'lying', 'running', 'sitting', 'standing', 'walking']
for SUBJECT in range(0, len(vet)):#SUBJECT
    print('SUBJECT ', SUBJECT)
    vet_series = []
    move = [forearm[SUBJECT].loc[forearm[SUBJECT].activity == NOME_MOVIMENTO] for NOME_MOVIMENTO in NOMES]
    vet = []
    for n_move in range(0, len(NOMES)):
        cont = 0
        for n_index in move[n_move].index:
            if (move[n_move].loc[n_index].duration_acc >= 15) and (move[n_move].loc[n_index].duration_acc <= 25):
                cont += 1
                if cont == QTDFRAME:
                    vet_series.append(move[n_move].loc[n_index-QTDFRAME:n_index-1])
                    vet_series[len(vet_series)-1].index = [k for k in range(QTDFRAME)]
                    cont = 0
            else:
                cont = 0
        print('series_geradas')
    print('QTD DE SERIES ', len(vet_series))
    dataMove = []
    for j in range(0, len(vet_series)):
        dic = []
        for k in range(0, QTDFRAME):
            dic.append({'a': list(vet_series[j].loc[k].index), 'b': list(vet_series[j].loc[k].values)})
        for k in range(0, len(dic)):
            for l in range(0, len(dic[k]['a'])):
                dic[k]['a'][l] = dic[k]['a'][l] + '_' + str(k + 1)
        aux = pd.concat([pd.DataFrame(dic[k]).T for k in range(0, QTDFRAME)], axis=1)
        aux.columns = aux.loc['a']
        aux = aux.drop('a')
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
        dataMove.append(aux)
    print('SUBJECT '+str(SUBJECT)+' -- OK')
    result = pd.concat(dataMove)
    result.to_csv('../../../Documentos/defasados/500ms/'+str(SUBJECT)+'_forearm_500ms.csv')
