import streamlit as st
from service import LNbits

# Initialize LNbits client
client = LNbits("localhost:5001", use_https=False)

# Wallet keys
wallet1_adminkey = "a141d91d41f34c1dae0db0689bb46191"  # Lender
wallet2_adminkey = "d2adf110d55b4aa1b449c38c7a57d512"  # Borrower

def main():
    st.title("Welcome to BitLoan!")
    st.write("A Bitcoin Micro Loan Platform brought to you by the Lightning Network.")

    # Role selection
    role = st.radio("Please select an option to begin:", ["Request Loan", "Repay Loan"])

    if role == "Request Loan":
        st.header("Loan Request Dashboard")
        
        # Loan request form
        with st.form("loan_request"):
            amount = st.number_input("Amount to borrow (in sats):", min_value=1, value=1000)
            submit_button = st.form_submit_button("Request Loan")

            if submit_button:
                try:
                    # Create loan request invoice
                    invoice_borrower = client.create_invoice(
                        wallet_key=wallet2_adminkey,
                        amount_sats=amount,
                        memo="Borrower's Loan Request"
                    )

                    # Process payment
                    client.pay_invoice(
                        wallet_adminkey=wallet1_adminkey,
                        invoice=invoice_borrower.payment_request
                    )
                    
                    st.success(f"Loan of {invoice_borrower.amount} sats approved!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    else:
        st.header("Loan Repayment Dashboard")
        
        # Repayment form
        with st.form("loan_repayment"):
            amount = st.number_input("Amount to repay (in sats):", min_value=1, value=1000)
            submit_button = st.form_submit_button("Submit Repayment")

            if submit_button:
                try:
                    # Create repayment invoice
                    invoice_lender = client.create_invoice(
                        wallet_key=wallet1_adminkey,
                        amount_sats=amount,
                        memo="Borrower's Loan Repayment"
                    )

                    # Process payment
                    client.pay_invoice(
                        wallet_adminkey=wallet2_adminkey,
                        invoice=invoice_lender.payment_request
                    )
                    
                    st.success(f"Successfully received {invoice_lender.amount} sats repayment!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 