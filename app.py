import tkinter as tk
from tkinter import scrolledtext
import joblib
import re, string
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))
model = joblib.load('spam_pipeline.joblib')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = [t for t in text.split() if t not in STOPWORDS]
    return ' '.join(tokens)

def check_spam():
    msg = text_box.get("1.0", "end-1c").strip()
    if not msg:
        result_label.config(text="Please enter a message!", fg="orange")
        return
    msg_clean = clean_text(msg)
    pred = model.predict([msg_clean])[0]

    label = "SPAM" if pred == 1 else "NOT SPAM"
    color = "red" if pred == 1 else "green"
    result_label.config(text=f"{label}", fg=color, font=("Arial", 14, "bold"))

root = tk.Tk()
root.title("Spam Message Classifier")
root.geometry("600x400")

tk.Label(root, text="Enter a message to classify:", font=("Arial", 12)).pack(pady=10)
text_box = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
text_box.pack(padx=10, pady=10)

tk.Button(root, text="Check Spam", command=check_spam, font=("Arial", 12)).pack(pady=5)
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
