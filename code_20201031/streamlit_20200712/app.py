import streamlit as st

import spacy
import gensim
from gensim.summarization import summarize
from textblob import TextBlob
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def text_analyzer(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    tokens = [token for token in doc]
    all_data = [f'"Tokens": {token.text}, "Lemma": {token.lemma_}' for token in doc]
    return all_data

def entity_analyzer(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    tokens = [token for token in doc]
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    all_data = [f"Tokens:{tokens}, Entity: {entities}"]
    return entities

def sumy_summarizer(doc):
    parser = PlaintextParser.from_string(doc, Tokenizer('english'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    return ' '.join([str(sentence) for sentence in summary])

def main():
    st.title("NLP with Streamlit")
    st.subheader("Natural Language Processing on the go")

    # Tokenization
    if st.checkbox("Show tokens and lemmas"):
        st.subheader("Tokenize your text")
        mess = st.text_area("Enter your text", "Type here", key="tokenization")
        if st.button("Analyze"):
            result = text_analyzer(mess)
            st.json(result)

    # Named Entity
    if st.checkbox("Show Named Entities"):
        st.subheader("Extract Entities from your text")
        mess = st.text_area("Enter your text", "Type here", key="named_entity")
        if st.button("Extract"):
            result = entity_analyzer(mess)
            st.json(result)
    
    # Sentiment Analysis
    if st.checkbox("Show Sentiments Analysis"):
        st.subheader("Analyze your text")
        mess = st.text_area("Enter your text", "Type here", key="sentiment_analysis")
        if st.button("Analyze"):
            blob = TextBlob(mess)
            result = blob.sentiment
            st.success(result)

    # Text Summarization
    if st.checkbox("Show Text Summarization"):
        st.subheader("Summarize your text")
        mess = st.text_area("Enter your text", "Type here", key="text_summarization")
        summary_option= st.selectbox("Choice Your Summarizer", ("gensim", "sumy"))
        if st.button("Summarize"):
            if summary_option == "gensim":
                st.text("Using Gensim...")
                result = summarize(mess)
            elif summary_option == "sumy":
                st.text("Using Sumy...")
                result = sumy_summarizer(mess)
            else:
                st.warning("Using default Summarizer")
                st.text("Using Gensim...")
                result = summarize(mess)

            st.success(result)

    st.sidebar.subheader("About App")
    st.sidebar.text("NLP with Streamlit")
    st.sidebar.info("Something with Streamlit")

if __name__ == "__main__":
    main()