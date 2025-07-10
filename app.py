import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re

st.set_page_config(page_title="Phishing URL Tespiti", layout="wide", page_icon="🔍")

def extract_features_from_url(url):
    features = [
        len(url),
        url.count('.'),
        url.count('http'),
        url.count('www'),
        int(url.endswith('.com')),
        int('phishing' in url.lower()),
        int('login' in url.lower()),
        int('secure' in url.lower()),
        int('account' in url.lower()),
        int('update' in url.lower()),
        int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        len(url.split("//")[-1].split("/")[0]),
        sum(1 for c in url if c.isupper()),
        sum(1 for c in url if c.islower()),
        sum(1 for c in url if c in "!@#$%^&*()_+-=[]{}|;':\",.<>?/"),
        sum(1 for c in url if c.isdigit()),
        url.count(' '),
        url.count('_'),
        url.count('-'),
        url.count('/'),
        len(url.split()),
        sum(len(word) for word in url.split()),
        len(url.replace(" ", ""))
    ]
    while len(features) < 30:
        features.append(0)
    return features


@st.cache_data
def load_and_train_model():
    df = pd.read_csv('phishing_data.csv', on_bad_lines='skip')


    X = df['URL'].apply(extract_features_from_url).tolist()
    X = pd.DataFrame(X)


    y = df['Label'].apply(lambda x: 1 if str(x).strip().lower() == 'bad' else 0)


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model


model = load_and_train_model()


st.title("🔍 Phishing URL Tespiti")
st.markdown("Bu araç, girdiğiniz URL'nin phishing olup olmadığını tahmin eder.")

url_input = st.text_input("🔗 Lütfen bir URL girin:")

def is_valid_url_format(url):
    return url.startswith("http://") or url.startswith("https://")

if st.button("🔬 Analiz Et"):
    if not url_input:
        st.warning("⚠️ Lütfen bir URL girin.")
    elif not is_valid_url_format(url_input.strip().lower()):
        st.warning("⚠️ Geçerli bir URL girin. 'http://' veya 'https://' ile başlamalı.")
    else:
        features = extract_features_from_url(url_input)
        prediction = model.predict(np.array(features).reshape(1, -1))[0]
        if prediction == 1:
            st.error("❌ Bu URL bir **phishing saldırısı** olabilir!")
        else:
            st.success("✅ Bu URL güvenli görünüyor.")
