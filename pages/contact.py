import streamlit as st


# Access the theme settings
primary_color = st.get_option("theme.primaryColor")



st.markdown(
    f"""
    <style>
    .centered {{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        text-align: center;
        margin-top: 20px;
    }}
    .centered ul {{
        text-align: left; /* Ensure the list items are left-aligned */
        list-style-position: inside; /* Ensure bullets are inside the content box */
        padding-left: 0; /* Remove default padding for ul */
    }}
    .centered li {{
        margin-left: 20px; /* Optional: Add space before list items */
    }}
    .custom-button {{
        font-size: 20px; 
        text-decoration: none; 
        color: white !important;  /* Force text color to white */
        background-color: {primary_color}; 
        padding: 10px 20px; 
        border-radius: 5px;
    }}
    </style>
    <div class="centered">
        <h3>Contact</h3>
        <p>Please send feedback, comments, bugs etc. to: 
        <a href="mailto:mpentzek@ssnaplogic.com">mpentzek@snaplogic.com</a>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)
