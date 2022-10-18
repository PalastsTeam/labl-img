import streamlit as st
import gspread as gs

gs_url = 'https://docs.google.com/spreadsheets/d/1A0LQ8Lich8OAWl-iTsBkEti5-z3CTnyxzSTpEO9wCMA'


def get_items():
    gc = gs.service_account(filename='cred.json')
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)
    return worksheet.get_all_records()


def save_into_csv(filename, types, styles, pattern, material, symetrie, nlegs, leg_length, leg_width, leg_form, leg_direction, leg_color, back_length, back_form, back_direction, n_arms, arm_form, arm_direction):
    gc = gs.service_account(filename='cred.json')
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)

    new_row = [filename, types, styles, pattern, material, symetrie, nlegs, leg_length, leg_width,
               leg_form, leg_direction, leg_color, back_length, back_form, back_direction,
               n_arms, arm_form, arm_direction]
    worksheet.append_row(new_row)
    st.write('Submitted to database!')
