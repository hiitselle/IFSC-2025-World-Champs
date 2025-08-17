import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import mdurl
import streamlit as st
import pandas as pd
from  streamlit_autorefresh import st_autorefresh
st.set_page_config(page_title="IFSC 2025 World Champs", layout="wide")
st_autorefresh(interval=2000)#in ms



def ch_bg_to_green():
 st.balloons()

 st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
           position: absolute;
           background: #f8de7e;
           color: rgb(248, 222, 126);
           inset: 0px;
           overflow: hidden;
    }
    header[data-testid="stHeader"] {
               position: fixed;
               top: 0px;
               left: 0px;
               right: 0px;
               height: 2.875rem;
               background: #f8de7e;
               outline: none;
               z-index: 999990;
               display: block;
    }   
   </style>
    """,
    unsafe_allow_html=True
 )

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.freepik.com/free-vector/hand-painted-watercolor-pastel-sky-background_13223496.htm#query=background&position=3&from_view=keyword&track=sph");
    }
   </style>
    """,
    unsafe_allow_html=True
)

st.header("**Seoul World Champs 2025**")

with st.sidebar:
    genderSel = st.selectbox(
        "Select Round",
        ("Male Boulder Semis", "Female Boulder Semis" ,"Male Boulder Final" ,"Female Boulder Finals" ,"Male Lead Semis", "Female Lead Semis" ,"Male Lead Final" ,"Female Lead Finals")
    )

#@st.cache_data(ttl=60)
def load_data(sheets_url):
    return pd.read_csv(sheets_url, dtype=str)

if(genderSel=="Male Boulder Semis"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1631360020")
 
elif(genderSel=="Female Boulder Semis"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1785852811")
 
elif(genderSel=="Male Boulder Final"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=935198785")    

elif(genderSel=="Female Boulder Final"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=769323139")
 
elif(genderSel=="Male Lead Semis"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1842627779")    

elif(genderSel=="Female Lead Semis"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=137564533")
 
elif(genderSel=="Male Lead Final"):
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=0")    
    
else:
    df = load_data("https://docs.google.com/spreadsheets/d/1RVgQboeDCi1X2zEQdCzWqe9HYQTJpj5EumjFXf4qjN0/export?format=csv&gid=1947247931")
df = df.astype(str)

# --- Athlete selector ---
athletes = df["Name"].dropna().tolist()
selected_athlete = st.selectbox("Select an athlete", athletes)

# --- Show details ---
if selected_athlete:
    row = df[df["Name"] == selected_athlete].iloc[0]

    st.subheader(f"📊 {selected_athlete}")

    st.write(f"**Total Score (D):** {row['TotalScore']}")
    st.write(f"**Points to 1st (I):** {row['Points to 1st']}")
    st.write(f"**Hold for Current 1st (R):** {row['Hold for Current 1st']}")
    st.write(f"**Points to 2nd (J):** {row['Points to 2nd']}")
    st.write(f"**Hold for Current 2nd (S):** {row['Hold for Current 2nd']}")
    st.write(f"**Points to 3rd (K):** {row['Points to 3rd']}")
    st.write(f"**Hold for Current 3rd (T):** {row['Hold for Current 3rd']}")
    st.write(f"**Actual Ranking (N):** {row['Actual Ranking']}")
    st.write(f"**Qualified (O):** {row['Qualified']}")
    st.write(f"**Min Needed (Q):** {row['min needed']}")
    st.write(f"**Min Hold to Qualify (U):** {row['Min Hold to Qualify']}")

                 
for x in range(len(df)):
    with st.expander(df['Name'].iloc[x]):
        generateInfo(x)

st.write("Made by Elle")
