import streamlit as st

def set_bg_hack_url():    
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://bodyhack.co/wp-content/themes/body-hack/assets/Images/Contact_bANNER.png");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
def set_color_title(color, title):
    st.markdown(
        f"""
        <h1 style="color: {color};
        font-size: 40px;
        font-weight: bold; 
        text-align: center">{title}
        </h1>""", 
        unsafe_allow_html=True
        )
    
def set_color_text(color, text):
    st.markdown(
        f"""
        <p style="color:{color};
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        ">{text}</p>
        """,
        unsafe_allow_html=True
    )
