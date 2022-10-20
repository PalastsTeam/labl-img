import streamlit as st
import gspread as gs
import datetime

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


def get_items():
    gc = gs.service_account_from_dict(credentials)
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)
    return worksheet.get_all_records()


def save_into_csv(filename, types, styles, pattern, material, symetrie, nlegs, leg_length, leg_width, leg_form, leg_direction, leg_color, back_length, back_form, back_direction, n_arms, arm_form, arm_direction, skipped):
    gc = gs.service_account_from_dict(credentials)
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)

    new_row = [filename, types, styles, pattern, material, symetrie, nlegs, leg_length, leg_width,
               leg_form, leg_direction, leg_color, back_length, back_form, back_direction,
               n_arms, arm_form, arm_direction, str(datetime.datetime.now()), skipped]
    worksheet.append_row(new_row)
    st.write('Submitted to database!')
