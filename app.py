import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
import os
from gtts import gTTS
import base64
from io import BytesIO
import pickle

# Page configuration
st.set_page_config(
    page_title="AI Language Translator for Travelers",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def add_custom_css():
    st.markdown("""
        <style>
            .main-header {
                font-size: 2rem;
                color: #3949ab;
                text-align: center;
                margin-bottom: 1rem;
            }
            .dark-theme .main-header {
                color: #8ab4f8;
            }
            .subheader {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 1rem;
            }
            .card {
                padding: 1.5rem;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            .dark-theme .card {
                background-color: #222244;
                color: #f0f0f0;
            }
            .feature-card {
                border-left: 4px solid #3949ab;
                padding: 0.8rem;
                background-color: #f5f7ff;
                border-radius: 0 8px 8px 0;
                margin-bottom: 0.8rem;
            }
            .dark-theme .feature-card {
                background-color: #16213e;
                border-left: 4px solid #8ab4f8;
            }
            .phrase-item {
                padding: 0.5rem;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            .phrase-item:hover {
                background-color: #f0f0f0;
            }
            .dark-theme .phrase-item:hover {
                background-color: #333355;
            }
            .history-item {
                padding: 0.8rem;
                border-bottom: 1px solid #eee;
                cursor: pointer;
            }
            .history-item:hover {
                background-color: #f5f5f5;
            }
            .dark-theme .history-item:hover {
                background-color: #333355;
            }
            .footer {
                text-align: center;
                margin-top: 2rem;
                color: #666;
                font-size: 0.8rem;
            }
            .dark-theme .footer {
                color: #aaa;
            }
            .offline-warning {
                padding: 0.8rem;
                background-color: #fff3cd;
                color: #856404;
                border-radius: 5px;
                margin-bottom: 1rem;
            }
            .dark-theme .offline-warning {
                background-color: #442c03;
                color: #ffe69c;
            }
            .dark-theme {
                background-color: #1a1a2e;
                color: #f0f0f0;
            }
            .btn-icon {
                background: none;
                border: none;
                cursor: pointer;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
            }
            .btn-icon:hover {
                background-color: #f0f0f0;
            }
            .dark-theme .btn-icon:hover {
                background-color: #333355;
            }
        </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'translation_history' not in st.session_state:
        st.session_state.translation_history = []
    if 'cached_translations' not in st.session_state:
        st.session_state.cached_translations = {}
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'offline_mode' not in st.session_state:
        st.session_state.offline_mode = False
    if 'formality' not in st.session_state:
        st.session_state.formality = True
    if 'speech_rate' not in st.session_state:
        st.session_state.speech_rate = 1.0
    if 'auto_translate' not in st.session_state:
        st.session_state.auto_translate = False

# Audio playback helper function
def get_audio_player(text, lang):
    """Generate an HTML audio player for the given text and language"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        audio_player = f'<audio controls autoplay="true"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        return audio_player
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# Simulate translation (in a real app, you would call an API)
def translate_text(text, source_lang, target_lang, formality):
    """
    Simulate translation - in a real app, this would call an external API
    like Google Translate, DeepL, etc.
    """
    if not text.strip():
        return ""
    
    # Check if in offline mode and if we have a cached translation
    cache_key = f"{text}_{source_lang}_{target_lang}_{formality}"
    if st.session_state.offline_mode and cache_key in st.session_state.cached_translations:
        return st.session_state.cached_translations[cache_key]
    
    # If in offline mode with no cached translation
    if st.session_state.offline_mode:
        return "Translation not available in offline mode. Please connect to translate new text."
        
    # Simple dictionary of common phrases in different languages (very limited example)
    translations = {
        'en': {
            'es': {
                'Hello': 'Hola',
                'Thank you': 'Gracias',
                'Please': 'Por favor',
                'Yes': 'Sí',
                'No': 'No',
                'Goodbye': 'Adiós',
                'Excuse me': 'Disculpe',
                'Sorry': 'Lo siento',
                'Where is the bathroom?': '¿Dónde está el baño?',
                'How much does this cost?': '¿Cuánto cuesta esto?',
                'I would like to order': 'Me gustaría ordenar',
                'I need help': 'Necesito ayuda'
            },
            'fr': {
                'Hello': 'Bonjour',
                'Thank you': 'Merci',
                'Please': 'S\'il vous plaît',
                'Yes': 'Oui',
                'No': 'Non',
                'Goodbye': 'Au revoir',
                'Excuse me': 'Excusez-moi',
                'Sorry': 'Désolé',
                'Where is the bathroom?': 'Où sont les toilettes?',
                'How much does this cost?': 'Combien ça coûte?',
                'I would like to order': 'Je voudrais commander',
                'I need help': 'J\'ai besoin d\'aide'
            },
            'de': {
                'Hello': 'Hallo',
                'Thank you': 'Danke',
                'Please': 'Bitte',
                'Yes': 'Ja',
                'No': 'Nein',
                'Goodbye': 'Auf Wiedersehen',
                'Excuse me': 'Entschuldigung',
                'Sorry': 'Es tut mir leid',
                'Where is the bathroom?': 'Wo ist die Toilette?',
                'How much does this cost?': 'Wie viel kostet das?',
                'I would like to order': 'Ich möchte bestellen',
                'I need help': 'Ich brauche Hilfe'
            }
        }
    }
    
    # Check if we have a direct translation
    if source_lang in translations and target_lang in translations[source_lang] and text in translations[source_lang][target_lang]:
        result = translations[source_lang][target_lang][text]
    elif source_lang == target_lang:
        # If source and target are the same, return the original text
        result = text
    else:
        # For other cases, append a prefix to show it's a simulated translation
        formality_str = "[FORMAL] " if formality else "[CASUAL] "
        result = f"{formality_str}[Translated from {source_lang} to {target_lang}]: {text}"
    
    # Cache the translation
    st.session_state.cached_translations[cache_key] = result
    
    # Simulate API delay
    time.sleep(0.5)
    
    return result

# Add to translation history
def add_to_history(source_text, translated_text, source_lang, target_lang):
    """Add a translation to the history"""
    if not source_text.strip() or not translated_text.strip():
        return
        
    timestamp = datetime.now().isoformat()
    
    history_item = {
        "id": int(time.time() * 1000),  # Unique ID based on timestamp
        "source_text": source_text,
        "translated_text": translated_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "timestamp": timestamp
    }
    
    # Add to the beginning of the history list
    st.session_state.translation_history.insert(0, history_item)
    
    # Keep only the last 50 items
    if len(st.session_state.translation_history) > 50:
        st.session_state.translation_history = st.session_state.translation_history[:50]

# Language code to name mapping
def get_language_name(lang_code):
    """Convert language code to full name"""
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'pt': 'Portuguese'
    }
    return languages.get(lang_code, lang_code)

# Main application
def main():
    # Initialize session state
    init_session_state()
    
    # Add custom CSS
    add_custom_css()
    
    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-theme">', unsafe_allow_html=True)
    
    # App header
    st.markdown('<h1 class="main-header">🌍 AI Language Translator for Travelers</h1>', unsafe_allow_html=True)
    
    # Offline mode warning
    if st.session_state.offline_mode:
        st.markdown(
            '<div class="offline-warning">⚠️ You are currently in offline mode. Limited functionality available.</div>',
            unsafe_allow_html=True
        )
    
    # Main translation interface
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Language selection row
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            source_lang = st.selectbox(
                "Translate from:", 
                options=["en", "es", "fr", "de", "it", "ja", "ko", "zh", "ru", "ar", "hi", "pt"],
                format_func=get_language_name,
                key="source_lang"
            )
        
        with col2:
            st.markdown("<div style='text-align: center; padding-top: 30px;'>")
            swap_button = st.button("🔄 Swap", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if swap_button:
                # Get current values
                source = st.session_state.source_lang
                target = st.session_state.target_lang
                source_text = st.session_state.source_text if "source_text" in st.session_state else ""
                translated_text = st.session_state.translated_text if "translated_text" in st.session_state else ""
                
                # Swap languages
                st.session_state.source_lang = target
                st.session_state.target_lang = source
                
                # Swap text if both have content
                if source_text and translated_text:
                    st.session_state.source_text = translated_text
                    st.session_state.translated_text = source_text
        
        with col3:
            target_lang = st.selectbox(
                "Translate to:", 
                options=["es", "en", "fr", "de", "it", "ja", "ko", "zh", "ru", "ar", "hi", "pt"],
                format_func=get_language_name,
                key="target_lang"
            )
        
        # Text input and translation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<p class='subheader'>Enter Text</p>", unsafe_allow_html=True)
            source_text = st.text_area("", height=150, key="source_text", 
                                       placeholder="Enter text to translate...")
            
            col1_1, col1_2 = st.columns([1, 1])
            with col1_1:
                if st.button("🔊 Listen", use_container_width=True):
                    if source_text:
                        audio_player = get_audio_player(source_text, source_lang)
                        if audio_player:
                            st.markdown(audio_player, unsafe_allow_html=True)
            with col1_2:
                if st.button("❌ Clear", use_container_width=True):
                    st.session_state.source_text = ""
                    st.experimental_rerun()
        
        with col2:
            st.markdown("<p class='subheader'>Translation</p>", unsafe_allow_html=True)
            
            if "translated_text" not in st.session_state:
                st.session_state.translated_text = ""
                
            translated_text = st.text_area("", 
                                          value=st.session_state.translated_text,
                                          height=150, key="translated_text", 
                                          placeholder="Translation will appear here...",
                                          disabled=True)
            
            col2_1, col2_2 = st.columns([1, 1])
            with col2_1:
                if st.button("🔊 Listen Translation", use_container_width=True):
                    if translated_text:
                        audio_player = get_audio_player(translated_text, target_lang)
                        if audio_player:
                            st.markdown(audio_player, unsafe_allow_html=True)
            with col2_2:
                if st.button("📋 Copy", use_container_width=True):
                    if translated_text:
                        # Use JavaScript to copy to clipboard
                        st.markdown(
                            f"""
                            <script>
                                navigator.clipboard.writeText("{translated_text.replace('"', '\\"')}");
                            </script>
                            """,
                            unsafe_allow_html=True
                        )
                        st.success("Copied to clipboard!")
        
        # Translation button and auto-translate checkbox
        col1, col2 = st.columns([3, 2])
        with col1:
            translate_button = st.button("🌐 Translate", use_container_width=True)
        with col2:
            auto_translate = st.checkbox("Auto-translate", value=st.session_state.auto_translate)
            st.session_state.auto_translate = auto_translate
            
        # Perform translation when button is clicked or auto-translate is on
        if translate_button or (auto_translate and source_text and "last_source" not in st.session_state or source_text != st.session_state.get("last_source", "")):
            if source_text:
                with st.spinner("Translating..."):
                    translated = translate_text(
                        source_text, 
                        source_lang, 
                        target_lang, 
                        st.session_state.formality
                    )
                    st.session_state.translated_text = translated
                    
                    # Add to history
                    add_to_history(source_text, translated, source_lang, target_lang)
                    
                    # Save last source to prevent multiple auto-translations
                    st.session_state.last_source = source_text
                    
                    # Force refresh
                    st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for History, Phrasebook, and Settings
    tab1, tab2, tab3 = st.tabs(["History", "Phrase Book", "Settings"])
    
    # History tab
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        if not st.session_state.translation_history:
            st.info("Your translation history will appear here")
        else:
            if st.button("🗑️ Clear History"):
                st.session_state.translation_history = []
                st.experimental_rerun()
                
            for item in st.session_state.translation_history:
                col1, col2 = st.columns([5, 1])
                with col1:
                    # Format the history item
                    st.markdown(
                        f"""
                        <div class="history-item" onclick="loadHistoryItem{item['id']}()">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: #3949ab;">
                                    {get_language_name(item['source_lang'])} → {get_language_name(item['target_lang'])}
                                </span>
                                <small style="color: #888;">
                                    {datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M')}
                                </small>
                            </div>
                            <div><b>{item['source_text'][:40] + ('...' if len(item['source_text']) > 40 else '')}</b></div>
                            <div>{item['translated_text'][:40] + ('...' if len(item['translated_text']) > 40 else '')}</div>
                        </div>
                        <script>
                        function loadHistoryItem{item['id']}() {{
                            const sourceElem = document.querySelector('[data-testid="stTextArea"] textarea[aria-label=""]');
                            if (sourceElem) {{
                                sourceElem.value = "{item['source_text'].replace('"', '\\"')}";
                                sourceElem.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            }}
                            
                            // Also need to update session state - this requires a form submit or similar
                            // For simplicity, we'll just tell the user we've loaded the text
                        }}
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                with col2:
                    if st.button("Load", key=f"load_{item['id']}"):
                        st.session_state.source_text = item['source_text']
                        st.session_state.source_lang = item['source_lang']
                        st.session_state.target_lang = item['target_lang']
                        st.session_state.translated_text = item['translated_text']
                        st.experimental_rerun()
                
                st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Phrase Book tab
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Categories for the phrasebook
        categories = {
            "Greetings & Basics": [
                "Hello", "Thank you", "Please", "Yes", "No", 
                "Goodbye", "Excuse me", "Sorry"
            ],
            "Travel & Directions": [
                "Where is the bathroom?", "How do I get to the hotel?", 
                "I am lost", "Can you show me on the map?", 
                "How much is a taxi to the airport?", "Is it far from here?"
            ],
            "Food & Dining": [
                "I would like to order", "The check, please", 
                "I am allergic to", "Is there a vegetarian option?", 
                "Water, please", "This is delicious"
            ],
            "Emergency & Health": [
                "I need help", "Call an ambulance", "I need a doctor", 
                "I have lost my passport", "Where is the nearest pharmacy?", 
                "I am not feeling well"
            ]
        }
        
        # Create expandable sections for each category
        for category, phrases in categories.items():
            with st.expander(category, expanded=(category == "Greetings & Basics")):
                cols = st.columns(2)
                for i, phrase in enumerate(phrases):
                    with cols[i % 2]:
                        st.markdown(f'<div class="phrase-item">{phrase}</div>', unsafe_allow_html=True)
                        if st.button("Use", key=f"phrase_{phrase.replace(' ', '_')}", use_container_width=True):
                            st.session_state.source_text = phrase
                            if st.session_state.auto_translate:
                                # Trigger translation
                                st.session_state.last_source = None
                            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Settings tab
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Display settings
        st.markdown("<p class='subheader'>Display Settings</p>", unsafe_allow_html=True)
        dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.experimental_rerun()
            
        offline_mode = st.checkbox("Offline Mode", value=st.session_state.offline_mode)
        if offline_mode != st.session_state.offline_mode:
            st.session_state.offline_mode = offline_mode
            st.experimental_rerun()
        
        # Speech settings
        st.markdown("<p class='subheader'>Speech Settings</p>", unsafe_allow_html=True)
        speech_rate = st.slider(
            "Speech Rate", 
            min_value=0.5, 
            max_value=2.0, 
            value=st.session_state.speech_rate,
            step=0.1,
            format="%.1f"
        )
        st.session_state.speech_rate = speech_rate
        
        # Translation settings
        st.markdown("<p class='subheader'>Translation Settings</p>", unsafe_allow_html=True)
        formality = st.checkbox("Formal Language", value=st.session_state.formality)
        st.session_state.formality = formality
        
        # Data management
        st.markdown("<p class='subheader'>Data Management</p>", unsafe_allow_html=True)
        if st.button("Clear Cached Translations"):
            st.session_state.cached_translations = {}
            st.success("Cached translations cleared!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Features</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h5>Modern Translation</h5>
                <small>Leveraging AI for accurate language translations</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h5>Travel Ready</h5>
                <small>Common phrases and offline capabilities for travelers</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h5>Text-to-Speech</h5>
                <small>Hear the correct pronunciation with native speakers</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        '<div class="footer">© 2025 AI Language Translator for Travelers | Version 1.0</div>',
        unsafe_allow_html=True
    )
    
    # Close dark theme div if needed
    if st.session_state.dark_mode:
        st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()