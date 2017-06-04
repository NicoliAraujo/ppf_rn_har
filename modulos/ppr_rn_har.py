
# coding: utf-8

# In[181]:


import pandas as pd
import numpy as np

QTDFRAME = 13
QTDSUBJECT = 16
forearm = [pd.read_csv('Documentos/sensores/'+str(i)+'_forearm.csv', index_col=0) for i in range(1, 16)]
#forearm += [pd.read_csv('Documentos/sensores/4'+str(i)+'_forearm.csv', index_col=0) for i in range(1, 4)]
#forearm += [pd.read_csv('Documentos/sensores/'+str(i)+'_forearm.csv', index_col=0) for i in range(5, 7)]
#forearm += [pd.read_csv('Documentos/sensores/7'+str(i)+'_forearm.csv', index_col=0) for i in range(1, 4)]
#forearm += [pd.read_csv('Documentos/sensores/'+str(i)+'_forearm.csv', index_col=0) for i in range(8, 14)]
#forearm += [pd.read_csv('Documentos/sensores/14'+str(i)+'_forearm.csv', index_col=0) for i in range(1, 4)]
#forearm += [pd.read_csv('Documentos/sensores/'+str(i)+'_forearm.csv', index_col=0) for i in range(15, 16)]
print('Leitura -- ok')


# In[186]:


move_str = ['climbingdown', 'climbingup', 'jumping', 'lying', 'running', 'sitting', 'standing', 'walking']
for a in range(0, len(forearm)):
    move = [forearm[a].loc[forearm[a].activity == j] for j in move_str]
    test2 = []
    dataMove = []
    for i in range(0, 2):
        cont = 0
        move[i]
        for j in range(0, move[i].shape[0]):
            if (move[i].loc[j].duration_acc >= 15) and (move[i].loc[j].duration_acc <= 25):
                cont += 1
                if cont == QTDFRAME:
                    test2.append(move[0].loc[j-QTDFRAME:j-1])
                    test2[len(test2)-1].index = [i for i in range(QTDFRAME)]
                    cont = 0
            else:
                cont = 0
        print('Series geradas')


# In[183]:


for j in range(0, len(test2)):
    dic = []
    for k in range(0, QTDFRAME):
        dic.append({'a': list(test2[j].loc[k].index), 'b': list(test2[j].loc[k].values)})
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


# In[184]:


result = pd.concat(dataMove)
result.to_csv('teste.csv')


# In[ ]:




