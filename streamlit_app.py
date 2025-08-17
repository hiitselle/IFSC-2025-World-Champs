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

# --- Athlete selector with ranking ---
st.title("🏆 Seoul World Champs 2025")

df = df.sort_values(by="Actual Ranking")  # ensure ranked order
athletes_display = [
    f"{int(row['Actual Ranking'])}. {row['Name']}"
    for _, row in df.iterrows()
]
selected_display = st.selectbox("Select an athlete", athletes_display)

# Extract just the athlete name from the dropdown choice
selected_athlete = selected_display.split(". ", 1)[1]

# --- Athlete Card ---
if selected_athlete:
    row = df[df["Name"] == selected_athlete].iloc[0]

    # Qualification Badge
    qualified = str(row["Qualified"]).strip().lower()
    if qualified in ["yes", "qualified", "true", "1"]:
        badge = "🟢 Qualified"
    else:
        badge = "🔴 Not Qualified"

    st.markdown(
        f"""
        <div style="
            background-color:#f9f9f9;
            border-radius:15px;
            padding:20px;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
        ">
            <h2 style="margin-bottom:5px;">{row['Actual Ranking']}. {selected_athlete}</h2>
            <p style="font-size:18px; font-weight:bold;">{badge}</p>

            <hr style="margin:10px 0;">

            <p><b>Total Score:</b> {row['TotalScore']}</p>
            <p><b>Points to 1st:</b> {row['Points to 1st']} | <b>Hold:</b> {row['Hold for Current 1st']}</p>
            <p><b>Points to 2nd:</b> {row['Points to 2nd']} | <b>Hold:</b> {row['Hold for Current 2nd']}</p>
            <p><b>Points to 3rd:</b> {row['Points to 3rd']} | <b>Hold:</b> {row['Hold for Current 3rd']}</p>
            
            <p><b>Actual Ranking:</b> #{row['Actual Ranking']}</p>
            <p><b>Min Needed:</b> {row['min needed']} | <b>Min Hold to Qualify:</b> {row['Min Hold to Qualify']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

                 
for x in range(len(df)):
    with st.expander(df['Name'].iloc[x]):
        generateInfo(x)

st.write("Made by Elle")
