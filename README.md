🌍 AI Language Translator for Travelers

An advanced, modern and visually polished Streamlit application that helps travelers translate languages instantly, listen to pronunciations, use common travel phrases, and even work in offline mode with cached translations.

✨ Features

🔤 Translate between 12+ languages

🗣️ Text-to-Speech for both input & translated text

📘 Travel Phrasebook with one-click insertion

📜 Translation History (up to 50 records) with reload option

🌙 Dark Mode

📴 Offline Mode (Simulated) using cached translations

⚙️ Formal/Casual tone selection

⚡ Auto-Translate mode

🎧 Adjustable speech rate

🎨 Beautiful UI with custom CSS & responsive layout

📁 Project Structure
.
├── app.py
├── README.md
├── requirements.txt
└── assets/

🛠 Installation
1️⃣ Clone the repository
git clone https://https://github.com/Riss620/AIproject
cd ai-language-translator

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

3️⃣ Install dependencies
pip install -r requirements.txt


Typical requirements.txt:

streamlit
gTTS
requests
pandas

4️⃣ Run the app
streamlit run app.py

🎯 How to Use

Select source and target languages

Enter text and click Translate

Listen to audio pronunciations

Use travel phrases with one click

Adjust settings like dark mode, offline mode, speech rate

Browse your translation history

🚀 Deployment
Streamlit Cloud

Push code to GitHub

Go to https://share.streamlit.io

Select your repository

Set app.py as the entry point

Deploy instantly

📦 Technologies Used

Python 3

Streamlit

gTTS

Pandas

Custom CSS / JS

Base64 Audio Encoding

🧩 Future Improvements

Live translation API integration (Google, DeepL, Gemini)

Voice input (Speech-to-Text)

More phrasebook categories

Multi-language UI

Save history to file

🤝 Contributing

Contributions are welcome!
Open an issue or submit a pull request.

📝 License

MIT License
