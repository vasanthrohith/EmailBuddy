import streamlit as st
from modules.make_mail import MakeMail
from modules.send_mail import SendMail_Notify
          
def main():
    st.markdown(
        """
        <h1 style="text-align: center; font-size: 3em;">
            📧 MAIL BUDDY
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Initial user input fields
    sender_email = st.text_input("Sender Email:", "")
    recipient_email = st.text_input("Recipient Email:", "")
    mail_content = st.text_area("Mail Content:", "")

    # Button to submit the initial form
    if st.button("Submit"):
        if sender_email and recipient_email and mail_content:
            st.info("Generating Professional Mail")

            # Model (Placeholder)
            # response = "bla"  # Placeholder for actual model response

            obj=MakeMail()
            generated_mail=obj.Make_Formal_Mail(user_content=mail_content, recipient_mail=recipient_email, sender_mail=sender_email)


            if generated_mail:
                # Display the values entered in 'Subject' and 'Mail Body'
                st.write("**Subject:**", generated_mail['make_mail_response']['subject'])
                st.write("**Mail Body:**", generated_mail['make_mail_response']['mail_body'])
 
                print("Sending mail")
                mail_obj = SendMail_Notify()
                mail_obj.Send_Mail(subject=generated_mail['make_mail_response']['subject'], mail_body=generated_mail['make_mail_response']['mail_body'], sender_mail=sender_email, rec_mail=[recipient_email])
                st.success("Email Sent successfully!")

        else:
            st.error("Please fill in all the fields before submitting.")

if __name__ == "__main__":
    main()
