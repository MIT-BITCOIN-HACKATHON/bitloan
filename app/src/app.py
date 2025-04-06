import streamlit as st
from service import LNbits
from typing import List, Dict
import time

# Initialize LNbits client
client = LNbits("localhost:5001", use_https=False)

# Wallet keys
lender1_adminkey = "a141d91d41f34c1dae0db0689bb46191"  
lender2_adminkey = "cacb571208fc4799a7dbd68096f7071f"
lender3_adminkey = "71afadfe18bd40368bddd154035100b1"
borrower1_adminkey = "d2adf110d55b4aa1b449c38c7a57d512" 

# Lender information
LENDERS = {
    "Lender 1": {
        "key": lender1_adminkey,
        "rate": "15% for 1 month",
        "min_amount": 10,
        "max_amount": 100
    },
    "Lender 2": {
        "key": lender2_adminkey,
        "rate": "10% for 2 months",
        "min_amount": 20,
        "max_amount": 200
    },
    "Lender 3": {
        "key": lender3_adminkey,
        "rate": "5% for 3 months",
        "min_amount": 30,
        "max_amount": 300
    }
}

# Global list to store available loan requests
if 'available_loans' not in st.session_state:
    st.session_state.available_loans = []
if 'approved_loans' not in st.session_state:
    st.session_state.approved_loans = []
if 'loan_balances' not in st.session_state:
    st.session_state.loan_balances = {}

def get_lender_key(lender_name: str) -> str:
    """Get the admin key for the selected lender"""
    return LENDERS[lender_name]["key"]

def get_loan_balance(loan_id: str) -> int:
    """Get the remaining balance for a loan"""
    return st.session_state.loan_balances.get(loan_id, 0)

def update_loan_balance(loan_id: str, payment_amount: int):
    """Update the remaining balance for a loan after a payment"""
    current_balance = get_loan_balance(loan_id)
    st.session_state.loan_balances[loan_id] = max(0, current_balance - payment_amount)

def display_available_loans(amount: int) -> List[Dict]:
    """Filter and display loans that match the lender's amount"""
    matching_loans = [loan for loan in st.session_state.available_loans if loan['amount'] == amount]
    if not matching_loans:
        st.info("No Loans Available for your Amount at this time")
        return []
    
    st.write("Available Loans:")
    for i, loan in enumerate(matching_loans, 1):
        st.write(f"{i}. Amount: {loan['amount']} sats (Requested at {loan['time']})")
    return matching_loans

def display_lender_options(amount: int) -> List[str]:
    """Display available lenders based on loan amount"""
    available_lenders = []
    st.write("Available Lenders:")
    
    for lender_name, lender_info in LENDERS.items():
        if lender_info["min_amount"] <= amount <= lender_info["max_amount"]:
            available_lenders.append(lender_name)
            with st.expander(f"📊 {lender_name}"):
                st.write(f"**Rate:** {lender_info['rate']}")
                st.write(f"**Loan Range:** {lender_info['min_amount']} - {lender_info['max_amount']} sats")
                st.write(f"**Status:** Available for your amount")
    
    return available_lenders

def main():
    st.title("Welcome to BitLoan!")
    st.write("A Bitcoin Micro Loan Platform brought to you by the Lightning Network.")

    # Role selection
    role = st.radio("Please select an option to begin:", ["Request Loan", "Approve Loan", "Repay Loan"])

    if role == "Request Loan":
        st.header("Loan Request Dashboard")
        
        # First, show available lenders
        st.subheader("Step 1: Check Available Lenders")
        amount = st.number_input("Enter amount to borrow (in sats):", min_value=0)
        
        if amount:
            available_lenders = display_lender_options(amount)
            
            if not available_lenders:
                st.warning("No lenders available for this amount. Please adjust your amount.")
            else:
                st.success(f"Found {len(available_lenders)} lender(s) available for your amount!")
                
                # Loan request form
                st.subheader("Step 2: Submit Loan Request")
                with st.form("loan_request"):
                    selected_lender = st.selectbox(
                        "Select preferred lender:",
                        available_lenders
                    )
                    submit_button = st.form_submit_button("Request Loan")

                    if submit_button:
                        try:
                            # Create loan request invoice
                            invoice_borrower = client.create_invoice(
                                wallet_key=borrower1_adminkey,
                                amount_sats=amount,
                                memo=f"Borrower's Loan Request for {selected_lender}"
                            )

                            # Add to available loans
                            st.session_state.available_loans.append({
                                'amount': amount,
                                'invoice': invoice_borrower,
                                'time': time.strftime("%H:%M:%S"),
                                'status': 'pending',
                                'borrower': 'Borrower 1',
                                'preferred_lender': selected_lender
                            })

                            st.success(f"Loan Request of {invoice_borrower.amount} sats has been posted!")
                            st.info(f"Waiting for {selected_lender} to approve...")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

    elif role == "Approve Loan":
        st.header("Loan Approval Dashboard")
        
        # Lender selection
        selected_lender = st.selectbox(
            "Select your lender account:",
            ["Lender 1", "Lender 2", "Lender 3"]
        )
        
        if st.session_state.available_loans:
            st.write("Pending Loan Requests:")
            
            # Group loans by amount
            loans_by_amount = {}
            for loan in st.session_state.available_loans:
                if loan['amount'] not in loans_by_amount:
                    loans_by_amount[loan['amount']] = []
                loans_by_amount[loan['amount']].append(loan)
            
            # Display loans grouped by amount
            for amount, loans in loans_by_amount.items():
                with st.expander(f"Loans of {amount} sats"):
                    for i, loan in enumerate(loans, 1):
                        st.write(f"Request {i}:")
                        st.write(f"- Requested at: {loan['time']}")
                        st.write(f"- Status: {loan['status']}")
                        st.write(f"- Borrower: {loan['borrower']}")
                        st.write(f"- Preferred Lender: {loan['preferred_lender']}")
                        
                        if loan['status'] == 'pending' and loan['preferred_lender'] == selected_lender:
                            if st.button(f"Approve Loan {i}", key=f"approve_{amount}_{i}"):
                                try:
                                    # Process payment using selected lender's key
                                    lender_key = get_lender_key(selected_lender)
                                    client.pay_invoice(
                                        wallet_adminkey=lender_key,
                                        invoice=loan['invoice'].payment_request
                                    )
                                    
                                    # Update loan status
                                    loan['status'] = 'approved'
                                    loan['approved_time'] = time.strftime("%H:%M:%S")
                                    loan['lender'] = selected_lender
                                    loan['loan_id'] = f"{selected_lender}_{loan['amount']}_{time.strftime('%Y%m%d%H%M%S')}"
                                    
                                    # Initialize loan balance
                                    st.session_state.loan_balances[loan['loan_id']] = loan['amount']
                                    
                                    # Move to approved loans
                                    st.session_state.approved_loans.append(loan)
                                    st.session_state.available_loans.remove(loan)
                                    
                                    st.success(f"Successfully approved loan of {loan['amount']} sats!")
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")
        else:
            st.info("No pending loan requests at the moment")

    else:
        st.header("Loan Repayment Dashboard")
        
        # First, show approved loans grouped by lender
        if st.session_state.approved_loans:
            st.subheader("Your Approved Loans")
            
            # Group loans by lender
            loans_by_lender = {}
            for loan in st.session_state.approved_loans:
                if loan['lender'] not in loans_by_lender:
                    loans_by_lender[loan['lender']] = []
                loans_by_lender[loan['lender']].append(loan)
            
            # Display loans for each lender
            for lender, loans in loans_by_lender.items():
                with st.expander(f"📊 {lender}'s Loans"):
                    for i, loan in enumerate(loans, 1):
                        remaining_balance = get_loan_balance(loan['loan_id'])
                        st.write(f"Loan {i}:")
                        st.write(f"- Original Amount: {loan['amount']} sats")
                        st.write(f"- Remaining Balance: {remaining_balance} sats")
                        st.write(f"- Approved at: {loan['approved_time']}")
                        st.write(f"- Rate: {LENDERS[lender]['rate']}")
            
            # Repayment form
            st.subheader("Submit Repayment")
            
            # Get loans for selected lender
            selected_lender = st.selectbox(
                "Select lender to repay:",
                list(loans_by_lender.keys()),
                key="lender_select"
            )
            
            lender_loans = loans_by_lender[selected_lender]
            
            # Only show loans with remaining balance
            active_loans = [loan for loan in lender_loans if get_loan_balance(loan['loan_id']) > 0]
            
            if not active_loans:
                st.info("No active loans to repay for this lender")
            else:
                selected_loan = st.selectbox(
                    "Select loan to repay:",
                    active_loans,
                    format_func=lambda x: f"Loan of {x['amount']} sats (Remaining: {get_loan_balance(x['loan_id'])} sats)",
                    key="loan_select"
                )
                
                remaining_balance = get_loan_balance(selected_loan['loan_id'])
                amount = st.number_input(
                    "Amount to repay (in sats):",
                    min_value=1,
                    max_value=remaining_balance,
                    value=min(remaining_balance, 1000),
                    key="repayment_amount"
                )
                
                if st.button("Submit Repayment", key="repay_button"):
                    try:
                        # Create repayment invoice
                        invoice_lender = client.create_invoice(
                            wallet_key=get_lender_key(selected_lender),
                            amount_sats=amount,
                            memo=f"Borrower's Loan Repayment to {selected_lender}"
                        )

                        # Process payment
                        client.pay_invoice(
                            wallet_adminkey=borrower1_adminkey,
                            invoice=invoice_lender.payment_request
                        )
                        
                        # Update loan balance
                        update_loan_balance(selected_loan['loan_id'], amount)
                        new_balance = get_loan_balance(selected_loan['loan_id'])
                        
                        st.success(f"Successfully repaid {amount} sats to {selected_lender}!")
                        st.info(f"Remaining balance: {new_balance} sats")
                        
                        # If loan is fully paid, update its status
                        if new_balance == 0:
                            selected_loan['status'] = 'paid'
                            st.success("Loan fully paid!")
                            
                        # Force refresh of the page
                        st.rerun()
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
            st.info("No approved loans to repay at the moment")

    # Display loan history section
    st.header("Loan History")
    
    if st.session_state.approved_loans:
        st.subheader("Approved Loans")
        for loan in st.session_state.approved_loans:
            remaining_balance = get_loan_balance(loan['loan_id'])
            status = "Fully Paid" if remaining_balance == 0 else f"Remaining: {remaining_balance} sats"
            st.write(f"Amount: {loan['amount']} sats (Approved by {loan['lender']} at {loan['approved_time']}) - {status}")
    
    if st.session_state.available_loans:
        st.subheader("Pending Loans")
        for loan in st.session_state.available_loans:
            st.write(f"Amount: {loan['amount']} sats (Requested at {loan['time']})")
    
    if not st.session_state.approved_loans and not st.session_state.available_loans:
        st.info("No loan history available")

if __name__ == "__main__":
    main() 