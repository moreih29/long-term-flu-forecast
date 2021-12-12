from konlpy.tag import Mecab, Okt
from multiprocessing import Manager
from tqdm import tqdm
import re
import platform
import warnings
import parmap
import psycopg2 as pg2


"""
트윗, 뉴스의 불필요한 부분을 제거함
해시태그, 리트윗, 이모지 등...
품사별로 분리해서 배열 형태로 리턴
"""

def clean_sentence(string):
    # 특정 문자열을 제외한 나머지 문자열 제거
    string = re.sub(r"@[A-Za-z0-9ㄱ-ㅎ가-힣!@$%^&()_]*", " ", string) # @이후 문자열 제거
    string = re.sub(r"#[A-Za-z0-9ㄱ-ㅎ가-힣!@$%^&()_]*", " ", string) # #이후 문자열 제거
    string = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9_.+-]+", " ", string) # 이메일 주소 제거
    string = re.sub(r"(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))", " ", string) # URL제거
    string = re.sub(r"\[(.*?)\]", " ", string) # 대괄호안 문자 제거
    string = re.sub(r"[^A-Za-z0-9가-힣]", " ", string) # 특수문자 & ㅠㅠㅋㅋ 제거
    string = re.sub(r" +", " ", string)
    string = string.strip()
    
    return string

def _tokenize(string, result, tokenizer_name):
    if tokenizer_name == 'mecab':
        tokenizer = Mecab()
        string = tokenizer.nouns(string)
        string = [word for word in string if len(word) > 1]
        result.append(string)
    elif tokenizer_name == 'okt':
        tokenizer = Okt()
        string = tokenizer.nouns(string)
        string = [word for word in string if len(word) > 1]
        result.append(string)
    else:
        return -1

def tokenize(sentences, tokenizer_name='okt', is_multi=True):
    warnings.filterwarnings(action='ignore')
    assert tokenizer_name == 'mecab' or tokenizer_name == 'okt', 'choose one of okt and mecab for tokenizer_name='
    assert tokenizer_name != 'mecab' or platform.system() != 'Windows', 'mecab is unavailable on Windows'
    
    if is_multi:
        # 멀티 프로세싱을 위한 코드
        sentence_list = Manager().list([])
        parmap.map(_tokenize, sentences, sentence_list, tokenizer_name, pm_pbar=True, pm_processes=8)
        sentence_list = list(sentence_list)
    else:
        sentence_list = []
        for sentence in tqdm(sentences):
            _tokenize(sentence, sentence_list, tokenizer_name)

    return sentence_list


# Dataframe 안의 string 형태의 배열을 배열로 변환
def str_to_list(string):
    return string[1:-1].replace('\'', '').split(', ')


# [[w1, w2, ..., wn], [...], [...]] 형태의 texts에서 각 단어의 출현 빈도수 카운트
def word_count(texts, num_words=None):
    word_count = {}
    for l in texts:
        for w in l:
            if w in word_count:
                word_count[w] += 1
            else:
                word_count[w] = 1
    num_words = len(word_count) if num_words is None else num_words
    word_count = {w:c for w, c in 
                  sorted(word_count.items(), key=(lambda x: x[1]), reverse=True)[:num_words]}
    
    return word_count


def weekly_word_count(texts, counter):
    result_dict = {}
    for w in counter:
        result_dict[w] = 0
        for l in texts:
            if w in l:
                result_dict[w] += 1
    return result_dict


def merge_dict(dict_list):
    tmp = {}
    for d in dict_list:
        for k, v in d.items():
            if k in tmp:
                tmp[k] += v
            else:
                tmp[k] = v
    return tmp


"""
DBConnector
"""


class DBconnector:
    def __init__(self):
        self.host = 'epidemic.co.kr'
        self.port = '54321'
        self.dbname = 'BJang'
        self.user = 'postgres'
        self.password = 'Jang1234'

    def __enter__(self):
        self.conn = pg2.connect(host=self.host, port=self.port, dbname=self.dbname,
                                user=self.user, password=self.password)
        self.cur = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def get(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()