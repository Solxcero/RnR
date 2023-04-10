# -*- coding: utf-8 -*-
from flask import Flask, redirect , render_template, request, url_for,jsonify
import pandas as pd
import numpy as np
import json 
import random
from modules import cbf
from konlpy.tag import Okt
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
import re

# 엘라스틱서치 전처리
es = Elasticsearch(["http://127.0.0.1:9200"])
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS') 

with open('./Ko_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.readlines()
    stopwords = [x.strip() for x in stopwords]

def preprocess_text(text):
    mecab = Okt()
    text = re.sub('[^0-9가-힣ㄱ-ㅎㅏ-ㅣ\s]', '', text)
    tokens = mecab.morphs(text)
    tokens = [word for word in tokens if word not in stopwords]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

ht_name_pattern = r'\b(24게스트하우스서울시청점|57명동호스텔|AC호텔바이메리어트서울강남|BB홍대호스텔|D.H네상스호텔|DW디자인레지던스|ENA스위트호텔남대문|G2호텔명동|G3호텔충무로|Glue호텔|G게스트하우스이태원인서울|HAvenue이대점|Ibc호텔|JK블라썸|JW메리어트동대문스퀘어|JW메리어트호텔서울|K-그랜드호스텔동대문|K게스트하우스동대문프리미엄|L7강남바이롯데|L7명동바이롯데|L7홍대바이롯데|N285호텔인사동|SR호텔사당점|SR호텔서울마곡|Stay7명동점|WD호텔|Zip호텔|가산더스테이호텔|가산마인드호텔|강남렉시|강남멜리샤호텔|강남아르누보씨티|강남제리스플래닛|강남캠퍼스|건대드가자|건대컬리넌-1호점|건대컬리넌-2호점|건대호텔KWorld|골드리버호텔|골든서울호텔|그랜드머큐어앰배서더호텔앤레지던스서울용산|그랜드워커힐서울|그랜드인터컨티넨탈서울파르나스|그랜드하얏트서울|그리드인호텔|글래드강남코엑스센터|글래드마포|글래드여의도|길동IMT1,2|나인트리프리미어호텔명동2|나인트리프리미어호텔인사동|나인트리호텔동대문|나인트리호텔명동|남산힐호텔|노보텔스위트앰배서더서울용산|노보텔앰배서더서울강남|노보텔앰배서더서울동대문호텔앤레지던스|노보텔앰배서더서울용산|노원필름37.2호텔|뉴국제호텔|뉴서울호텔|대영호텔명동|더가든호텔|더리버사이드호텔|더리센츠동대문호텔|더블라썸연남게스트하우스|더스테이트선유|더케이호텔서울|더클래식500이그제큐티브레지던스펜타즈|더퍼스트스테이호텔|더플라자서울오토그래프컬렉션|도미인서울강남|독산3SHOTEL|독산호텔인카페|드림게스트하우스|디아티스트호텔역삼점|디어스명동|딜라이트호텔잠실|라까사호텔서울|라마다서울동대문|라마다서울신도림|라마다호텔앤스위트서울남대문|라비타호텔|라이즈오토그래프컬렉션바이메리어트|라인호텔명동|레스케이프호텔|레이크호텔|로사나호텔|로얄스퀘어호텔|로이넷호텔서울마포|롯데시티호텔구로|롯데시티호텔김포공항|롯데시티호텔마포|롯데시티호텔명동|롯데호텔서울|롯데호텔서울이그제큐티브타워|롯데호텔월드|마마스앤파파스홍대게스트하우스|머큐어앰배서더서울홍대|메리어트이그제큐티브아파트먼트서울|메이플러스서울동대문|메이필드호텔서울|명동뉴스테이인|명동멀린호텔|명동메트로호텔|명동스타힐스호텔|명동아트래블홈|목시서울인사동|몬드리안서울이태원|밀리오레호텔서울명동|반얀트리클럽앤스파서울|베니키아노블호텔|베스트웨스턴프리미어강남|베이튼호텔|보코서울강남|불광포레스타|비스타워커힐서울|사당MRG|사당티트리호텔|사당호텔카일|사보이호텔|서머셋팰리스|서울가든호텔|서울대54번가|서울맘게스트하우스|서울신라호텔|서울신촌위고인호스텔|서울앤호텔동대문|서울올림픽파크텔|서울웨스틴조선호텔|서울킴스테이9|서초라바|선릉그레이호텔|센터마크호텔서울|성신여대역더월|성신여대역샤미소|성신여대호텔디아티스트|세종호텔|센트럴관광호텔|소설호텔|소테츠프레사인서울명동|소테츠호텔즈더스프라지르서울동대문|소테츠호텔즈더스프라지르서울명동|소피텔앰배서더서울|솔라리아니시테츠명동|수송게스트하우스|수유호텔클래시|스위스그랜드호텔|스타즈호텔독산|스타즈호텔명동2호점|스탠포드호텔명동|스탠포드호텔서울|스탭인명동2|스테이비명동호텔|스테이호텔강남|슬로우스테이DA|시그니엘서울|신라스테이광화문|신라스테이구로|신라스테이마포|신라스테이삼성|신라스테이서대문|신라스테이서초|신라스테이역삼|신림돈키호텔|신림르네상스|신천A+무인호텔|신천포레스타1|신천포레스타2|신천호텔더캐슬-잠실새내점|신천엔유|신촌MAC|신촌가을|신촌넘버25|신촌라뉘|신촌라싸|신촌루씨르|신촌림|신촌모모-구이젠|신촌신디호텔|신촌앨리|신촌어반노드|신촌포레스타|써미트호텔|아리랑힐호텔동대문|아마레호텔종로|아만티호텔서울|안다즈서울강남|안테룸서울|알로프트서울강남|알로프트서울명동|앰배서더서울풀만호텔|야코리아호스텔강남점|야코리아호스텔동대문|약수프린스모텔|어반플레이스강남|업플로호스텔|에버8서비스레지던스|에이든바이베스트웨스턴청담|에이큐브호텔|여의도메리어트호텔|여의도코보스호텔|역삼PREMIERXYM|역삼리치웰|역삼린|역삼벤|역삼브라운도트|역삼스타호텔|역삼인트로호텔|역삼컬리넌|역삼호텔스타프리미어|영등포Blvd호텔오라|영등포GMS호텔|영등포그곳에|영등포데쟈트|영등포부띠크HotelSB|영등포호텔갤럭시|영등포호텔더휴|영등포호텔브릿지|오라카이대학로호텔|오라카이인사동스위츠|오라카이청계산호텔|오리엔스호텔앤레지던스|오월호텔|오크우드프리미어코엑스센터|오클라우드호텔|왕십리아모렉스|왕십리컬리넌|왕십리포레스타|용산엘르인|웨스턴코업동대문레지던스|은평씨에스에비뉴호텔|을지로코업레지던스|이비스스타일앰배서더강남|이비스스타일앰배서더서울명동|이비스스타일앰배서더서울용산|이비스앰배서더명동|이비스앰배서더인사동|이코노미호텔명동프리미어점|이태원옐로우게스트하우스|이태원인|인사동미니호텔|인사동호스텔|인사동호텔썬비|인터시티서울|인터컨티넨탈서울코엑스|임피리얼팰리스부티크호텔|잠실(방이)호텔더캐슬1호점|잠실2.4호텔|잠실HLHotel|잠실Stayhotel|잠실라비호텔|잠실루이체|잠실셀레네|잠실와우|잠실첼로|잠실호텔넘버25|잠실호텔톰지|잠실포레스타호텔|장안시그니처|조선팰리스서울강남럭셔리컬렉션호텔|종로(5가)호텔KWORLD|종로HOTELLABOUM|종로M&LUCKYHOTEL|종로THEMAYHOTEL|종로더포스트호텔|종로부티크호텔K|종로시네마|종로아비숑|종로헤르츠|종로호스텔토미|종로호텔라와|종로호텔팝리즈프리미어|창동론스타|천호HOTELH|카파스호텔|카푸치노호텔|칼리스타호텔|케니스토리인종로|케이스타메트로호텔|케이팝호텔서울역점|켄싱턴호텔여의도|코리아나호텔|코코모호텔|코코아게스트하우스|코트야드메리어트서울남대문|코트야드메리어트서울보타닉파크|코트야드메리어트서울타임스퀘어|콘래드서울|크라운파크호텔서울|크레토호텔명동|토요코인서울강남|토요코인서울동대문2|토요코인서울영등포|통통쁘띠호텔|트레블로지동대문|트레블로지명동시티홀호텔|트레블로지명동을지로호텔|트리아호텔|파라스파라서울|파로스호텔|파크하비오호텔|파크하얏트서울|파티오세븐호텔|퍼시픽호텔|페어몬트앰배서더서울|페어필드바이메리어트서울|포시즌스호텔서울|포포인츠바이쉐라톤서울강남|포포인츠바이쉐라톤서울구로|포포인츠바이쉐라톤조선서울명동|포포인츠바이쉐라톤조선서울역|프레이저플레이스센트럴서울|프레지던트호텔|하모니호텔|하우재이태원|하이서울유스호스텔|해밀톤호텔|핸드픽트호텔|헨나호텔서울명동|호스텔코리아|호텔28명동|호텔8아워즈|호텔DM|호텔U5|호텔가온골든파크동대문|호텔국도명동|호텔그레이스리서울|호텔나포레|호텔뉴브|호텔더디자이너스DDP|호텔더디자이너스건대프리미어|호텔더디자이너스동대문|호텔더디자이너스리즈강남프리미어|호텔더디자이너스서울역|호텔더디자이너스종로|호텔더디자이너스청량리|호텔더디자이너스홍대|호텔로프트|호텔리베라서울|호텔리베라청담|호텔리안|호텔릿서울역|호텔마누서울|호텔미도명동|호텔미드시티명동|호텔베뉴지|호텔베르누이서울|호텔부티크9|호텔삼정|호텔선샤인서울|호텔스카이파크동대문1호점|호텔스카이파크명동1호점|호텔스카이파크명동2호점|호텔스카이파크명동3호점|호텔스카이파크센트럴명동점|호텔스카이파크킹스타운동대문점|호텔스테이인|호텔아이린시티|호텔아트리움종로|호텔엔트라|호텔엠펠리체|호텔유리앤|호텔인나인강남|호텔인피니|호텔쿠레타케소인사동|호텔크레센도서울|호텔토마스명동|호텔페이토강남|호텔페이토삼성|호텔포코|호텔프린스서울|호텔피제이명동|홀리데이인익스프레스서울홍대|홍대나비호스텔|홍대나인브릭호텔|홍대더휴식아늑|홍대써니힐게스트하우스|화곡HOTELN|화곡Mshotel|화곡VOLL|화곡블루힐|화곡소설스미스|화곡해담채|화웬하우스hq|힐튼가든인서울강남)\b'


gra_pattern = r'\b(게스트하우스|모텔|5성|호스텔|4성|2성|3성)\b'
gu_pattern = r'\b(은평구|마포구|노원구|강남구|광진구|강북구|강서구|송파구|구로구|도봉구|금천구|서초구|종로구|동대문구|중구|영등포구|동작구|관악구|용산구|서대문구|성북구|성동구|강동구)\b'
sta_pattern = r'\b(합정역|선릉역|삼성역|길동역|역삼역|발산역|숙대입구역|구로디지털단지역|여의나루역|한강진역|장한평역|연주역|사당역|신논현역|남부터미널역|신천역|여의도역|을지로4가역|성신여대역|역삼역역|고속터미널역|성신여대입구역|신길역|신림역|광화문역|교대역|동대문역사문화공원역|성수역|공덕역|충무로역|녹사평역|오류동역|서울역|디지털미디어시티역|잠실역|동대입구역역|이대역|을지로입구|가산디지털단지역|이태원역|군자역|언주역|김포공항역|수유역|광화문|약수역|마포역|상왕십리역|왕십리역|독산역|불광역|잠실새내역|길동사거리.강동세무서역|송정역|몽촌토성역|회현역|남영역|몽촌토성역역|선정릉역|창동역|청담역|강남역|북한산우이역|건대입구역|삼성중앙역|동대입구역|천호역|시청역|버티고개역|광나루역|국회의사당역|종합운동장역|종각역|종로5가역|동묘앞역|학동역|을지로입구역|삼각지역|상수역|영등포역|서대문역|석촌고분역|오목교역|노원역|을지로|3가역|안국역|염창역|압구정역|장지역|당산역|홍대입구역|종로3가역|마곡나루역|청구역|봉은사역|구로역|청계산입구역|양재역|을지로3가역|신사역|명동역|홍제역|서울대입구역|신촌역|선유도역|용산역|신대방삼거리역|청량리역)\b'

wo1_pattern = r'\b(청담|선릉|신길|회현|서울|종합운동장|사당|독산|길동사거리|동대입구|오목교|신천|길동|삼성|삼전|신설동|을지로4가|국회의사당|강남|이태원|녹사평|염창|서대문|성신여대|수유|영등포|공덕|광나루|홍제|구로|서울대입구|안국|왕십리|충무로|동묘앞|발산|약수|오류동|이대|장지|건대|천호|김포공항|상수|구로디지털단지|봉은사|삼각지|몽촌토성|노원|장한평|신촌|까치산|석촌고분|을지로|3가|고터|숙대입구|학동|청계산입구|마포|가산디지털단지|남부터미널|청량리|남영|녹번|신대방삼거리|홍대|광화문|디지털미디어시티|광화|연주|양재|북한산우이|을지로입구|한강진|을지로3가|언주|합정|잠실새내|여의도|종각|송정|삼성중앙|당산|교대|여의나루|신논현|용산|잠실|을지로입|명동|신림|압구정|성수|종로5가|시청|청구|역삼|신사|불광|선정릉|군자|선유도|종로3가|상왕십리|창동|동역사|버티고개|마곡나루)\b'
wo2_pattern = r'\b(동대문역사문화공원|몽촌토성|명동|충무로|양재|언주|신도림|신길|회현|을지로입구|봉은사|공덕|잠실|잠실새내|선릉|시청|신사|종로3가|을지로입구|광화문)\b'
wo3_pattern = r'\b(송파|광진|도봉|서초|금천|종로|동대문|노원|강서|은평|동작|관악|강남|용산|성동|서대문|영등포|성북|강동|강북|구로|마포)\b'

# 필요한 데이터 파일 준비 
score_df = pd.read_csv('C:/Users/user/Desktop/Project/Final/webFinal/score.csv')
ht_info = pd.read_csv('C:/Users/user/Desktop/Project/Final/webFinal/호텔_리스트_최종.csv')
gu_loglat = pd.read_csv('C:/Users/user/Desktop/Project/Final/webFinal/seoul_gu_loglat.csv')
ht_map = 'C:/Users/user/Desktop/Project/Final/webFinal/hotel.json'
cat_lst =score_df.columns[1:].tolist()
level_lst = ['5성','4성','3성','모텔','게스트하우스']

ht_name_find = ht_info['ht_name'].to_list()
ht_address_find = ht_info['address'].to_list()


# 랜덤 색상 생성 함수
def random_color(opacity=1,random_state=0):
    random.seed(random_state)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgba({r}, {g}, {b}, {opacity})"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 엘라스틱서치 파트 
@app.route('/result')
def result():
    session_id = request.cookies.get('session_id')
    now = datetime.now()
    search = request.args.get('search')
    
    matches_name = re.findall(ht_name_pattern, search)
    if matches_name:
        ht_name_key = matches_name[0][0]
        ht_id_num=ht_name_find.index(ht_name_key) +1
        ht_address = ht_address_find[ht_name_find.index(ht_name_key)]
        return redirect(url_for('hotelDetail', ht_id= ht_id_num, ht_name = ht_name_key, ht_address = ht_address))


    # 검색 로그 남기기
    doc = {
                "timestamp" : now,
                "session_id" : session_id,
                "message" : search
            }
    es.index(index="log_index",  body=doc)

    # input값 전처리 하고 검색
    query_texts = preprocess_text(search)
    query_texts = re.sub(r'(\d+) 성', r'\1성', query_texts)  # 3 성 같은 숫자+성 붙이기 
    query_text = query_texts

    matches1 = re.findall(gra_pattern, query_text)
    matches2 = re.findall(gu_pattern, query_text)
    matches3 = re.findall(sta_pattern, query_text)
    matches4 = re.findall(wo1_pattern, query_text)
    matches5 = re.findall(wo2_pattern, query_text)
    matches6 = re.findall(wo3_pattern, query_text)

    # 만약 해당되는게 있다면 필터링하고 문장에서 제외
    if matches1:
        grade = matches1[0]
        query_text = re.sub(grade,'',query_text)
        query_text = preprocess_text(query_text)
    else : grade = None
    if matches2:
        gu = matches2[0]
        query_text = re.sub(gu,'',query_text)
        query_text = preprocess_text(query_text)
        print(gu, query_text)
        
        gu_lat = gu_loglat[gu_loglat['구']==gu]['latitude'].values.tolist()[0]
        gu_long = gu_loglat[gu_loglat['구']==gu]['longitude'].values.tolist()[0]
    else : 
        gu = None
        gu_lat = gu_loglat[gu_loglat['구']=='서울시']['latitude'].values.tolist()[0]
        gu_long = gu_loglat[gu_loglat['구']=='서울시']['longitude'].values.tolist()[0]
    if matches3:
        station = matches3[0]
        query_text = re.sub(station,'',query_text)
        query_text = preprocess_text(query_text)
    else : station = None
    if matches4:
        word1 = matches4[0]
        query_text = re.sub(word1,'',query_text)
        query_text = preprocess_text(query_text)
    else : word1 = None
    if matches5:
        word2 = matches5[0]
        query_text = re.sub(word2,'',query_text)
        query_text = preprocess_text(query_text)
    else : word2 = None
    if matches6:
        word3 = matches6[0]
        query_text = re.sub(word3,'',query_text)
        query_text = preprocess_text(query_text)
    else : word3 = None

    if len(query_text)<=1:query_text = query_texts #검색내역에서 전부 조건 필터링에 걸릴 경우 그냥 검색


    body ="""
        {"query": {"function_score": {"query": {"bool": {"must": [{"match": {"review": "%s"}}], "should": []}},
                                    "script_score": {"script": {"source": "cosineSimilarity(params.query_vector, 'rev_vec') + 1.0",
                                                                "params": {"query_vector": %s}}}}}, "size": 50}
    """ % (query_text,list(model.encode(query_text)))

    if gu:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"gu": {"query": gu,"boost": 10.0}}})
        body = json.dumps(body_json)
    if station:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"station": { "query": station,"boost": 10.0} }})
        body = json.dumps(body_json)
    if station:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"station2": {"query": station,"boost": 10.0}}})
        body = json.dumps(body_json)
    if grade:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"grade": {"query": grade,"boost": 10.0}}})
        body = json.dumps(body_json)
    if word1:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"word1": {"query": word1,"boost": 10.0}}})
        body = json.dumps(body_json)
    if word2:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"word2": {"query": word2,"boost": 10.0}}})
        body = json.dumps(body_json)
    if word3:
        body_json = json.loads(body)
        body_json["query"]['function_score']['query']["bool"]["should"].append({"match": {"word3": {"query": word3,"boost": 10.0}}})
        body = json.dumps(body_json)


    res = es.search(index='review_list', body=body) #검색

    next_ls = []
    for i in range(len(res['hits']['hits'])):
        next_ls.append([res['hits']['hits'][i]['_source']['ht_id'],
                        res['hits']['hits'][i]['_score'],
                        res['hits']['hits'][i]['_source']['cat_id'],
                        res['hits']['hits'][i]['_source']['date'],
                        res['hits']['hits'][i]['_source']['review'],
                        res['hits']['hits'][i]['_source']['label'],
                        ]) 
    # next_ls for문 믿에
    if len(next_ls) == 0:
        return render_template('nodata.html')
    
    next_df = pd.DataFrame(next_ls,columns=['ht_id','score','cat_id','date','review','label'])
    print(query_text)
    print(next_df)
    next_df=next_df.drop_duplicates(['ht_id'], keep='first')
    print(next_df)
    next_df = next_df[next_df['score']>=15]
    next_df.reset_index(drop=True, inplace=True)

    ht_ls = next_df['ht_id'].to_list()# 중복 제거하고 호텔 아이디 출력
    cnt = len(ht_ls)
    next_df.set_index('ht_id',inplace=True)
    
    if len(ht_ls) == 0:
        return render_template('nodata.html')
    
    result=pd.DataFrame()
    for i in ht_ls:
        result=pd.concat([result,ht_info[ht_info['ht_id']==i]])
    result.reset_index(drop=True, inplace=True)
    result.set_index('ht_id',inplace=True)


    

    
    num = [1,2,3,4,5]
    idx_ = num*(cnt//5) + num[0:cnt%5]
    
    # print(ht_ls)
    
    with open(ht_map,'r',encoding='utf-8') as f:
        hotel_map = json.load(f)
    add_json = []
    for k in ht_ls:
        for item in hotel_map:
            if item['ht_id'] == k:
                add_json.append(item)
    print(add_json)
    
    df = score_df.copy()   
    df = df[df['ht_id'].isin(ht_ls)]
    pick_avg = []
    for c in cat_lst :
        pick_avg.append(round(df[c].mean(skipna=True),2))
    sc_df = df.set_index('ht_id')
        
    seoul_avg = []
    for c in cat_lst :
        seoul_avg.append(round(score_df[c].mean(skipna=True),2))   
        
    sim = {}
    sim_id = {}
    sim_add= {}
    for i in ht_ls :
        sim[i] = []
        sim_id[i] = []
        sim_add[i] = []
        for j in cbf.top_match(i,5,cbf.sim_hotel):
            sim[i].append(j[2])
            sim_id[i].append(j[1])
            sim_add[i] += ht_info['address'][ht_info['ht_id']==j[1]].values.tolist()
    

    return render_template('result.html',search = search, cnt = cnt, res = result, next_df = next_df,
                           zip=zip,idx_=idx_,map_db = add_json,gu_long = gu_long , gu_lat = gu_lat,
                           seoul_avg = seoul_avg ,pick_avg = pick_avg,score_df=sc_df,sim=sim,sim_id = sim_id, sim_add=sim_add,cat_lst = cat_lst)

@app.route('/pick')
def pick():
    gu_lst = list(ht_info['구'].unique()[:-1])
    gu_lst.sort()
    gu_lst2 = ['선택안함']
    gu_lst2 += gu_lst
    return render_template('pick.html',cat_lst = cat_lst, gu_lst = gu_lst2,level_lst = level_lst)


# 카테고리 선택 파트 
@app.route('/show',methods=['POST'])
def get_category():
    '''
    넘길 정보 : ht_lst, add_json, ht_name_lst, score // 서울 평균 과 추천 평균 이랑 비교해서 레이더 보여주기 
    '''
    # 1. 지역으로 거르기(지역선택안하면 패스)
    gu = request.form['gu']    
    gu2  = request.form['gu2']
    if gu =='선택안함' :
        gu_ht = ht_info   
        gu_lat = gu_loglat[gu_loglat['구']=='서울시']['latitude'].values.tolist()[0]
        gu_long = gu_loglat[gu_loglat['구']=='서울시']['longitude'].values.tolist()[0]
        gu_send = ''
    else:
        gu_lat = gu_loglat[gu_loglat['구']==gu]['latitude'].values.tolist()[0]
        gu_long = gu_loglat[gu_loglat['구']==gu]['longitude'].values.tolist()[0]
        gu_send = gu
        if gu2 == '선택안함':
            gu_ht = ht_info[ht_info['구']==gu]
        else:
            gu_ht = ht_info[ht_info['구'].isin([gu,gu2])]   
            
    # print(gu_long, gu_lat)
            
    # 2. 등급으로 거르기(전체 선택시 패스)
    level = request.form.getlist('level_checkbox')
    if len(level) == 5 or len(level)==0:
        level_ht  = gu_ht
    else :
        for i in range(len(level)):
            if '성' in level[i] :
                level[i] = level[i].split('성')[0] 
        level_ht = gu_ht[gu_ht['등급'].isin(level)] 
            
    # 3. 점수 계산하기 
        # 상위 10개 리스트 뽑아줄건데, 전체 평점 중 상위 몇 %인지는 보여줘야 할 것 같음 
    cat_dict={}
    df = score_df.copy()    
    # 3.1 지역과 등급으로 필터링 된 숙소들만 가지고 점수 산정
    df = pd.merge(level_ht['ht_id'],df,left_on='ht_id',right_on='ht_id',how='left')
    df.dropna(inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    # 3.2 웹에서 각 카테고리에 대한 가중치 받아와서 딕셔너리 저장
    for c in cat_lst:
        value = float(request.form[c])
        cat_dict[c] = value
    
    # 3.3 가중치를 반영한 각 호텔에 대한 점수를 sc 에 합한 후 score 리스트에 저장
    score = []
    for i in range(df.shape[0]):
        sc = 0 
        c = 0 
        for cat in cat_dict: 
            if df.loc[i,cat] == np.nan:
                continue                
            sc += (df.loc[i,cat] * cat_dict[cat])
            c+= 1
        score.append(sc/c)
        
    # 3.4 각 호텔에 대한 최종 점수 컬럼['score'] 지정 -> 최대 상위 20개 숙소 전달
    df['score'] = score
    df = df.sort_values('score',ascending=False)
    df.reset_index(drop=True, inplace=True)
    df = df.iloc[:20,:]
    # print(df)
    ht_lst = df.iloc[:,0].tolist()
    print('---호텔 리스트---')
    print(ht_lst)
    # sc_df = score_df[score_df['ht_id'].isin(ht_lst)]
    sc_df = df.drop(columns=['score'])
    # print(test)
    sc_df.reset_index(drop=True,inplace=True)
    print('---점수정보---')    
    # print(sc_df)
    
    ht_data = level_ht[level_ht['ht_id'].isin(ht_lst)]
    ht_data.reset_index(drop=True, inplace=True)
    ht_data  = pd.merge(sc_df['ht_id'],ht_data,how='left')
    print('---호텔정보---')
    ht_data = ht_data.set_index('ht_id')
    # print(ht_data)
    # print(sc_df)
    
    pick_avg = []
    for c in cat_lst :
        pick_avg.append(round(sc_df[c].mean(skipna=True),2))
        
    seoul_avg = []
    for c in cat_lst :
        seoul_avg.append(round(score_df[c].mean(skipna=True),2))   
    sc_df = sc_df.set_index('ht_id')
        
    # 유사도 or 상관계수 기반 추천 리스트 보내기   
    sim = {}
    sim_id = {}
    sim_add = {}
    for i in ht_lst :
        sim[i] = []
        sim_id[i] = []
        sim_add[i] = []
        for j in cbf.top_match(i,5,cbf.sim_hotel):
            sim[i].append(j[2])
            sim_id[i].append(j[1])
            sim_add[i] += ht_info['address'][ht_info['ht_id']==j[1]].values.tolist()
    print('sim============')
    # print(sim)
    # print(sim_id)
    # print(sim_add)
 
        
    # 4. 지도 시각화 데이터 보내기 
    ## 필요한거!! 구 지정되어있으면 구 중앙 좌표도 같이 보내줘야 할듯-> 처음 화면 띄울 때 해당 구로 보여줘야 하니까 
    with open(ht_map,'r',encoding='utf-8') as f:
        hotel_map = json.load(f)
    add_json = []
    for k in ht_lst:
        for item in hotel_map:
            if item['ht_id'] == k:
                add_json.append(item)
                
    num = [1,2,3,4,5]
    idx_ = num*(len(ht_lst)//5) + num[0:len(ht_lst)%5]
    
    # print(gu_send)
                
    # print(f'지역 : {gu}')
    # print(f'등급 : {level}')
    # print(add_json)
    return render_template('show.html',map_db = add_json,res=ht_data,score_df =sc_df,cat_lst=cat_lst,
                           pick_avg=pick_avg,seoul_avg=seoul_avg ,gu_long = gu_long , gu_lat = gu_lat ,
                           sim=sim,sim_id = sim_id,sim_add=sim_add, zip=zip,idx_=idx_,gu_send = gu_send)


# 엘라스틱서치 파트 
@app.route('/hotel', methods=['GET'])
def hotelDetail():
    # search_key 안들어오는 경우 확인하기
    search_key = request.args.get('search_key')
    ht_id = request.args.get('ht_id')
    hotel = request.args.get('ht_name')
    
    score = request.args.get('score')
    df_cat = request.args.get('cat_id')
    df_date = request.args.get('df_date')
    df_review = request.args.get('df_review')
    ht_address = request.args.get('ht_address')

    
    print(ht_id)
    sim = [hotel]
    sim_id = [int(ht_id)]
    sim_add = [ht_address]
    for j in cbf.top_match(int(ht_id),5,cbf.sim_hotel):
        sim.append(j[2])
        sim_id.append(j[1])
        sim_add += ht_info['address'][ht_info['ht_id']==j[1]].values.tolist()
    idx_ = [1,2,3,4,5]    
    
    print(sim)
    print(sim_id)
    
    # score_df - raderChart
    tem= score_df[score_df['ht_id'].isin(sim_id)]
    temp = pd.DataFrame({'ht_id':sim_id})
    ht = ht_info[['ht_id','ht_name']][ht_info['ht_id'].isin(sim_id)]
    dt = pd.merge(ht,tem)
    dt = pd.merge(temp,dt)
    dt.fillna(0,inplace=True)
    print(dt)
    
    rader_dt = {
        'labels': cat_lst,
        'datasets': [
        ]
    }
    
    for i in range(6):
        dict = {}
        dict['label'] = dt.iloc[i,1]
        dict['data'] = dt.iloc[i,2:].values.tolist()
        dict['backgroundColor'] = random_color(0.2,i+20)
        dict['borderColor'] = random_color(1,i+20)
        dict['borderWidth'] = 1
        rader_dt['datasets'].append(dict)
    
    
    # 긍정리뷰 보내기 - 카테고리 분류 : pos_rev
    # 가성비
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 1}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_1 = es.search(index='review_list', body=body)
    cnt_1 = len(rev_1['hits']['hits'])

    # 친절
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 2}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_2 = es.search(index='review_list', body=body)
    cnt_2 = len(rev_2['hits']['hits'])

    # 청결
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 3}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_3 = es.search(index='review_list', body=body)
    cnt_3 = len(rev_3['hits']['hits'])

    # 주변시설
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 4}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_4 = es.search(index='review_list', body=body)
    cnt_4 = len(rev_4['hits']['hits'])

    # 주차
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 5}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_5 = es.search(index='review_list', body=body)
    cnt_5 = len(rev_5['hits']['hits'])
    # 조식
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 6}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_6 = es.search(index='review_list', body=body)
    cnt_6 = len(rev_6['hits']['hits'])
    # 방음
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 7}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_7 = es.search(index='review_list', body=body)
    cnt_7 = len(rev_7['hits']['hits'])
    # 위치
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 8}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_8 = es.search(index='review_list', body=body)
    cnt_8 = len(rev_8['hits']['hits'])
    # 비품
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 9}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_9 = es.search(index='review_list', body=body)
    cnt_9 = len(rev_9['hits']['hits'])
    # 시설
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 10}},
        {"match": {"label": 1}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_10 = es.search(index='review_list', body=body)
    cnt_10 = len(rev_10['hits']['hits'])

    # 부정리뷰 보내기 - 카테고리 분류 : neg_rev
# 가성비
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 1}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_1_0 = es.search(index='review_list', body=body)
    cnt_1_0 = len(rev_1_0['hits']['hits'])

    # 친절
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 2}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_2_0 = es.search(index='review_list', body=body)
    cnt_2_0 = len(rev_2_0['hits']['hits'])

    # 청결
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 3}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_3_0 = es.search(index='review_list', body=body)
    cnt_3_0 = len(rev_3_0['hits']['hits'])

    # 주변시설
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 4}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_4_0 = es.search(index='review_list', body=body)
    cnt_4_0 = len(rev_4_0['hits']['hits'])

    # 주차
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 5}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_5_0 = es.search(index='review_list', body=body)
    cnt_5_0 = len(rev_5_0['hits']['hits'])
    # 조식
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 6}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_6_0 = es.search(index='review_list', body=body)
    cnt_6_0 = len(rev_6_0['hits']['hits'])
    # 방음
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 7}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_7_0 = es.search(index='review_list', body=body)
    cnt_7_0 = len(rev_7_0['hits']['hits'])
    # 위치
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 8}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_8_0 = es.search(index='review_list', body=body)
    cnt_8_0 = len(rev_8_0['hits']['hits'])
    # 비품
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 9}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_9_0 = es.search(index='review_list', body=body)
    cnt_9_0 = len(rev_9_0['hits']['hits'])
    # 시설
    body= """
    {"query": {"bool": {"must": [{"match": {"ht_name": "%s"}},
        {"match": {"cat_id": 10}},
        {"match": {"label": 0}}]}},
    "size": 100, "sort":[{"date":{"order":"desc"}}]} """ % (hotel)
    rev_10_0 = es.search(index='review_list', body=body)
    cnt_10_0 = len(rev_10_0['hits']['hits'])


    return render_template('hotelDetail.html', ht_id = ht_id, hotel = hotel, search_key = search_key, score = score, df_cat = df_cat,
                           df_date = df_date, df_review = df_review,
                           cnt_1 = cnt_1, cnt_2 = cnt_2, cnt_3 = cnt_3, cnt_4 = cnt_4, cnt_5 = cnt_5,
                            cnt_6 = cnt_6, cnt_7 = cnt_7, cnt_8 = cnt_8,cnt_9 = cnt_9,cnt_10 = cnt_10,
                            cnt_1_0 = cnt_1_0, cnt_2_0 = cnt_2_0, cnt_3_0 = cnt_3_0, cnt_4_0 = cnt_4_0, cnt_5_0 = cnt_5_0,
                            cnt_6_0 = cnt_6_0, cnt_7_0 = cnt_7_0, cnt_8_0 = cnt_8_0,cnt_9_0 = cnt_9_0,cnt_10_0 = cnt_10_0,
                            rev_1 = rev_1['hits']['hits'], rev_2= rev_2['hits']['hits'], rev_3=rev_3['hits']['hits'], rev_4= rev_4['hits']['hits'],
                            rev_5= rev_5['hits']['hits'],rev_6= rev_6['hits']['hits'],rev_7= rev_7['hits']['hits'],rev_8= rev_8['hits']['hits'],
                            rev_9= rev_9['hits']['hits'],rev_10= rev_10['hits']['hits'],
                            rev_1_0 = rev_1_0['hits']['hits'], rev_2_0= rev_2_0['hits']['hits'], rev_3_0=rev_3_0['hits']['hits'], rev_4_0= rev_4_0['hits']['hits'],
                            rev_5_0= rev_5_0['hits']['hits'],rev_6_0= rev_6_0['hits']['hits'],rev_7_0= rev_7_0['hits']['hits'],rev_8_0= rev_8_0['hits']['hits'],
                            rev_9_0= rev_9_0['hits']['hits'], rev_10_0= rev_10_0['hits']['hits'],ht_address=ht_address,
                            sim=sim, sim_id = sim_id, sim_add = sim_add,zip=zip,idx_ = idx_,rader_dt = rader_dt)
  


# 테스트용 페이지 
@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':    
    # app.run(host='192.168.10.29' ,debug=True)
    app.run(port='80' ,debug=True)