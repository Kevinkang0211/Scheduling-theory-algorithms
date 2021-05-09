import pandas as pd
import numpy as np

data = pd.read_csv("C:/Users/kevin/Desktop/課程Lesson/排程理論與應用/HW-flowshop/flowshop.csv")

m1 = np.array(data.iloc[0][1:])
m2 = np.array(data.iloc[1][1:])


def get_seq(m1,m2):
    
    #依據johnson's rule，將所有工作分成兩群 
    s1=[]
    s2=[]
    
    for i in range(len(m1)):
        if m1[i]<=m2[i]:
            s1.append([i,m1[i]])
        else:
            s2.append([i,m2[i]])
            
    #第一群照M1的process time由小排到大，第二群照M2的process time由大排到小
    s1 = sorted(s1, key = lambda s: s[1])
    s2 = sorted(s2, key = lambda s: s[1],reverse=True)
    
    #再把經過排序好的兩群合併
    seq =pd.concat([pd.DataFrame(s1).iloc[:][0], pd.DataFrame(s2).iloc[:][0]], ignore_index=True)
    return seq
    
#用johnson's rule得到machine1、2的整體jobs排序
all_seq = get_seq(m1, m2)

#table for in and out time 計算machine中所有工作進出的時間
m1_table=[[],[]]
m2_table=[[],[]]

temp_in = 0


#compute for machine1
for index in all_seq:    
    m1_table[0].append(temp_in)
    m1_table[1].append(temp_in+m1[index])
    temp_in+=m1[index]
    
#compute for machine2
temp_out = 0
for i in range(len(all_seq)):
    m2_table[0].append(max(m1_table[1][i] , temp_out))
    m2_table[1].append(m2_table[0][i] + m2[all_seq[i]])
    temp_out=m2_table[1][i]
    
    
#整個flow shop結束的時間
end_time = m2_table[1][-1]
   
#machine1、2的總idle time
it1 = end_time - m1_table[1][-1]
it2 = end_time - sum(m2)

print('Jobs sequence under johnson\'s algorithm:')
print([x for x in all_seq])
print('')
print('-Total Flow Shop time: ', end_time)
print('-Machine1\'s idle time:', it1)
print('-Machine2\'s idle time:', it2)




