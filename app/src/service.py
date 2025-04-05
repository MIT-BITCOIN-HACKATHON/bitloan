#
#   Written by Pavel Kononov from LightningBounties.com
#   For MIT Bitcoin Hackathon 2025
#
#   Happy hacking!
#

import requests

from models import Account, Wallet, WalletInfo, Invoice


class LNbits:
    """
    The class provides an example of basic operations with LNbits network.
    For other operations, refer to LNbits API reference: 
        https://demo.lnbits.com/docs
    """

    def __init__(self, url_base: str, use_https: bool = False):
        self._URL_BASE = url_base
        protocol = "https" if use_https else "http"
        self._API_V1_URL = f"{protocol}://{self._URL_BASE}/api/v1"

        self._ACCOUNTS_RESOURCE = f"{self._API_V1_URL}/account"
        self._WALLETS_RESOURCE = f"{self._API_V1_URL}/wallet"
        self._PAYMENTS_RESOURCE = f"{self._API_V1_URL}/payments"

    def create_account(self, name: str) -> Account:
        """
        Creates an LNbits account.

        Args:
            - name (str): the name of the account to be created

        Returns:
            - an Account object of the newly created account

        Raises:
            - an Exception if the operation did not succeed. 
                Check API reference & response body for details
        """

        # Making the request
        response = requests.post(
            url=self._ACCOUNTS_RESOURCE,
            json={
                "name": name
            }
        )

        # Checking for errors
        if response.status_code != 200:
            raise Exception(
                f"Couldn't create an account.\n"
                f"Response status code: {response.status_code}\n"
                f"Response body: {response.json()}"
            )

        # Converting a json dict into a model
        return Account(**response.json())
    
    def create_wallet(self, account_api_key: str, name: str) -> Wallet:
        """
        Creates an LNbits wallet.

        Args:
            - account_api_key (str): an API key of the account associated with the wallet
            - name (str): the name of the wallet to be created

        Returns:
            - a Wallet object of the newly created wallet

        Raises:
            - an Exception if the operation did not succeed. 
                Check API reference & response body for details
        """

        # Making the request
        response = requests.post(
            url=self._WALLETS_RESOURCE,
            headers=self._get_header(account_api_key),
            json={
                "name": name
            }
        )

        # Checking for errors
        if response.status_code != 200:
            raise Exception(
                f"Couldn't create a wallet.\n"
                f"Response status code: {response.status_code}\n"
                f"Response body: {response.json()}"
            )

        # Converting a json dict into a model
        return Wallet(**response.json())
    
    def get_wallet(self, wallet_key: str) -> WalletInfo | None:
        """
        Fetches a wallet by its inkey or adminkey.

        Args:
            - wallet_key (str): the wallet's inkey or adminkey

        Returns:
            - a Wallet object
            - None if wallet does not exist

        Raises:
            - an Exception if the operation did not succeed. 
                Check API reference & response body for details
        """

        # Making the request
        response = requests.get(
            url=self._WALLETS_RESOURCE,
            headers=self._get_header(wallet_key)
        )

        # Wallet not found
        if response.status_code == 404: 
            return None
        
        # Checking for errors
        if response.status_code != 200:
            raise Exception(
                f"Couldn't fetch the wallet.\n"
                f"Response status code: {response.status_code}\n"
                f"Response body: {response.content}"
            )
        
        # Converting a json dict into a model
        return WalletInfo(**response.json())
    
    def create_invoice(self, wallet_key: str, amount_sats: int, memo: str = "") -> Invoice:
        """
        Creates an invoice to be paid by another wallet.

        Args:
            - wallet_key (str): the wallet's inkey or adminkey
            - amount_sats (int): the amount in sats to be paid
            - memo (str, default ""): an arbitrary string to distinguish the payment among other

        Returns: 
            - an Invoice object

        Raises:
            - an Exception if the operation did not succeed. 
                Check API reference & response body for details
        """

        # Making the request
        response = requests.post(
            url=self._PAYMENTS_RESOURCE,
            headers=self._get_header(wallet_key),
            json={
                "out": False,
                "amount": amount_sats,
                "memo": memo
            }
        )

        # Checking for errors
        if response.status_code != 201:
            raise Exception(
                f"Couldn't create an invoice.\n"
                f"Response status code: {response.status_code}\n"
                f"Response body: {response.content}"
            )
        
        # Convert response to dict and add payment_request field
        response_dict = response.json()
        response_dict["payment_request"] = response_dict["bolt11"]
        # Convert amount from millisats to sats
        response_dict["amount"] = response_dict["amount"] // 1000

        # Converting a json dict into a model
        return Invoice(**response_dict)
    
    def pay_invoice(self, wallet_adminkey: str, invoice: str) -> None:
        """
        Pays an invoice.

        Args:
            - wallet_adminkey (str): the wallet's adminkey (inkey will NOT work)
            - invoice (str): the invoice to be paid

        Returns: 
            - an Invoice object

        Raises:
            - an Exception if the operation did not succeed. 
                Check API reference & response body for details
        """

        # Making the request
        response = requests.post(
            url=self._PAYMENTS_RESOURCE,
            headers=self._get_header(wallet_adminkey),
            json={
                "out": True,
                "bolt11": invoice
            }
        )

        # Checking for errors
        if response.status_code >= 400:
            raise Exception(
                f"Couldn't create an invoice.\n"
                f"Response status code: {response.status_code}\n"
                f"Response body: {response.content}"
            )

        # Convert response to dict and add payment_request field
        response_dict = response.json()
        response_dict["payment_request"] = response_dict["bolt11"]

        # Converting a json dict into a model
        return Invoice(**response_dict)

    def _get_header(self, auth_key: str) -> dict[str, str]:
        """
        Converts LNbits auth key into a header 
        that can be used for requests to LNbits API.

        Args:
            - auth_key (str): an auth key to be used in the header

        Returns:
            - a dict that contains the API key header with the auth_key in its value
        """
        return {
            "X-Api-Key": auth_key
        }
    