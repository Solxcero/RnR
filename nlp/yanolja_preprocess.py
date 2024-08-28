import pandas as pd
from hanspell import spell_checker
import re
import datetime
from datetime import timedelta
from kss import split_sentences


def change_date(x):
    # now = datetime.datetime.today()  # 크롤링한 날짜로 바꿔서 하면 될 듯
    now = datetime.datetime(2023,2,22)  # 크롤링한 날짜로 바꿔서 하면 될 듯
    today = now.strftime("%Y.%m.%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y.%m.%d")
    _2days_ago = (now - timedelta(days = 2)).strftime("%Y.%m.%d")
    _3days_ago = (now - timedelta(days = 3)).strftime("%Y.%m.%d")
    hour = int(datetime.datetime.today().strftime("%H"))
    if "시간 전" in x:
        x = int(x.replace("시간 전", ""))
        if hour - x > 0: return today
        else: return yesterday
    elif "일 전" in x:
        if "1" in x: return yesterday
        elif "2" in x: return _2days_ago
        else: return _3days_ago
    elif "분 전" in x :
        return today
    else: return x
    
def get_season(x):
    if x == 3 or x==4 or x==5:
        return 'Spring'
    elif x == 6 or x==7 or x==8 :
        return 'Summer'
    elif x==9 or x==10 or x==11 :
        return 'Autumn'
    else:
        return 'Winter'
    
def spell_check(review):
    result = spell_checker.check(review)
    return result.checked

def del_text(df,n):
    df['date'] = df['date'].apply(lambda x : change_date(x))
    df['date'] = pd.to_datetime(df['date'])
    df['Month'] = df['date'].apply(lambda x : x.month)
    df['Season'] = df['Month'].apply(lambda x : get_season(x))
    
    df['review'] = df['review'].apply(lambda x: x.replace('\n',''))
    df['review'] = df['review'].apply(lambda x: x.replace('\r',''))
    df['review'] = df['review'].str.replace('[^가-힣 0-9]','')
    df['review'] = df['review'].apply(lambda x : re.sub('[ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅃㅉㄸㄲㅆㅛㅕㅑㅐㅔㅗㅓㅏㅣㅜㅠㅡ]', '',x))

    idx = df[df['review']==""].index
    df.drop(index=idx,inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    idx = 0
    test = pd.DataFrame({'date':[],'star':[],'review':[],'month':[],'season':[]})


    for i in range(df.shape[0]):
        try : 
            sent = split_sentences(df.iloc[i,2])
            if len(sent) != 1 :
                for s in sent:
                    df1 = pd.DataFrame({'date':df.iloc[i,0],'star':df.iloc[i,1],'review':s,'month':df.iloc[i,3],'season':df.iloc[i,4]},index=[idx])
                    idx += 1
                    test = pd.concat([test,df1])
            else:
                df1 = pd.DataFrame({'date':df.iloc[i,0],'star':df.iloc[i,1],'review':sent,'month':df.iloc[i,3],'season':df.iloc[i,4],},index=[idx])
                idx += 1
                test = pd.concat([test,df1])
        except :
            pass
    test[['month']] = test[['month']].astype(int)
    test['date'] = test['date'].dt.strftime("%Y.%m.%d")
    test['review']=test['review'].astype('str')
    test['review'] = test['review'].apply(lambda x : spell_check(x))
    test.reset_index(drop=True,inplace=True)
    test['ht_id'] = n
    test = test[['ht_id','date','star','review','month','season']]
    return test

