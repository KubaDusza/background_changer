from constants import *
from imports import *


def sticky_header():
    header = st.container()
    header.header(NAME_OF_THE_SITE + "  " + MAIN_ICON)
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    # Custom CSS for the sticky header
    st.markdown(
        """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            background: #0E1117;
            top: 2rem;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 4px solid #262730;
        }
    </style>
        """,
        unsafe_allow_html=True
    )