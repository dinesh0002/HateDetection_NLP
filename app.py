# Importing Libraries for the streamlit web application
import streamlit as st
import re
import nltk
import pickle
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword = set(stopwords.words('english'))
import keras
from keras.preprocessing import sequence


# loading the model using keras load models
load_model = keras.models.load_model("hate_detectioin.h5")
with open('tokenizer.pickle', 'rb') as handle:
    load_tokenizer = pickle.load(handle)

# Function to remove all the unwanted text from the text
def cleaning_text(text):
   text = str(text).lower()
   text = re.sub('\[.*?\]', '', text)
   text = re.sub('https?://\S+|www\.\S+', '', text)
   text = re.sub('<.*?>+', '', text)
   text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
   text = re.sub('\n', '', text)
   text = re.sub('\w*\d\w*', '', text)
   text = [word for word in text.split(' ') if word not in stopword]
   text=" ".join(text)
   text = [stemmer.stem(word) for word in text.split(' ')]
   text=" ".join(text)
   return text

def text_2_vector(text):
  seq = load_tokenizer.texts_to_sequences(text)
  return seq

def predict_hate(text):
  seq = load_tokenizer.texts_to_sequences(text)
  padded = sequence.pad_sequences(seq, maxlen = 250)
  pred = load_model.predict(padded)
  return pred

def classify_hate(text):
  probability = predict_hate(text)
  if probability < 0.5:
    return ("NO HATE FOUND")
  else:
    return ("HATE AND ABUSIVE FOUND")


def main():
  st.title("Hate Speech Detection App")
  menu = ["Home","Monitor","About"]
  choice = st.sidebar.selectbox("Menu", menu)

  if choice == "Home":
    st.subheader("Home --  Detect Hate Speech")

    with st.form(key = 'Hate speech Detection Form'):
      raw_text = st.text_area("Type Here")
      submit_text = st.form_submit_button(label = 'Predict')

    if submit_text:
      col1, col2 = st.columns(2)

      with col1:
        st.success("Text after Cleaning")
        cleaned_text = [cleaning_text(raw_text)]
        st.write(cleaned_text)

        st.success("Predictions")
        predictions = predict_hate(cleaned_text)
        prediction = predictions * 100
        st.write("Predicted Hate Percentage is", prediction)

      with col2:
        st.success("Classification")
        classify = classify_hate(cleaned_text)
        st.write(classify)
    st.write("This is a Hate Speech Detection App")
    st.write("Done by Dinesh Kumar")
    st.write("Gitam University")



  elif choice == "Monitor":
    st.subheader("Monitor App")

  else:
    st.subheader("About")
    st.write("This is a Hate Speech Detection app")
    st.write("Done by Dinesh Kumar")
    st.write("Gitam University, Hyderabad")

if __name__ == '__main__':
  main()
