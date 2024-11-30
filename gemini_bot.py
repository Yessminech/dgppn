import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
GOOGLE_API_KEY = 'AIzaSyBEoATdexrJPrhSmKY7x1AlLHYmeqRdkf8'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def init_page():
    st.set_page_config(
        page_title="Medical DiGA Chatbot",  # Set the page title
        page_icon="🩺",                    # Set the page icon
        layout="wide",                     # Use a wide layout for better user experience
        initial_sidebar_state="expanded"   # Sidebar starts expanded
    )
    st.header("Therapiegespräch")
    st.sidebar.title("Settings")

def start_chat(initial_context):
    return model.start_chat(history=[{"role": "user", "parts": initial_context}])

def main():
    init_page()
    
    # Paths to avatar images
    practitioner_avatar = "/home/yessmine/Documents/Aerztin.png"  # Path to practitioner avatar
    patient_avatar = "/home/yessmine/Documents/1430402.png"           # Path to patient avatar
    
    # Initial context for the simulated conversation
    initial_context = (
    "Die Diskussion sollte zwischen Patienten und Praktikern stattfinden, "
    "wobei die Praktiker die Rolle des Patienten übernehmen. "
    "Ich bin der Patient, und du der Professional. "
    "Der Praktiker muss immer Verständnis zeigen und auf die Bedenken des Patienten eingehen. "
    "Die Diskussion sollte zwischen Patienten und Praktikern abwechselnd stattfinden, "
    "Simuliertes Gespräch: Therapeut als 'Patient'\n"
    "Psychotherapeut:\n"
    "Willkommen! Schön, dass Sie heute hier sind. Wie kann ich Ihnen helfen? Was beschäftigt Sie momentan?\n"
    "Praktiker (als Patient):\n"
    "Ich bin nur noch müde und energielos, konnte mich kaum aufraffen, hierher zu kommen. Sie hatten ja bei meinem letzten Besuch etwas von einer App erwähnt, die mir helfen könnte. Ich bin mir irgendwie so unsicher, ob das wirklich funktionieren kann…\n"
    "Praktiker (als Therapeut):\n"
    "'Das ist eine berechtigte Sorge. Die App, die ich Ihnen empfehlen würde, ist allerdings nicht zu vergleichen mit einem beliebigen Download aus dem App Store. Es handelt sich um eine Digitale Gesundheitsanwendung, kurz DiGA. Das bedeutet, dass sie vom BfArM, der gleichen Behörde, die Medikamente reguliert, gründlich geprüft wurde. Dadurch wird sichergestellt, dass die App bereits positive Behandlungseffekte bei Patienten gezeigt hat.'\n"
    "Praktiker (als Patient):\n"
    "'Aber wie soll das in mein Leben passen? Ich fühle mich schon jetzt überfordert, und ich mache mir Sorgen, dass das einfach wieder etwas ist, an dem ich nicht dranbleiben werde. Mir geht es einfach sehr schlecht.'\n"
    "Praktiker (als Therapeut):\n"
    "'Das ist nachvollziehbar. Die App ist jedoch so entwickelt, dass sie benutzerfreundlich und flexibel ist. Sie können sie in Ihrem eigenen Tempo nutzen, und sie lässt sich in Ihren Alltag integrieren – sei es während einer Pause, vor dem Schlafengehen oder immer, wenn Sie einen ruhigen Moment haben. Es gibt ihnen eine Möglichkeit, aktiv an ihrer mentalen Gesundheit zu arbeiten, auch außerhalb von Therapie oder Terminen. Ganz so wie es im Ihr Leben passt.'\n"
    "Praktiker (als Patient):\n"
    "'Und was ist mit meinen Daten? Ich habe viel über Apps gehört, die persönliche Informationen sammeln. Wie sicher ist das was Sie mir empfehlen?'\n"
    "Praktiker (als Therapeut):\n"
    "'DiGAs müssen strenge europäische und deutsche Datenschutzgesetze einhalten. Im Gegensatz zu vielen ungeprüften Apps sind sie so entwickelt, dass sie medizinische Datenschutzstandards einhalten.'\n"
    "Praktiker (als Patient):\n"
    "'Aber ehrlich gesagt, wird das wirklich einen Unterschied machen? Ich bin mir nicht sicher, ob eine App eine echte Person oder Therapie ersetzen kann.'\n"
    "Praktiker (als Therapeut):\n"
    "'Da haben Sie vollkommen recht – es geht tatsächlich auch gar nicht darum, die Therapie zu ersetzen. Eine DIGA ist ein zusätzliches Hilfsmittel, um Sie zu unterstützen. Zum Beispiel könnte die App Sie durch Entspannungsübungen führen, wenn Sie sich ängstlich fühlen, oder andere Anregungen geben, die Ihnen im Alltag helfen können. Es ist wie eine Ressource, die Sie jederzeit zur Hand haben, die Ihnen hilft, wenn Sie es brauchen. Außerdem können wir Ihren Fortschritt gemeinsam in unseren Sitzungen besprechen, so dass Sie auf diesem Weg nicht allein sind.'\n"
    "Praktiker (als Patient):\n"
    "'Das klingt gut, dann werd ich es zumindest mal versuchen.'\n"
)
    # Initialize chat
    if 'chat' not in st.session_state:
        st.session_state.chat = start_chat(initial_context)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Add initial message if the conversation is empty
    if not st.session_state.messages:
        initial_message = "Willkommen! Schön, dass Sie heute hier sind. Wie kann ich Ihnen helfen? Was beschäftigt Sie momentan?"
        st.session_state.messages.append({"role": "init", "content": initial_message})

    # Clear conversation button
    if st.sidebar.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat = start_chat(initial_context)
        st.session_state.messages.append({"role": "assistant", "content": "Willkommen! Schön, dass Sie heute hier sind. Wie kann ich Ihnen helfen? Was beschäftigt Sie momentan?"})
    
    # Custom CSS for chat messages
    st.markdown("""
        <style>
        .user-message {
            align-self: flex-end;
            background-color: #99FFAC; /* Green background */
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: left;
            border: none; /* Ensure no border */
            box-shadow: none; /* Remove shadows if any */
        }
        .assistant-message {
            align-self: flex-start;
            background-color: #F4F3F6; /* Light grey background */
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            text-align: left;
            border: none;
            box-shadow: none;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "init":
            avatar = practitioner_avatar
            st.chat_message("assistant", avatar=avatar).markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        if message["role"] == "user":
            avatar = patient_avatar
            st.chat_message("user", avatar=avatar).markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            avatar = practitioner_avatar
            st.chat_message("assistant", avatar=avatar).markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

    # User input
    if user_input := st.chat_input("Meine Frage..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user", avatar=patient_avatar):
            st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

        # Generate response
        with st.chat_message("assistant", avatar=practitioner_avatar):
            with st.spinner("Denke nach..."):
                if user_input == "Das klingt gut, dann werd ich es zumindest mal versuchen. Danke!":
                    response_text = "Gern geschehen! Wenn Sie weitere Fragen haben oder Unterstützung benötigen, lassen Sie es mich bitte wissen."
                else:
                    response = st.session_state.chat.send_message(user_input)
                    response_text = response.text
                st.markdown(f'<div class="assistant-message">{response_text}</div>', unsafe_allow_html=True)

        # Add assistant response to messages
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    main()