import re
import pandas as pd

abusive = pd.read_csv('data/abusive.csv', encoding='utf-8')
new_kamusalay = pd.read_csv('data/new_kamusalay.csv', encoding ='latin-1')
kamus_alay_new = {}
for k,v in new_kamusalay.values:
    kamus_alay_new[k] = v
    
def processing_word(input_text):
    new_text = [] 
    new_new_text = []
    text = input_text.split(" ") 
    for word in text:
        if word in abusive['ABUSIVE'].tolist():# check word di dalam list_of_abusive_words
            continue 
        else:
            new_text.append(word) 
   
    for word in new_text:
        new_word = kamus_alay_new.get(word, word) # check ke new_kamus_alay, apakah word ada di dictionarynya. kalau ga ada, return word yang sama. kalau ada, kembalikan value barunya (value yang ada di dict)
        new_new_text.append(new_word)
    
    text = " ".join(new_new_text)
    
    return text

def cleansing_data(text):
    text= text.lower()
    text=  re.sub(r'&amp', ' ', text) #menghapus &amp
    text= re.sub(r'user', ' ', text) #menghilangkan kata yang double 
    text= re.sub(r'#\w+',' ', text) #menghapus hastag
    text = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "NOMOR_TELEPON", text) 
    text= re.sub(r'\\[0-9A-z]{2,}',' ', text) # \\khusus
    text= re.sub(r'\\[0-9A-z]',' ', text) #menghapus \\n
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL', text)
    text= re.sub(r'[^a-zA-Z\s]',' ', text) #menghilangkan huruf dengan karakter khusus
    text= re.sub(r'[^\w\s]',' ', text) #menghilangkan tanda baca
    text= re.sub(r'\s+', ' ', text) #menghapus spasi
    text= re.sub(r'\t+', '\t ', text) #menghapus tab
    text= re.sub(r'RT[\s]+', ' ', text) #menghapus RT
    text= re.sub(r'rt[\s]+', ' ', text) #menghapus rt
    text= text.strip()
    text= processing_word(text)
    
    return text