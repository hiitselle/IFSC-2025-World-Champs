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

#st.dataframe(data=df, use_container_width=True)
df_metric = df.copy()
df_metric['TotalScore'] = df_metric['TotalScore'].astype('float')
df_metric = df_metric.sort_values(by='TotalScore', ascending=True)
df_metric = df_metric.tail(8)
df_metric['color'] = ''
for z in range(len(df_metric)):
    if(df_metric['Qualified'].iloc[z] == "Qualified for Finals :)") or (df_metric['Qualified'].iloc[z] == "Podium Garentee!!!!") :
        df_metric['color'].iloc[z] = 'green'
        #st.write(df_metric['color'].iloc[z])
    else:
        df_metric['color'].iloc[z] = 'red'
#st.dataframe(data=df_metric, use_container_width=True)
plot_assym = go.Figure(go.Bar(x=df_metric['TotalScore'], y=df_metric["Name"], orientation='h',text=df_metric['TotalScore'].astype('str'),marker={'color': df_metric['color']}))
st.sidebar.plotly_chart(plot_assym)
with st.expander("Current Leader"):
    
    index = df['Actual Ranking'].idxmin()

    if(df['Worst Case'].iloc[index] == "1"):
        st.success(df['Name'].iloc[index] + " WINNER WINNER CHICKEN DINNER!")
        ch_bg_to_green()
    else:
        st.error(df['Name'].iloc[index] + " :red[is leading & is Beatable!]")


def generateInfo(index):
    st.write("Current Points: " + df['TotalScore'].iloc[index])
    st.write("Current Position: " + df['Actual Ranking'].iloc[index])
   
    if(df['Is score complete'].iloc[index] == "1"):
        st.write("Worst Case Position: " + df['Worst Case'].iloc[index])
        st.write("Qualified: " + df['Qualified'].iloc[index])
        st.write("Points still needed to 1st: " + df['Points to 1st raw'].iloc[index])
        
     
    else:
     
        st.write("min needed for 8th: " + df['min needed'].iloc[index])
        st.write("Points to 1st: " + df['Points to 1st'].iloc[index])
        st.write("Points to 2nd: " + df['Points to 2nd'].iloc[index])
        st.write("Points to 3rd: " + df['Points to 3rd'].iloc[index])
        
        
     

    if(df['Qualified'].iloc[index] == "Qualified for Finals :)") or (df['Qualified'].iloc[index] == "Podium Garentee!!!!") :
        
 
        #st.write(index)
        st.success(df['Name'].iloc[index] + " :green[...]")
        
        st.markdown(
                    """
                    <style>
    
                    div[data-testid="stExpander"]:nth-of-type(""" + str(index+5) + """) {
                         background: 	#d0f0c0;
                         color: black; # Expander content color
                    }

                    </style>
                    """,
                    unsafe_allow_html=True
                    )
    else:
        #st.write(index)
        
        st.error(df['Name'].iloc[index] + " :red[...]") 
        st.markdown(
                    """
                    <style>
    
                    div[data-testid="stExpander"]:nth-of-type(""" + str(index+5) + """) {
                         background: 	#ffcccb;
                         color: black; # Expander content color
                    }

                    </style>
                    """,
                    unsafe_allow_html=True
                    )
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
