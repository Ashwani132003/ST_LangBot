import streamlit as st
import time
import openai
import speech_recognition as sr
from src.main import global_state


openai_key = st.secrets['openai_key']
openai.api_key = openai_key


if len(global_state.messages)==0:
    global_state.messages = [{"role": "system", "content": "You are a Language Learning Companion"}]

def app():

    def ask_tech_question(question):
        global_state.messages.append({"role": "user", "content": question})
        response = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = global_state.messages
        )
        ChatGPT_reply = response.choices[0].message.content
        print(ChatGPT_reply)

        global_state.messages.append({"role": "assistant", "content": ChatGPT_reply})
        st.session_state.q =''

        return ChatGPT_reply

    def voice_to_text():
        recognizer = sr.Recognizer()
        with st.spinner("Listening..."):
            with sr.Microphone() as source:
                print("Say something:")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=3)  # Listen for up to 5 seconds

            try:
                voice_text = recognizer.recognize_google(audio)
                print("You said:", voice_text)
                # st.session_state.message=voice_text
                
                # return voice_text
                st.session_state.q=text.text_input("input something", value=voice_text, key="2")
                
            except sr.UnknownValueError:
                print("Sorry, I could not understand audio.")
                st.warning('Sorry, I could not understand audio.')
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")
                st.warning(f"Could not request results from Google Web Speech API; {e}")

    chats = {}
    st.session_state.chat = 0
   

    st.session_state.message = ''



    col1,col2,col3 = st.columns([1,8,1])

    # col1.markdown("")
    # col1.markdown("")

    col1.button(' :microphone:',on_click=voice_to_text)

    if 'q' not in st.session_state:
        st.session_state.q =''
    text = col2.empty()

    st.session_state.q=text.text_input(label='a',placeholder="Ask here - ", value=st.session_state.q, key="1", label_visibility="collapsed")
    
    # from streamlit import _bottom
    # _bottom._enqueue("message", text)
    
    # st.markdown(
    # """
    # <style>





    # div[data-testid="stHorizontalBlock"] {
    #     position: fixed;
    #     bottom: 0;
    #     width: 70%;
    #     text-align: center;
    #     padding: 10px;
    #     background-color: rgba(0, 0, 0);
    #     border: 2px solid green;
    #     margin-top: 50px;
    #     z-index: 9999;

    # }
    # </style>

    # """, unsafe_allow_html=True
    # )
    st.markdown(
    """
    <style>


    
    h1 {
        position: fixed;
        top: 0;
        padding: 10px;
        z-index: 9999;
        margin:40px 0;
        background-color: rgba(0, 0, 0);
    }   

    div[data-testid="stSelectbox"] {
        position: fixed;
        top:0;
        text-align: center;
        padding: 10px;
        background-color: rgba(0, 0, 0);
        z-index: 9999;
        margin:100px 0;

    }


    div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        width: 71%;
        text-align: center;
        padding: 10px;
        background-color: rgba(0, 0, 0);
        border: 2px solid green;
        margin-top: 50px;
        z-index: 9999;

    }

        @media only screen and (max-width: 768px) {
            h1 {
                width:400px;
            
                color: red; /* Change color for smaller devices */
            }
        }

        /* Media query for devices with a width between 769px and 1200px */
        @media only screen and (min-width: 769px) and (max-width: 1200px) {
            h1 {
                width:770px;
            
                color: green; /* Change color for medium-sized devices */
            }
        }

        /* Media query for devices with a width greater than 1200px */
        @media only screen and (min-width: 1201px) {
            h1 {
                width:1284px;
                color: orange; /* Change color for larger devices */
            }
            div[data-testid="stSelectbox"]  {
                width:1284px;
                color: orange; /* Change color for larger devices */
            }

        }
    </style>

    """, unsafe_allow_html=True
    )


    print('q',st.session_state.q)

    def run(answer):

        for word in answer.split():
            yield word + " "
            time.sleep(0.02)


    # Selectbox for to and from Langauage
    st.title('LangBot')       
    selectbox=st.selectbox('Translate to: ',('English','Hindi','French','German'),index=None)
    if selectbox and global_state.selectbox!=selectbox:
        global_state.selectbox=selectbox
        st.session_state.q=''
        global_state.messages = [{"role": "system", "content": f"You are a Language Learning Companion, you have to convert all the messages from user into {selectbox}"}]
        print(global_state.messages, selectbox)

    # Cards for some sample questions


    def send():
        answer=ask_tech_question(st.session_state.q)
    if col3.button(' :arrow_forward:'):
        send()
    
    elif st.session_state.q:

        send()        

    st.markdown("""
        <script>
            // Function to update element width
            function updateElementWidth() {
                var element = document.querySelector('[data-testid="stVerticalBlock"]');
                var width = element.offsetWidth;
                // Example: Update width based on current width
                if (width > 300) {
                    element.style.width = "200px"; // Adjust width as needed
                } else {
                    element.style.width = "200px"; // Adjust width as needed
                }
            }
            
            // Call the function when the page loads and when it's resized
            window.onload = updateElementWidth;
            window.addEventListener("resize", updateElementWidth);
        </script>
    """, unsafe_allow_html=True)

    print(global_state.messages)
    if len(global_state.messages)>1: 
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")



        for message in global_state.messages[1:-1]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"]) 
        for message in global_state.messages[-1:]:
            with st.chat_message(message["role"]):
                # st.markdown(message["content"]) 
                st.write_stream(run(message["content"]))


    # for i in st.session_state.message:
    #     print(i)
    #     st.chat_message("user").write(i[0])
    #     st.chat_message("assistant").write(f"Echo: {i[1]}")    
    st.divider()
    if st.button("Toggle Sidebar"):
        print('toggled')

        st.sidebar.toggle()
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")

app()    