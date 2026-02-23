import urllib.request
from bs4 import BeautifulSoup
import re
import sys
def find_all_text(url):
    header = {
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request(url, headers=header)
    response=urllib.request.urlopen(req)
    data=response.read().decode("utf-8")
    soup=BeautifulSoup(data,"html.parser")
    text=soup.get_text()
    text=text.lower()  
    text = re.sub(r'[^a-z0-9 ]', '', text)  
    return text.split()

def find_count(f):
    word_count={}
    for word in f:
        if word in word_count:
            word_count[word]+=1
        else:
            word_count[word]=1
    return word_count

def hash_function(word, p=53, m=2**64):
    hash_value = 0
    power = 1
    for char in word:
        hash_value = (hash_value + ord(char) * power) % m
        power = (power * p) % m
    
    return hash_value

def find_fingerprint(freq_dic):
    bits=64
    vector_value=[0]*bits
    for word,weight in freq_dic.items():
        h=hash_function(word)
        for i in range(bits):
            mask=1<<i
            if(h&mask):
                vector_value[i]+=weight
            else:
                vector_value[i]-=weight
    fingerprint=0
    for i in range(bits):
        if vector_value[i]>0:
           fingerprint |= (1 << i)
    return fingerprint


def find_duplicate(url1,url2):
    bits=64
    f1=find_all_text(url1)
    f2=find_all_text(url2)
    freq_count_url1=find_count(f1)
    freq_count_url2=find_count(f2)
    doc1_fingerprint=find_fingerprint(freq_count_url1)
    doc2_fingerprint=find_fingerprint(freq_count_url2)
    count_common_bit=0
    for i in range(bits):
        mask=1<<i
        if((doc1_fingerprint & mask)==(doc2_fingerprint & mask)):
            count_common_bit+=1
    similarity = (count_common_bit / 64) * 100
    print("Similarity Percentage:", similarity, "%")
url1=sys.argv[1]
url2=sys.argv[2]
find_duplicate(url1,url2)
    

    

    