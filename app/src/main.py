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
        wallet1_adminkey = "a141d91d41f34c1dae0db0689bb46191" #Lender
        wallet2_adminkey = "d2adf110d55b4aa1b449c38c7a57d512" #Borrower

        # Ask user role
        while True:
            role = input("Are you Borrower 'B' or Lender 'L'?: ").upper()
            if role in ['B', 'L']:
                break
            print("Please enter 'B' for Borrower or 'L' for Lender")

        if role == 'B':
            # Borrower flow
            while True:
                try:
                    amount = int(input("Please input Sats requested: "))
                    if amount > 0:
                        break
                    print("Please enter a positive number")
                except ValueError:
                    print("Please enter a valid number")

            # Create loan request invoice
            invoice_borrower = client.create_invoice(
                wallet_key=wallet2_adminkey, 
                amount_sats=amount, 
                memo="Borrower's Loan Request"
            )
            # print(f"Loan Request created for {invoice_borrower.amount} sats")
            # print(f"Payment Request: {invoice_borrower.payment_request}")

            client.pay_invoice(
                wallet_adminkey=wallet1_adminkey,
                invoice=invoice_borrower.payment_request
            )
            print(f"Loan Approved for {invoice_borrower.amount} sats")

        else:
            # Lender Repayment flow
            while True:
                try:
                    amount = int(input("Please input Sats to repay: "))
                    if amount > 0:
                        break
                    print("Please enter a positive number")
                except ValueError:
                    print("Please enter a valid number")

            # Create loan invoice
            invoice_lender = client.create_invoice(
                wallet_key=wallet1_adminkey, 
                amount_sats=amount, 
                memo="Borrower's Loan Repayment"
            )
            # print(f"Loan Repayment Amount {invoice_lender.amount} sats")
            # print(f"Payment Request: {invoice_lender.payment_request}")

            client.pay_invoice(
                wallet_adminkey=wallet2_adminkey,
                invoice=invoice_lender.payment_request
            )
            print(f"Successfully repaid {invoice_lender.amount} sats")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
