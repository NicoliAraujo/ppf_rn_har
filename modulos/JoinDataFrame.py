'''
Created on 22 de mai de 2017

@author: pibic-elloa-nicoli
http://sensor.informatik.uni-mannheim.de/#dataset_realworld_subject6
'''
import pandas as pd
import os

        
class Subject:
    '''Classe que adiciona subject, gender, age, health e weight aos dataframes
    de acc e de gyr de cada sujeito 
    '''
    def __init__(self, activity_list,num_subject, body_part, etc=''):
        
        self.subject_df = pd.DataFrame()
        self.add_activity(activity_list, num_subject, body_part, etc)
        #print(self.subject_df)
    def remove_time(self, df, sensor):
        df.drop(['attr_time_'+sensor], axis=1, inplace=True)
            
    def add_attr(self, num_sub):
        for attr in ATT_DICT:
            #print(attr, att_dict, att_dict[attr])
            #print(int(num_sub))
            self.subject_df[attr] = ATT_DICT[attr][int(num_sub)-1]
        #print(self.subject_df)
        
        
    def set_time(self, df, sensor):
        #print(self.subject_df)
        #print(df)
        total = pd.Series(df['attr_time_'+sensor])
        #print(total)
        #total.reindex([i for i in range(len(total))], inplace=True)
        #print('total', total, total.size)
        defasada = pd.Series([0]).append(df['attr_time_'+sensor].loc[:len(df)-2])
        defasada.index = total.index
        #print('defasada',defasada)
        
        df['duration_'+sensor] = total-defasada
        
        df.set_value(0, 'duration_'+sensor, 0)
        
        #print(df['duration_'+sensor])
        self.remove_time(df, sensor)
        
    def drop_extra_lines(self, df1, df2):
        len1 = len(df1)
        len2 = len(df2)
        if len1!=len2:
            if len1>len2:
                df1.drop(df1.index[[len2,len1-1]], inplace=True)
            else:
                df2.drop(df2.index[[len1,len2-1]], inplace=True)
                
    def rename_attr(self, df, sensor):
        df.rename(columns={'attr_x':sensor+'_x', 'attr_y':sensor+'_y', 'attr_z':sensor+'_z', 'attr_time':'attr_time_'+sensor,}, inplace=True)
    
    def reorder_cols(self):
        #self.subject_df.drop('id', inplace=True)
        print(self.subject_df)
        self.subject_df = self.subject_df.reindex(columns=['subject', 'gender', 'age', 'weight', 'height', 'duration_acc', 'acc_x', 'acc_y', 'acc_z', 'duration_gyr', 'gyr_x', 'gyr_y', 'gyr_z', 'activity'])
    
    def set_dfs_sensor(self, num_subject, activity, sensor,  etc):
        try:
            if sensor == 'gyr':
                sensor_name = 'Gyroscope'
            else:
                sensor_name = 'acc'
            filename = PATH +num_subject+'/' + sensor + '_' + activity + '_csv/' + sensor_name + '_' + activity + '_' + etc + body_part +'.csv'
            
            df = pd.read_csv(filename)
            
        except:
            try:
                filename = PATH + num_subject+'/' + sensor + '_' + activity + '_csv/' + sensor_name + '_' + activity + '_' + body_part +'.csv'
                df = pd.read_csv(filename)
                
            except:
                print('df ', sensor , ' deu problema:', activity, filename)
                df = pd.DataFrame()
        #print(df)
        try:
            df.drop('id', axis=1, inplace=True)
        except:
            pass
        self.rename_attr(df, sensor)
        self.set_time(df, sensor)
        return df
      
    def add_activity(self, activity_list, num_subject, body_part, etc=''):
        for activity in activity_list:
            df_acc = self.set_dfs_sensor(num_subject, activity, 'acc', etc)
            
            
            df_gyr = self.set_dfs_sensor(num_subject, activity, 'gyr', etc)
            
            
            self.drop_extra_lines(df_acc, df_gyr)
            
            df_act = pd.concat([df_acc, df_gyr], axis=1, join_axes=[df_acc.index])
            
            df_act['activity'] = activity
            self.subject_df = self.subject_df.append(df_act)
            #print(self.subject_df)
            self.subject_df = self.subject_df.reset_index(drop=True)
            #self.subject_df.drop('id')
        
        #print(self.subject_df)
    '''def add_activity(self, activity_list, num_subject, body_part, etc):
        for activity in activity_list:
            filename_acc = PATH +num_subject+'/' + 'acc' + '_' + activity + '_csv/' + 'acc' + '_' + activity + '_' + etc + body_part +'.csv'
            #print(filename_acc)
            filename_gyr = PATH +num_subject+'/' + 'gyr' + '_' + activity + '_csv/' + 'Gyroscope' + '_' + activity + '_' + etc + body_part +'.csv'
            df_acc = pd.read_csv(filename_acc, index_col=0)
            self.rename_attr(df_acc, 'acc')
            df_gyr = pd.read_csv(filename_gyr, index_col=0)
            self.rename_attr(df_gyr, 'gyr')
            
            self.drop_extra_lines(df_acc, df_gyr)
            
            df_act = pd.concat([df_acc, df_gyr], axis=1, join_axes=[df_acc.index])
            
            df_act['activity'] = activity
            self.subject_df = self.subject_df.append(df_act)
            self.subject_df = self.subject_df.reset_index(drop=True)
        #print(self.subject_df)'''
    def save_subject(self, subject, body_part):
        path = '../dados/sensores_separados/' + subject
        os.makedirs(path, exist_ok=True)
        filename = path + '/' + subject + '_' + body_part +  '.csv'
        #print(filename)
        with open(filename, 'w') as file:
            self.subject_df.to_csv(filename)
            
PATH = '../dados/realworld2016_dataset/proband'
ATT_DICT = {'subject':[i for i in range(1,16)],
            'gender': ['F', 'M', 'M', 'M', 'M', 'F', 'M', 'F','M', 'M', 'F', 'F', 'F', 'M', 'F'],
            'age':[52, 26, 27, 26, 62, 24, 26, 36, 26, 26, 48, 16,27,26,30],
            'height': [163, 179, 176, 183,170, 174, 180, 165, 179,170,175,164,170,183,165], #em cm
            'weight': [48, 70, 81, 82,70,65, 81,95,95,90,71,54,65,78,66]}

if __name__ == '__main__':

    body_part_list = ['upperarm', 'forearm']
    activity_list = ['climbingdown', 'climbingup', 'jumping', 'lying',
                 'running', 'sitting', 'standing', 'walking']
    
    
    '''
    for i in range(13,16):
        for body_part in body_part_list:
            sub_acc = Subject(activity_list, str(i), body_part)
            sub_acc.add_attr(att_dict, i)
            sub_acc.set_time()
            sub_acc.save_subject(str(i), body_part)'''
    
    i=2
    
    '''#j=2
    for body_part in body_part_list:
        sub_acc = Subject(activity_list, str(i), body_part)
        sub_acc.add_attr(att_dict, i)
        sub_acc.set_time()
        sub_acc.save_subject(str(i), body_part)'''
        
    
    
    
    '''for body_part in body_part_list:
        df1 = pd.DataFrame()
        for j in range(1,4):
            sub_acc = Subject(activity_list, str(i), body_part, etc=str(j)+'_')
            sub_acc.add_attr(att_dict, i)
            try:
                sub_acc.set_time()
            except:
                print('não deu pra setar o tempo pra ', j)
            #print(len(sub_acc.subject_df))
            df1=pd.concat([sub_acc.subject_df, df1])
            print(len(df1))
        sub_acc.subject_df=df1
        sub_acc.save_subject(str(i), body_part)
        print(len(sub_acc.subject_df))'''
    
    for body_part in body_part_list:
        print(body_part)
        sub_acc = Subject(activity_list, str(i), body_part)
        #print(sub_acc.subject_df)
        sub_acc.add_attr(i)
        sub_acc.reorder_cols()
        sub_acc.save_subject(str(i), body_part)