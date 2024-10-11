import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import utils as utl



# Function to send the email
def send_email(to_email, from_email, subject, message_body):
    # Email server (using Gmail as an example)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "your_email@gmail.com"  # Replace with your email
    smtp_password = "your_password"  # Replace with your password

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the message body
    msg.attach(MIMEText(message_body, "plain"))

    # Send the email via SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Streamlit app layout
#st.title("Contact Us")

# Create a centered layout using columns
col1, col2, col3 = st.columns([1, 2, 1])  # The middle column (col2) is wider to center the content

with col2:
    st.header("Send us some feedback...",)
    
    # Create a form for user input
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        # Submit button
        submitted = st.form_submit_button("Send Message")

# Process the form submission
if submitted:
    if not name or not email or not message:
        st.error("Please fill in all fields before submitting.")
    else:
        # Compose the email message
        subject = f"Message from {name} via Contact Form"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send the email
        success = send_email("recipient_email@example.com", email, subject, body)
        
        if success:
            st.success("Your message has been sent successfully!")
        else:
            st.error("Failed to send your message. Please try again.")
