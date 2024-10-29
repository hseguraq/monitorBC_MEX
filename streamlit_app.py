
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Sistema de Monitoreo del Cáncer de Mama en México'
APP_SUB_TITLE = 'Variables indicadoras basadas en información de CONAPO'

# def display_time_filters(df):
#     year_list = list(df['Year'].unique())
#     year_list.sort()
#     year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
#     quarter = st.sidebar.radio('Quarter', [1, 2, 3, 4])
#     st.header(f'{year} Q{quarter}')
#     return year, quarter

# def display_state_filter(df, state_name):
#     state_list = [''] + list(df['State Name'].unique())
#     state_list.sort()
#     state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
#     return st.sidebar.selectbox('State', state_list, state_index)

# def display_report_type_filter():
#     return st.sidebar.radio('Report Type', ['Fraud', 'Other'])

# def display_map(df, year, quarter):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

#     map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
#     choropleth = folium.Choropleth(
#         geo_data='data/us-state-boundaries.geojson',
#         data=df,
#         columns=('State Name', 'State Total Reports Quarter'),
#         key_on='feature.properties.name',
#         line_opacity=0.8,
#         highlight=True
#     )
#     choropleth.geojson.add_to(map)

#     df_indexed = df.set_index('State Name')
#     for feature in choropleth.geojson.data['features']:
#         state_name = feature['properties']['name']
#         feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
#         feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

#     choropleth.geojson.add_child(
#         folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
#     )
    
#     st_map = st_folium(map, width=700, height=450)

#     state_name = ''
#     if st_map['last_active_drawing']:
#         state_name = st_map['last_active_drawing']['properties']['name']
#     return state_name

# def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
#     df = df[df['Report Type'] == report_type]
#     if state_name:
#         df = df[df['State Name'] == state_name]
#     df.drop_duplicates(inplace=True)
#     if is_median:
#         total = df[field].sum() / len(df[field]) if len(df) else 0
#     else:
#         total = df[field].sum()
#     st.metric(title, string_format.format(round(total)))

def display_RC_LOC(df, nivel_riesgo, title):

    if nivel_riesgo != 'Todos':
        df = df[df['Etiquetas_RiesgoC'] == nivel_riesgo]
        df = df[['AGEB', 'POB_TOTAL', 'Etiquetas_RiesgoC', 'GM_2020']]
        title = f'Número de localidades con nivel de riesgo **{nivel_riesgo}** en el municipio de San Luis Potosí'

    else:
        title = f'Número total de localidades en San Luis Potosí'

    
    df = df[['AGEB', 'POB_TOTAL', 'Etiquetas_RiesgoC', 'GM_2020']]
    instancias  = len(df)
    st.metric(title, instancias)

def display_map(df, riesgo):
    import folium

# Coordinates for San Luis Potosí, Mexico
    latitude = 22.1565
    longitude = -100.9855


    map = folium.Map(location=[latitude, longitude], zoom_start=12, tiles='CartoDB positron')

    cloropleth = folium.Choropleth(
        geo_data = 'data/output_RC_LOC.geojson',
        data = df,
        columns= ('AGEB', 'RC_num'),
        key_on= 'feature.properties.CVE_AGEB',
        line_opacity= 0.8,
        highlight= True

    )

    cloropleth.geojson.add_to(map)
    cloropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['CVE_AGEB','RC' ,'IM3', 'GM'])
    )

    st_map = st_folium(map, width = 700, height=450)

    # st.write(df.head())
    # st.write(df.columns)



def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    df_loc = pd.read_csv('data/TablaFINAL_labels_LOC_tentativo.csv')
    df_def_gen = pd.read_csv('data/BDmortalidadCAMAbase.csv')
    df_rc_loc = pd.read_csv('data/etiquetas_RC_loc.csv')

    title_def_slp = 'Número de defunciones en el municipio de San Luis Potosí, 2020'
    df_def_slp = df_def_gen[(df_def_gen['cve_ent'] == 24) & (df_def_gen['cve_mun'] == 28) & (df_def_gen['anio_cert'] == 2020)]
    st.metric(title_def_slp, len(df_def_slp))

    

    nivel_riesgo= 'Muy alto'

    title = 'Índice de riesgo y marginación para localidades del municipio de San Luis Potosí'

    
    custom_order = ["Todos", "Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
    riesgo = st.sidebar.selectbox('Nivel de Riesgo', custom_order)
    if riesgo != 'Todos':
        df_rc_loc = df_rc_loc[df_rc_loc['Etiquetas_RiesgoC'] == riesgo]



    display_RC_LOC(df_loc, riesgo, title)


    # #Display Filters and Map
    
    risk_labels = list(df_rc_loc['Etiquetas_RiesgoC'].unique())
    
    # st.write(custom_order) 


    display_map(df_rc_loc, riesgo)




    
    # st.write(df_loc.columns)

    

    # df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
    # df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
    # df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

    # #Display Filters and Map
    # year, quarter = display_time_filters(df_continental)
    # state_name = display_map(df_continental, year, quarter)
    # state_name = display_state_filter(df_continental, state_name)
    # report_type = display_report_type_filter()

    # #Display Metrics
    # st.subheader(f'{state_name} {report_type} Facts')

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     display_fraud_facts(df_fraud, year, quarter, report_type, state_name, 'State Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
    # with col2:
    #     display_fraud_facts(df_median, year, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
    # with col3:
    #     display_fraud_facts(df_loss, year, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')        


if __name__ == "__main__":
    main()