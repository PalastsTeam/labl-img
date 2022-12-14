import streamlit as st
import gspread as gs
import os
import pandas as pd
from src.helpers import get_items, save_into_csv
import datetime

all_items = os.listdir('img')

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.answers = 0

credentials = {
    "type": "service_account",
    "project_id": "labelling-365915",
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": "labelling@labelling-365915.iam.gserviceaccount.com",
    "client_id": st.secrets["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/labelling%40labelling-365915.iam.gserviceaccount.com"
}
gs_url = st.secrets["url"]

gc = gs.service_account_from_dict(credentials)
sh = gc.open_by_url(gs_url)
worksheet = sh.get_worksheet(0)
data = worksheet.get_all_records()


labeled_items = pd.DataFrame(data)['Filename'].unique()

final_list = list(set(all_items) - set(labeled_items))

filename = final_list[st.session_state.count]
path = "img/{}".format(filename)


with st.sidebar:
    st.image(path)
    skipped = st.checkbox('Skipped?', False)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader('Overal')

    types = st.multiselect(
        'Motivational Type',
        ['Mondän', 'Rational', 'Fürsorglich', 'Traditionel', 'Unabhängig'],
        ['Mondän', 'Rational', 'Fürsorglich', 'Traditionel', 'Unabhängig'],
        key='type')

    styles = st.multiselect(
        'Style',
        ['Midcentury', 'Landhause', 'Modern', 'Classic', 'Industrial', 'Other'],
        ['Midcentury'],
        key='style')

    pattern = st.multiselect(
        'Pattern',
        ['unifarbig', 'blumen', 'streifen', 'kariert', 'other'],
        ['unifarbig'],
        key='pattern'
    )

    material = st.multiselect('Main Material', ['holz',
                                                'samt',
                                                'leder',
                                                'stoff',
                                                'metal',
                                                'rattan',
                                                'plastik',
                                                'other'],
                              key='material'
                              )
    farbe = st.multiselect('Farbe', ['grau',
                                     'blau',
                                     'braun',
                                     'grün',
                                     'beige',
                                     'rot',
                                     'gelb',
                                     'rosa',
                                     'gold',
                                     'silber',
                                     'schwarz',
                                     'weiß',
                                     'lila',
                                     'orange'],
                           key='farb'
                           )

    symetrie = st.checkbox('Is symetric?', True)


with col2:
    st.subheader('Legs')

    nlegs = st.slider('How many legs', min_value=0,
                      max_value=5, value=4, key='nlegs')

    leg_length = st.multiselect(
        'Leg length',
        ['lang', 'mittel', 'kurz'],
        ['mittel'],
        key='llength')

    leg_width = st.multiselect(
        'Leg thickness',
        ['extra thin', 'thin', 'mittel', 'thick'],
        ['thin'],
        key='lthick')

    leg_form = st.multiselect(
        'Leg form',
        ['straight', 'bended', 'curvy'],
        ['straight'],
        key='lform')

    leg_direction = st.checkbox('Standing out legs?')

    # leg_direction = st.multiselect(
    #    'Leg direction',
    #    ['straight', 'standingout'],
    #    ['standingout'],
    #    key='ldir')

    leg_color = st.multiselect(
        'Leg color',
        ['light holz', 'dark holz', 'chrom', 'gold',
         'schwarz', 'weiß', 'other'],
        [],
        key='lcol')

with col4:
    st.subheader('Rücklehne')
    back_length = st.multiselect(
        'Back length',
        ['short', 'mittel', 'long', 'extralong', 'none'],
        [],
        key='blength')

    back_form = st.multiselect(
        'Back form',
        ['eckig', 'rund', 'curvy'],
        ['eckig', 'rund', 'curvy'],
        key='bform')

    back_direction = st.checkbox('Standing out back?')


with col3:
    st.subheader('Armlehne')
    n_arms = st.slider('N Armlehnen', min_value=0, max_value=2)

    arm_form = st.multiselect(
        'Armlehnen form',
        ['eckig', 'rund', 'curvy'],
        ['rund'],
        key='aform')

    # arm_direction = st.multiselect(
    #    'Armlehnen direction',
    #    ['streight', 'standingout'],
    #    ['standingout'],
    #    key='adir')
    arm_direction = st.checkbox('Standing out armrests?')

increment = st.button('Confirm')
if increment:
    st.session_state.count += 1

    save_into_csv(str(filename), str(types), str(styles),
                  str(pattern), str(material), str(
                      farbe), str(symetrie), str(nlegs),
                  str(leg_length), str(leg_width), str(
                      leg_form), str(leg_direction),
                  str(leg_color), str(back_length), str(
                      back_form), str(back_direction), str(n_arms),
                  str(arm_form), str(arm_direction), str(skipped))

    st.write('Thanks! Saved!')
    with st.sidebar:
        st.button('Next')
