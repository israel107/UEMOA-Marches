import random
#import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np


#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="Market Dashboard", page_icon=":bar_chart:", layout="wide")

st.markdown("<h2 style='text-align: left; font-size: 40px;  font-weight: bold;'>Tableau de bord du marché de l'UEMOA</h2>", unsafe_allow_html=True)
st.image("./pays_uemoa_png.png", caption="", use_container_width=False)
st.markdown("_DABFA-SFE v0.0.1_")

#graphs will use css
theme_plotly = None

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)


#######################################
# DATA LOADING
#######################################

# df = load_data(uploaded_file)
all_months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
all_year = ["2019", "2020", "2021", "2022", "2023", "2024"]
all_secteur = ["BRVM Composite", "BRVM 30", "BRVM Prestige","BRVM Principal", "Agriculture","Finances","Serv. Publics", "Industrie","Distribution", "Transport","Autres"]
all_period = ["Année","Semestre","Trimestre","Mois"]

df_index = pd.read_excel("./All_Indices_2024.xlsx", sheet_name="Cours") 
df_val = pd.read_excel("./idx_val_sept2024_2.xlsx" , sheet_name= "Feuil1")
df_vol = pd.read_excel("./idx_volume_sept2024.xlsx", sheet_name= "Feuil2")
#df_oblig = pd.read_excel("./Val_Oblig_sept_2024.xlsx", sheet_name=None)
#df_oblig.set_index('seance', inplace=True)

df_index_2 = df_index

df_liq = pd.read_excel("./BRVM_ratio_liquidite.xlsx", sheet_name="Feuille 1")
df_liq.set_index('Seance', inplace=True)

df_index.set_index('Séance')
CHART_THEME ='plotly_white'
df_val = df_val.set_index('seance', inplace=True)

all_pays = ['Bénin',"Burkina","Côte d'Ivoire", "Guinée Bissaù","Mali","Niger","Sénégal","Togo"]

#######################################
# SIDEBAR
#######################################

with st.sidebar:
    m_pays = st.selectbox('Pays', all_pays)

with st.sidebar:
    m_secteur_3 = st.multiselect('Select indices', all_secteur, ["BRVM Composite", "Agriculture"])

    #print("Réponse : " + str(m_secteur))

with st.sidebar:
    v_annee = st.slider("Années", 2019, 2024, 2022)
   

with st.sidebar:
    v_periode = st.selectbox('Périodes', all_period)

#######################################
# DATA INDICATEUR
#######################################
with st.expander("STATISTIQUES"):
    st.markdown('### Infos essentielles')
    m_cap_obl = [7100, 12000, 9500, 10500, 14100, 11600]
    m_cap_action = [5000, 8000, 7500, 7200,9100, 5600]
    mar_Prim_mob = [2430, 2350,2750, 3400, 4200, 3900]
    emiss_MTP = [1200, 1740, 1480, 2100, 2500, 2150]
    total_Eurob = [1400, 1800, 1100, 2500, 2900, 3200]

    Nb_action = [44, 45, 46, 47, 47, 48, 48]
    Nb_oblig = [90, 105, 98, 110, 96, 120, 114]
    m_period = ["Année", "semestre", "Trimestre","Mois"]

    m_controler = 0
    tx_croiss_mark = 0
    tx_croiss_mark_act = 0
    tx_croiss_mark_obl = 0
    tx_croiss_Ire = 0
    tx_croiss_emiss = 0
    tx_croiss_action = 0

    if v_annee == 2019:
        m_controler = 0
    elif v_annee == 2020: 
        m_controler = 1
    elif v_annee == 2021: m_controler = 2
    elif v_annee == 2022: m_controler = 3
    elif v_annee == 2023: m_controler = 4
    elif v_annee == 2024: m_controler = 5

    market_cap = m_cap_obl[m_controler] + m_cap_action[m_controler] 
    action_cap = m_cap_action[m_controler] 
    oblig_cap = m_cap_obl[m_controler]
    cap_prim = mar_Prim_mob[m_controler]
    nb_action = Nb_action[m_controler]
    val_emiss = emiss_MTP[m_controler]

    if v_annee == 2019:
        tx_croiss_mark = 0
        tx_croiss_mark_act = 0
        tx_croiss_mark_obl = 0
        tx_croiss_Ire = 0
        tx_croiss_emiss = 0
        tx_croiss_action = 0
    else : 
        market_cap_lag = m_cap_obl[m_controler-1] + m_cap_action[m_controler-1]
        tx_croiss_mark_act = round(((m_cap_action[m_controler]/m_cap_action[m_controler-1])-1)*100,2)
        tx_croiss_mark_obl = round(((m_cap_obl[m_controler]/m_cap_obl[m_controler-1])-1)*100,2)

        tx_croiss_mark = round(((market_cap/market_cap_lag)-1)*100,2)
        tx_croiss_Ire = round(((mar_Prim_mob[m_controler]/mar_Prim_mob[m_controler-1])-1)*100,2)
        tx_croiss_emiss = round(((emiss_MTP[m_controler]/emiss_MTP[m_controler-1])-1)*100,2)
        tx_croiss_action = round(((Nb_action[m_controler]/Nb_action[m_controler-1])-1)*100,2)

    total1, total2, total3, total4 = st.columns(4, gap='small')

    with total1:
        st.metric(label="Cap. Marché (Mds FCFA)", value=f"{market_cap: ,.0f}", delta=tx_croiss_mark)

    with total2:
        st.metric(label="Montant Levé sur le marché Primaire (Mds FCFA)", value=f"{cap_prim: ,.0f}", delta=tx_croiss_Ire)

    with total3:
        st.metric(label="Emission titres Publics (Mds FCFA)", value=f"{val_emiss: ,.0f}", delta=tx_croiss_emiss)

    with total4:
        st.metric(label="Nombre Actions", value=nb_action, delta=tx_croiss_action)

    st.info("**_Résumé:_**")
#######################################
# DATA LINE_0
#######################################
mob_Ire_BN = [4300, 2500, 3600, 4600, 4950, 5300]
mob_Ire_BF = [5812,3501,4466,6410,3041,5767]
mob_Ire_CI = [5128,6151,2878,3898,3629,5338]
mob_Ire_GB = [2974,6272,6625,6172,3683,3572]
mob_Ire_ML = [4371,3288,5877,6971,6115,2551]
mob_Ire_NG = [2641,4030,5949,4858,2424,4343]
mob_Ire_SN = [6653,4911,2994,6202,6827,2429]
mob_Ire_TG = [3854,3259,3423,3231,6921,5727]

m_mob_Ire = 0
if m_pays == "Bénin": m_mob_Ire = mob_Ire_BN
elif m_pays == "Burkina": m_mob_Ire = mob_Ire_BF
elif m_pays == "Côte d'Ivoire": m_mob_Ire = mob_Ire_CI
elif m_pays == "Guinée Bissaù": m_mob_Ire = mob_Ire_GB
elif m_pays == "Mali": m_mob_Ire = mob_Ire_ML
elif m_pays == "Niger": m_mob_Ire = mob_Ire_NG
elif m_pays == "Sénégal": m_mob_Ire = mob_Ire_SN
elif m_pays == "Togo": m_mob_Ire = mob_Ire_TG

m_mob_sec = [6250, 4320, 3920, 5640, 5750, 7260]
emiss_pays_20 = [6426,6693,6615,3729,3170,5071,5083,5723]
emiss_pays_21 = [4928,4813,5745,6389,5327,6492,6203,4536]
emiss_pays_22 = [6341,3547,5665,4056,3292,3453,4673,6245]
emiss_pays_23 = [5187,4577,5631,3360,3569,3242,4813,4056]
emiss_pays_24 = [4360,3300,6398,4290,4495,6025,5885,3539]

all_emiss = [emiss_pays_20, emiss_pays_21,emiss_pays_22, emiss_pays_23,
             emiss_pays_24]

m_emiss = 0
if v_annee <= 2020:
    m_emiss = emiss_pays_20
elif v_annee == 2021:
    m_emiss = emiss_pays_21
elif v_annee == 2022:
    m_emiss = emiss_pays_22
elif v_annee == 2023:
    m_emiss = emiss_pays_23
elif v_annee == 2024:
    m_emiss = emiss_pays_24

st.markdown('#### Marché des titres publics (MTP)')
col1, col2, col3 = st.columns(3, gap='small')

with col1:
    fig = go.Figure()
    m_value = m_mob_Ire
    fig.add_trace(go.Bar(
        x=all_year,
        y= m_value, 
        text= m_value,
        name='Primary Product', marker_color='rgb(133, 32, 12)', marker=dict(cornerradius="10%")) )

    fig.layout.template = CHART_THEME
    fig.update_layout(
        title= {
            'text':'Montant mobilisé sur le Marché Primaire',
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size = 12,
        yaxis=dict(
            title=dict(
            text="Milliards (FCFA)",
            font=dict(size=12, color="gray")
        )),
         
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=all_pays,
        y= m_emiss, 
        text= m_emiss,
        name='Primary Product', marker_color='rgb(100, 132, 12)', marker=dict(cornerradius="25%")) )

    fig.layout.template = CHART_THEME
    fig.update_layout(
        title= {
            'text':'Montant mobilisé sur le Marché Primaire par pays',
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=dict(
            text="Milliards (FCFA)",
            font=dict(size=12, color="gray")
            ))
    )

    st.plotly_chart(fig, use_container_width=True)

with col3:

    fig = go.Figure(data=[go.Pie(labels=all_pays, values=m_emiss, hole=.3)])
    fig.update_layout(
        title="Emission sur le Marché primaire par pays <br> (en milliards FCFA)",
        title_x=0.2,
        height=500,  # Hauteur du graphique
        width=500,    # Largeur du graphique
        legend=dict(
        orientation="h",  # Légende horizontale
        y=-0.2,  # Ajustement vertical sous le graphique
        x=0.5,   # Centrage horizontal
        xanchor="center",
        yanchor="top"
        )
    )

    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=15,
                  )
    
    st.plotly_chart(fig, use_container_width=True)

#######################################
# DATA LINE_1
#######################################
cap_BN = [3159,1863,1633,3403,1718,2898]
int_BN = [302,165,125,315,155,265]

cap_BF = [1038,1011,1423,1500,986,1154]
int_BF = [98,95,115,115,85,105]

cap_CI = [2938,1518,2490,1618,2141,3433]
int_CI = [265,125,220,115,202,310]

cap_ML = [1052,2467,1314,568,1862,2353]
int_ML = [73.6, 172.6, 91.9, 39.7, 130.3, 164.7]

cap_GB = [716,850,602,914,575,539]
int_GB = [50.1,59.5,42.1,63.9,40.2,37.7 ]

cap_NG = [863,998,611, 537,566, 770]
int_NG = [60.4,69.8 ,42.77,37.59,39.6,53.9]

cap_SN = [2667,2664,2609,1770,3551,1907]
int_SN = [145,126.4,112.6,123.9,228.5 ,103.49 ]

cap_TG = [1334,819,1482,714,1086,1485]
int_TG = [93.3,57.3 ,103.7 ,49.9 ,76,101]

tx_dure_BN = ["12 mois","3 ans","5 ans", "7 ans"]
tx_valeur_BN = [0.0639, 0.0684, 0.0708, 0.0702]

tx_dure_BF = ["3 mois","12 mois","3 ans","5 ans", "7 ans"]
tx_valeur_BF = [0.0819, 0.0864, 0.0928, 0.0745, 0.0779]

tx_dure_CI = ["6 mois","12 mois", "3 ans","5 ans","7 ans","10 ans"]
tx_valeur_CI = [0.0591, 0.0568, 0.0749, 0.0740, 0.0687, 0.0699]

tx_dure_GB = ["3 mois","6 mois","11 mois","12 mois", "3 ans"]
tx_valeur_GB = [0.0912, 0.0915, 0.0960, 0.0950, 0.1008]

Euro_bn = [3159,1863,1633,3403,1718,2898]
Euro_bf = [1038,1011,1423,1500,986,1154]
Euro_ci = [2938,1518,2490,1618,2141,3433]
Euro_gb = [716,850,602,914,575,539]
Euro_ml = [1052,2467,1314,568,1862,2353]
Euro_ng = [863,998,611, 537,566, 770]
Euro_sn = [2667,2664,2609,1770,3551,1907]
Euro_tg = [1334,819,1482,714,1086,1485]

m_cap = 0
m_interet = 0
tx_valeur = 0
tx_dure_GB = []
val_euro = 0

if m_pays == "Bénin":
    m_cap = cap_BN
    m_interet = int_BN
    tx_valeur = [100 * x for x in tx_valeur_BN]
    tx_dure = tx_dure_BN
    val_euro = Euro_bn
elif m_pays == "Burkina":
    m_cap = cap_BF
    m_interet = int_BF
    tx_valeur = [100 * x for x in tx_valeur_BF] 
    tx_dure = tx_dure_BF
    val_euro = Euro_bf
elif m_pays == "Côte d'Ivoire":
    m_cap = cap_CI
    m_interet = int_CI
    tx_valeur = [100 * x for x in tx_valeur_CI] 
    tx_dure = tx_dure_CI
    val_euro = Euro_ci
elif m_pays == "Guinée Bissaù":
    m_cap = cap_GB
    m_interet = int_GB
    tx_valeur = [100 * x for x in tx_valeur_GB]  
    tx_dure = tx_dure_GB
    val_euro = Euro_gb
elif m_pays == "Mali":
    m_cap = cap_ML
    m_interet = int_ML
    val_euro = Euro_ml
elif m_pays == "Niger":
    m_cap = cap_NG
    m_interet = int_NG
    val_euro = Euro_ng
elif m_pays == "Togo":
    m_cap = cap_TG
    m_interet = int_TG
    val_euro = Euro_tg
elif m_pays == "Sénégal":
    m_cap = cap_SN
    m_interet = int_SN
    val_euro = Euro_sn
elif m_pays == "UEMOA":
    m_cap = np.array(cap_ML)+ np.array(cap_SN)+np.array(cap_TG)+np.array(cap_NG)+np.array(cap_GB)+np.array(cap_CI)+np.array(cap_BF)+np.array(cap_BN)
    m_interet = m_cap = np.array(int_ML)+ np.array(int_SN)+np.array(int_TG)+np.array(int_NG)+np.array(int_GB)+np.array(int_CI)+np.array(int_BF)+np.array(int_BN)
    val_euro = np.array(Euro_sn)+ np.array(Euro_tg)+np.array(Euro_ng)+np.array(Euro_ml)+np.array(Euro_gb)+np.array(Euro_ci)+np.array(Euro_bf)+np.array(Euro_bn)


col1, col2, col3 = st.columns(3, gap='small')

with col1:
    fig = go.Figure()

    fig.add_trace(go.Bar(x=all_year, y=m_cap, name="Principal", marker_color='rgb(133, 32, 12)'))
    fig.add_trace(go.Bar(x=all_year, y=m_interet, name="Intérêt", marker_color='orange'))

    # Configuration en mode empilé
    fig.update_layout(
        barmode="stack",  # Mode empilé
        title="Évolution du service de la dette (" + m_pays+ ')',
        yaxis_title="Montant en mds FCFA",
        legend_title="Dette"
    )   

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x= tx_dure,
        y= tx_valeur, 
        text= tx_valeur,
        name='Primary Product', marker_color='rgb(100, 132, 12)', marker=dict(cornerradius="25%")) )

    fig.layout.template = CHART_THEME
    fig.update_layout(
        title= {
            'text':'Taux moyen pondérés (' + m_pays+ ')',
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=dict(
            text="en %",
            font=dict(size=12, color="gray")
        )),
         )

    st.plotly_chart(fig, use_container_width=True)

with col3:
    #tab1, tab2 = st.tabs(["Eurobond par Année", "Eurobonds par Pays"])

    #with tab1:
    m_chart = go.Figure()

    m_chart.add_trace(go.Bar(x=all_year, y=val_euro, marker_color='rgb(133, 32, 12)', name='Global'))
# m_chart.add_trace(go.Scatter(x=df_idx["BRVM_TRP"].index, y=df_idx["BRVM_SRP"], mode='lines', line=dict(color='rgb(133, 32, 12)'), name='Global'))
    m_chart.layout.template = CHART_THEME
    #m_chart.update_layout(margin = dict(t=50, b=50, l=25, r=25))
    m_chart.update_layout(
        title= {
            'text':'Evolution des Eurobonds ('+ m_pays+ ')',
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title=dict(
            text="Points",
            font=dict(size=12, color="gray")
        ),
        ))

    st.plotly_chart(m_chart, use_container_width=True)
st.info("**_Conclusion MTP:_** Le MTP est...")
#######################################
# Indicateur Line 2
#######################################
obli_2019 = [2505.31,1458.41,1840.07,2680.77,2648.21,2349.45,1712.04,1898.08,2807.41,2302.05,1696.77,1883.78]
obli_2020 = [1120.27,2479.62,768.15,2756.8,809.86,2084.25,1879.28,822.42,1539.94,1318.56,2849.2,2768.08]
obli_2021 = [1868.88,2181.84,1183.97,1232.85,2817.07,1358.57,1359.05,1458.92,739.48,1935.59,2671.31,1425.76]
obli_2022 = [1256.74,2116.65,2602.32,1067.3,1760.87,2638.02,2387.65,1083.68,1298.24,830.93,2817.79,2260.62]
obli_2023 = [722.57,2309.81,1235.08,1606.97,938.16,1083.58,896.77,2317.29,923.43,1906.66,1489.97,1473.82] 
obli_2024 = [2632.32,2554.19,2800.58,2057.39,2458.52,2280.06,1901.63,1244.83,2522.21,2442.1,1586.63,1296.49]

all_oblig = [obli_2019, obli_2020, obli_2021, obli_2022, obli_2023, obli_2024]

divid_dist = [[0.2, 0.25, 0.55], [0.3, 0.35, 0.35],[0.15, 0.25, 0.6],
[0.4,0.4,0.2],[0.4,0.4,0.2],[0.1,0.2,0.7]]

an_2019 = [502.4, 117.9, 506.1, 213.8, 143.7, 118.9, 706.1, 126.1, 527.5, 439.4, 794.7, 669.3]
an_2020 = [544.18,707.06,558.8,252.81,262.92,404.21,732.19,241.18,754.58,678.83,102.73,337.68]
an_2021 = [376.3,524.85,247.37,182.15,380.85,284.42,160.21,598.85,103.1,223.54,657.03,486.43]
an_2022 = [630.23,650.91,426.01,652.43,363.53,790.77,225.85,340.16,275.86,364.29,789.86,755.69]
an_2023 = [100.68,350.5,308.74,604.78,237.56,695.93,733.44,644.68,652.04,629.22,472.47,655.46] 
an_2024 = [835.54,648.33,501.57,142.07,142.64,791.31,531.33,766.41,743.32,420.33,306.35,669.29]

all_action = [an_2019, an_2020,an_2021, an_2022, an_2023, an_2024]

data = {
    "2019": an_2019,
    "2020": an_2020,
    "2021": an_2021,
    "2022": an_2022,
    "2023": an_2023,
    "2024": an_2024,
}

action_tran = pd.DataFrame(data)
m_absci = ""

if v_periode == "Année" :
    m_absci = all_year
    val_action = [round(sum(an_2019)), round(sum(an_2020)), round(sum(an_2021)), round(sum(an_2022)), round(sum(an_2023)),round(sum(an_2024))]
    val_oblig =  [round(sum(an_2019)), round(sum(an_2020)), round(sum(an_2021)), round(sum(an_2022)), round(sum(an_2023)),round(sum(an_2024))]
elif v_periode == "Semestre":
    m_absci = ["2019 Sem 1", "2019 Sem 2", "2020 Sem 1", "2020 Sem 2", "2021 Sem 1",
                "2021 Sem 2", "2022 Sem 1", "2022 Sem 2","2023 Sem 1", "2023 Sem 2"]
    sem_11 = round(sum(an_2019[:6]),2) 
    sem_12 = round(sum(an_2019[6:]),2) 
    sem_21 = round(sum(an_2020[:6]),2) 
    sem_22 = round(sum(an_2020[6:]),2) 
    sem_31 = round(sum(an_2021[:6]),2) 
    sem_32 = round(sum(an_2021[6:]),2) 
    sem_41 = round(sum(an_2022[:6]),2) 
    sem_42 = round(sum(an_2022[6:]),2) 
    sem_51 = round(sum(an_2023[:6]),2) 
    sem_52 = round(sum(an_2023[6:]),2) 
    val_action = [sem_11, sem_12, sem_21,sem_22, sem_31, sem_32,sem_41,sem_42,sem_51,sem_52]

    ob_sem_11 = round(sum(obli_2019[:6]),2) 
    ob_sem_12 = round(sum(obli_2019[6:]),2) 
    ob_sem_21 = round(sum(obli_2020[:6]),2) 
    ob_sem_22 = round(sum(obli_2020[6:]),2) 
    ob_sem_31 = round(sum(obli_2021[:6]),2) 
    ob_sem_32 = round(sum(obli_2021[6:]),2) 
    ob_sem_41 = round(sum(obli_2022[:6]),2) 
    ob_sem_42 = round(sum(obli_2022[6:]),2) 
    ob_sem_51 = round(sum(obli_2023[:6]),2) 
    ob_sem_52 = round(sum(obli_2023[6:]),2) 

    val_oblig =[ob_sem_11, ob_sem_12, ob_sem_21, ob_sem_22, ob_sem_31, ob_sem_32, ob_sem_41, ob_sem_42, ob_sem_51 ,ob_sem_52]

elif v_periode == "Trimestre":
    m_absci = ["Trim 1", "Trim 2", "Trim 3", "Trim 4"]
    val_action = all_action[m_controler]
    trim_1 = round(sum(val_action[:3]),2)
    trim_2 = round(sum(val_action[3:6]),2)
    trim_3 = round(sum(val_action[6:9]),2)
    trim_4 = round(sum(val_action[3:]),2)
    val_action = [trim_1, trim_2, trim_3,trim_4]

    val_oblig = all_oblig[m_controler]
    trim_1 = round(sum(val_oblig[:3]),2)
    trim_2 = round(sum(val_oblig[3:6]),2)
    trim_3 = round(sum(val_oblig[6:9]),2)
    trim_4 = round(sum(val_oblig[3:]),2)

    val_oblig = [trim_1, trim_2, trim_3,trim_4]

elif v_periode == "Mois":
    m_absci = all_months
    val_action = all_action[m_controler]
    val_oblig = all_oblig[m_controler]

m_revenus = ['Dividend','Interet', "Capitaux Remb."]
y_2019 = [1500, 2500, 4200]
y_2020 = [3500, 900, 1035]
y_2021 = [2300, 1340, 3000]
y_2022 = [2000,4000,6000]
y_2023 = [3500, 900, 1035]
y_2024 = [1600,2200,4100]

sel_data = []
if v_annee == 2019: sel_data = y_2019
elif v_annee == 2020: sel_data = y_2020
elif v_annee == 2021: sel_data = y_2021
elif v_annee == 2022: sel_data = y_2022
elif v_annee == 2023: sel_data = y_2023
elif v_annee == 2024: sel_data = y_2024


st.markdown('#### Marché des Obligations')

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    fig = go.Figure()
    m_h_sem = m_absci
    m_param = "Valeur"
    m_h_values = val_oblig

    fig.add_trace(go.Bar(
        x=m_h_values,
        y= m_h_sem,
        orientation = 'h',
        text = m_h_values,
        name='Vol_sect', marker_color='rgb(237, 224, 212)', marker=dict(cornerradius="40%")) )

    fig.layout.template = CHART_THEME
    fig.update_layout(
        title= {
            'text':'Montants mobilisés sur le marché primaire',
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Montant (en milliards FCFA)',
            ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=m_absci, y=val_oblig, mode='lines+markers+text', text =val_oblig, textposition="top center"))

    fig.update_layout(
    title= {
            'text':'Montants transigés sur le marché secondaire',
            'y':0.9,
            'x':0.5,
            'xanchor': "center",
            'yanchor': 'top'
        },
    legend=dict(
        orientation="h",  # Légende horizontale
        y=-0.2,  # Ajustement vertical sous le graphique
        x=0.5,   # Centrage horizontal
        xanchor="center",
        yanchor="top"
    ))

    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = go.Figure(data=[go.Pie(labels=m_revenus, values=sel_data, hole=.5)])
    fig.update_layout(
        title="Répartition des revenus (en mds FCFA)",
        title_x=0.2,
        height=500,  # Hauteur du graphique
        width=500,    # Largeur du graphique
        legend=dict(
        orientation="h",  # Légende horizontale
        y=-0.2,  # Ajustement vertical sous le graphique
        x=0.25,   # Centrage horizontal
        xanchor="center",
        yanchor="top"
        )
    )

    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=13,
                  )
    
    st.plotly_chart(fig, use_container_width=True)

st.info("**_Conclusion Marché Obligations_**")
#######################################
# Chart Line 3 : Actions
#######################################
with st.expander("INDICATEURS ACTIONS"):
    st.markdown("#### Marché d'actions BRVM")
    col1, col2 = st.columns(2, gap="small")
    data = {
        "Revenus" : ['Dividend','Interet', "Capitaux Remb."],
        "2019": [1500, 2500, 4200],
        "2020": [3500, 900, 1035],
        "2021": [2300, 1340, 3000],
        "2022": [2000,4000,6000],
        "2023": [3500, 900, 1035],
        "2024": [1600,2200,4100],
    }

    revenu_dist = pd.DataFrame(data)

    with col1:
        m_val = []
        df_l3 = 0
        for i in range(0, len(m_secteur_3)):
            m = m_secteur_3[i]
            if   m   == "BRVM Composite": m_val.append("BRVM_C") 
            elif m == "BRVM 30": m_val.append("BRVM_30")  
            elif m == "BRVM Prestige": m_val.append("BRVM_PRES")  
            elif m == "BRVM Principal": m_val.append("BRVM_PRI")  
            elif m == "Industrie": m_val.append("BRVM_IND")  
            elif m == "Serv. Publics": m_val.append("BRVM_SRP")  
            elif m == "Finances": m_val.append("BRVM_FIN")  
            elif m == "Transport": m_val.append("BRVM_TRP")  
            elif m == "Agriculture": m_val.append("BRVM_AGR")  
            elif m == "Distribution": m_val.append("BRVM_DIS")  
            elif m == "Autres": m_val.append("BRVM_AUT")  

        if v_annee == 2024:
            df_l3 = df_index_2[235:]
        else:
            df_l3 = df_index_2[:235]

        
        st.markdown('###### Evolution des indices boursiers')
        st.line_chart(df_l3, x = 'Séance', y = m_val )

    with col2:
        fig = go.Figure()
        m_secteur = "Total"
        m_semestres = m_absci
        m_value = val_action
        fig.add_trace(go.Bar(
            x=m_semestres,
            y= m_value, 
            text= m_value,
            name='Primary Product', marker_color='rgb(133, 32, 12)', marker=dict(cornerradius="10%")) )

        fig.layout.template = CHART_THEME
        fig.update_layout(
            title= {
                'text':'Montant Actions transigées',
                'y':0.9,
                'x':0.5,
                'xanchor': "center",
                'yanchor': 'top'
            },
            xaxis_tickfont_size=12,
            yaxis=dict(
                title=dict(
                text="Milliards (FCFA)",
                font=dict(size=12, color="gray")
            ),
             ))

        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2, gap="small")

    with col1:
        fig = go.Figure()

        semLiq_1 = round(df_liq['2022-01-01':'2022-06-30'].mean(),2 )
        semLiq_2 = round(df_liq['2022-07-01':'2022-12-31'].mean(),2 )
        semLiq_3 = round(df_liq['2023-01-01':'2023-06-30'].mean(),2 )
        semLiq_4 = round(df_liq['2023-07-01':'2023-12-31'].mean(),2 )
        semLiq_5 = round(df_liq['2024-01-01':'2024-06-30'].mean(),2 )

        m_semestres = ["Sem1_2022","Sem2_2022","Sem1_2023","Sem2_2023","Sem1_2024"]
        m_values = [semLiq_1["ratio_liquidité_pct"] , semLiq_2["ratio_liquidité_pct"], semLiq_3["ratio_liquidité_pct"], 
                    semLiq_4["ratio_liquidité_pct"], semLiq_5["ratio_liquidité_pct"]]
        fig.add_trace(go.Bar(
            x=m_semestres,
            y=m_values,
            text = m_values,
            width= [0.3,0.3,0.3,0.3,0.3], name='Vol_sect', marker_color='rgb(133, 32, 12)', marker=dict(cornerradius="10%")) )

        fig.layout.template = CHART_THEME
        fig.update_layout(
            title= {
                'text':'Evolution du taux de liquidité de 2022 à juin 2024',
                'y':0.9,
                'x':0.5,
                'xanchor': "center",
                'yanchor': 'top'
            },
            xaxis_tickfont_size=12,
            yaxis=dict(
                title='Pourcentage (%)',
                
                ))
        st.plotly_chart(fig, use_container_width=True)

    st.info("** _Conclusion:_ **")

def m_upload():
    st.subheader("Mise à jour")

    datafile = st.file_uploader("Upload un fichier excel ou CSV", type=["xlsx"])
    if datafile is not None:
        file_detail = {"Filename": datafile.name, "FileType":datafile.type}
        df = pd.read_excel(datafile)
        # st.dataframe(df)
        st.success('Fichier chargé.')
     
         
 
m_upload()

 
