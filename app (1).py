import streamlit as st
import nlpcloud

# Simulated in-memory database
if 'database' not in st.session_state:
    st.session_state.database = {}

# Session variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# NLPCloud client setup
API_KEY = "2b58d7fb9af09e617ee525e78c7766b6d8c5bb61"  # replace with your real key
MODEL = "distilbert-base-uncased-emotion"


def register():
    st.subheader("Register")
    name = st.text_input("Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        if email in st.session_state.database:
            st.error("Email already exists.")
        else:
            st.session_state.database[email] = [name, password]
            st.success("Registration successful. Please log in.")


def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        db = st.session_state.database
        if email in db and db[email][1] == password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful.")
        else:
            st.error("Invalid email or password.")


def sentiment_analysis():
    st.subheader("Sentiment Analysis")
    para = st.text_area("Enter paragraph for sentiment analysis")

    if st.button("Analyze"):
        client = nlpcloud.Client(MODEL, API_KEY, gpu=False, lang="en")
        response = client.sentiment(para)

        scores = response["scored_labels"]
        top_sentiment = max(scores, key=lambda x: x["score"])
        st.success(f"Predicted Emotion: {top_sentiment['label'].capitalize()}")

        # Show all scores
        st.write("Full Scores:")
        for s in scores:
            st.write(f"{s['label'].capitalize()}: {s['score']:.2f}")


def main():
    st.title("🧠 NLP Web App with Streamlit + NLPCloud")

    menu = ["Home", "Register", "Login"] if not st.session_state.logged_in else ["Sentiment Analysis", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome! Please register or login to use NLP features.")
    elif choice == "Register":
        register()
    elif choice == "Login":
        login()
    elif choice == "Sentiment Analysis":
        sentiment_analysis()
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.success("Logged out.")


if __name__ == '__main__':
    main()
