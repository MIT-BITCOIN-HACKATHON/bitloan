#
#   Written by Pavel Kononov from LightningBounties.com
#   For MIT Bitcoin Hackathon 2025
#
#   Happy hacking!
#

from service import LNbits


def main() -> None:
    try:
        client = LNbits("localhost:5001", use_https=False)

        # account = client.create_account(name="super-jaba")
        # print(f"Account created: {account.name}")

        # wallet1 = client.create_wallet(
        #     account_api_key=account.adminkey,
        #     name="Lender"
        # )
        # print(f"Wallet created: {wallet1.name}")

        # wallet2 = client.create_wallet(
        #     account_api_key=account.adminkey,
        #     name="Borrower"
        # )
        # print(f"Wallet created: {wallet2.name}")

        # Use existing wallet admin keys
        wallet1_adminkey = "a141d91d41f34c1dae0db0689bb46191"
        wallet2_adminkey = "d2adf110d55b4aa1b449c38c7a57d512"

        # Lender creates loan invoice to borrower
        invoice_borrower = client.create_invoice(
            wallet_key=wallet2_adminkey, 
            amount_sats=100, 
            memo="Borrower's Loan Request"
        )
        print(f"Borrower's Loan Request created for {invoice_borrower.amount} sats")

        client.pay_invoice(
            wallet_adminkey=wallet1_adminkey,
            invoice=invoice_borrower.payment_request
        )
        print(f"Borrower's Loan Request paid: {invoice_borrower.amount} sats")

        # Borrower creates repayment invoice to lender
        invoice_lender = client.create_invoice(
            wallet_key=wallet1_adminkey, 
            amount_sats=10, 
            memo="Borrower's Loan Repayment"
        )
        print(f"Borrower's Loan Repayment created for {invoice_lender.amount} sats")

        client.pay_invoice(
            wallet_adminkey=wallet2_adminkey,
            invoice=invoice_lender.payment_request
        )
        print(f"Borrower's Loan Repayment paid: {invoice_lender.amount} sats")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
