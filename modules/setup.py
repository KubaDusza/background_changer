from constants import *
from imports import *


def setup():
    st.set_page_config(
        page_title=NAME_OF_THE_SITE,
        page_icon=MAIN_ICON,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "About": "mailto: jacob.dusza@gmail.com linkedin:https://www.linkedin.com/in/jakub-dusza-041a9023b/",
            # "Get help": "https://www.youtube.com/",
            # "Report a bug": "https://www.youtube.com/"
        }
    )

    if "threshold_reset_counter" not in st.session_state:
        st.session_state.threshold_reset_counter = 0


    if "access_key" not in st.session_state:
        st.session_state.access_key = ""

    if "images" not in st.session_state:
        st.session_state.images = {}

    if "inverted" not in st.session_state:
        st.session_state.inverted = False

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None



def grant_access():
    allowed_emails = st.secrets.get("ALLOWED_EMAILS")
    allowed_access_keys = st.secrets.get("ALLOWED_ACCESS_KEYS")

    if (st.experimental_user.email in allowed_emails) or (
            st.session_state.access_key in allowed_access_keys) or REMOVE_RESTRICTIONS:
        return True
    else:
        if st.experimental_user.email is None:
            st.write("streamlit removed ability to see logged in account (?), so use an access key instead.")
            #st.write(
            #    "You are not logged in. You can log in or create streamlit accout here:\n https://share.streamlit.io/")
        else:
            st.write(f"sorry, email {st.experimental_user.email}has no access. Log in to an allowed account")

        st.write("Paste an access key:")

        st.session_state.access_key = st.text_input(label="access key", label_visibility="collapsed", type="password",
                                                    placeholder="access key")

        if st.session_state.access_key in allowed_access_keys:
            st.rerun()
