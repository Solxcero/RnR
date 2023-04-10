from math import sqrt
import pandas as pd

score_df = pd.read_csv('C:/Users/user/Desktop/Project/Final/webFinal/score.csv')
ht_info = pd.read_csv('C:/Users/user/Desktop/Project/Final/webFinal/호텔_리스트_최종.csv')


ht_lst = pd.merge(score_df['ht_id'],ht_info[['ht_id','ht_name']], left_on='ht_id',right_on='ht_id',how='inner').set_index('ht_id')
df = score_df.set_index('ht_id')
df = df.dropna(axis=0, how='all')

cat_lst = df.columns.tolist() 
  
ht = {}
for i in list(df.index):
    ht[i] = {}
    for c in cat_lst:
        if pd.isna(df.loc[i,c])==False:
            ht[i][c] = df.loc[i,c]
        else:
            continue

# 유클리디안 거리공식
def sim_dist(id1, id2):
    sum = 0 
    for i in ht[id1]:
        sum += pow(ht[id1][i] - ht[id2][i],2)
        
    return 1/(1+sqrt(sum))

# 피어슨 상관계수
def sim_hotel( name1, name2):
    sumX=0 # X의 합
    sumY=0 # Y의 합
    sumPowX=0 # X 제곱의 합
    sumPowY=0 # Y 제곱의 합
    sumXY=0 # X*Y의 합
    count=0 #호텔 개수
    
    for i in ht[name1]: # i = key
        if i in ht[name2]:
            sumX+=ht[name1][i]
            sumY+=ht[name2][i]
            sumPowX+=pow(ht[name1][i],2)
            sumPowY+=pow(ht[name2][i],2)
            sumXY+=ht[name1][i]*ht[name2][i]
            count+=1
    
    return (sumXY- ((sumX*sumY)/count) )/ sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count)))

def top_match(id, index=5, sim_function=sim_hotel):
    li = []
    for i in ht:
        if id != i :
            li.append((sim_function(id,i),i,ht_lst.loc[i,'ht_name'])) #유사도, 이름을 튜플에 묶어서 리스트로 저장
    li.sort() # 오름차순
    li.reverse() # 뒤집기
    
    t = li[:index]
    print(t)
    return t

