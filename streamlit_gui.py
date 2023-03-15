import streamlit as st
from modules.utils import thread, del_user, add_user, read_profiles, read_logs, stop_event, set_defaults, delete_defaults
profiles = read_profiles()

st.header('Spotify Bot')
container = st.empty()
with container:
    column = st.columns(2)
    with column[0]:
        with st.form(key='start'):
            #headless = st.checkbox(label='Headless', value=True)
            #mute = st.checkbox(label='Mute', value=False)
            playlist_url = st.text_input(label= 'Playlist URL', placeholder='Leave Empty to use Default')
            proxy_url = st.text_input(label= 'Proxy URL', placeholder='Leave Empty to use Default')
            set_links = st.form_submit_button(label="Set URL's")

        with st.form(key='Set Default URL', clear_on_submit=True):
            new_playlist_url = st.text_input('Set Default Playlist URL',  placeholder='Enter the playlist URL')
            new_proxy_url = st.text_input('Set Default Proxy URL', placeholder="Enter the proxy URL")
            
            set_default = st.form_submit_button(label='Set Defaults')
            if set_default:
                set_defaults(new_playlist_url, new_proxy_url)
   
        start = st.button(label='Start', on_click=thread, args=[proxy_url, playlist_url])

    with column[1]:

        with st.form(key='new_user', clear_on_submit=True):
            new_mail = st.text_input(label='Add Mail Address', placeholder='name@mail.com')
            new_password = st.text_input(label='Add Password', type='password')
            add_user_button = st.form_submit_button(label='Add User')
            if add_user_button:
                add_user(new_mail,new_password)

        with st.form(key='delete_user', clear_on_submit= True):
            try:
                opt = [ f"{i['username']}" for i in profiles['credentials']]
            except:
                opt = []
            del_username = st.multiselect(label='Select Accounts to Delete', options=opt )
            delete_user_button = st.form_submit_button(label='Delete')
            if delete_user_button:
                del_user(del_username)
            
        with st.form(key='delete_defaults', clear_on_submit=True):
            res_playlist_default = st.checkbox(label="Remove Default Playlist")
            res_proxy_default = st.checkbox(label="Delete Default Proxy")
            delete_defaults_button = st.form_submit_button(label="Delete Defaults")
            if delete_defaults_button:
                delete_defaults(res_playlist_url= res_playlist_default, res_proxy_url = res_proxy_default )
#info_cols = st.columns(3)
#info_cols[0].info( """ ***Active Accounts:***\n{} """.format("\n".join(opt)))
#info_cols[1].info("Active Playlist: {} \nActive Proxy: {}".format(proxy_url, playlist_url))
#st.text('Run The Program')


table = st.empty()
table.dataframe( read_logs() )

if start:
    stop_event.clear()
    table.dataframe( read_logs() )

    with container.form(key ='Stop'):
        st.warning( body= f"Running on { len( profiles['credentials'] ) } bots." )

        stop = st.form_submit_button('Stop', on_click=stop_event.set)
        if stop:
            st.error('Please Wait Until All Browsers Closes')
            st.stop()
        

