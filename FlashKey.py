import os
import time

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountInfo
from stellar_sdk import Server, Keypair

# === Component: Menu ===

def main_menu():
    clear_console()
    while True:
        print("\n=== FlashKey Wallet v3.2 ===")
        print(" 1. XRP")
        print(" 2. XLM")
        print(" 3. Create Public")
        print("-----------------------")
        print(" 4. Get Public Address & Balance")
        print(" 0. Exit")
        
        choice = input(" Enter the menu item number: ").strip()
        
        if choice == "1":
            xrp_menu()
        elif choice == "2":
            xlm_menu()
        elif choice == "3":
            create_public_file()
        elif choice == "4":
            get_public_balance()
        elif choice == "0":
            print("\n Goodbye!")
            time.sleep(3)
            exit()
        elif choice == "cls" or choice == "-":
            clear_console()
        else:
            print("\n Incorrect choice. Please try again.")

def xrp_menu():
    while True:
        print("\n<< XRP:")
        print(" 1. Create a new XRP wallet.")
        print(" 0. Return to the main menu.")
        
        choice = input(" Enter the menu item number: ").strip()
        
        if choice == "1":
            xrp_gen()
        elif choice == "0":
            break
        else:
            print("\n Incorrect choice. Please try again.")

def xlm_menu():
    while True:
        print("\n<< XLM:")
        print(" 1. Create a new XLM wallet.")
        print(" 0. Return to the main menu.")
        
        choice = input(" Enter the menu item number: ").strip()
        
        if choice == "1":
            xlm_gen()
        elif choice == "0":
            break
        else:
            print("\n Incorrect choice. Please try again.")

def license_agreement():
    while True:
        print("\n === License Agreement ===")
        print(" 1. The software is provided 'as is' without any warranties regarding its functionality or safety.")
        print(" 2. The developer does not guarantee that the program will work without interruptions or errors.")
        print(" 3. The developers and contributors of the project are not responsible for any loss or theft of funds.")
        print(" 4. The user is fully responsible for keeping their private keys and assets secure.")
        print(" 5. The user is fully responsible for any actions performed using this program.")
        print(" =========================")
        print(" By using this wallet, you agree to these terms.")
        print(" To proceed, you must accept the license agreement.")
        print(" 1. Accept the terms")
        print(" 2. Decline the terms and exit")

        choice = input(" Enter the menu item number: ").strip()

        if choice == "1":
            main_menu()
        elif choice == "2":
            break
        else:
            print("\n Incorrect choice. Please try again.")

# === Component: Menu ===


# === Component: Wallet function ===

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_public_balance():
    print("\n===============")
         
    xrp_client = JsonRpcClient("https://s1.ripple.com:51234")  
    xlm_server = Server("https://horizon.stellar.org")  

    # Get the absolute path to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    public_addr = os.path.join(script_dir, "public_addr")

    # Function to get the XRP balance
    def get_xrp_balance(public_key):
        try:
            request = AccountInfo(
                account=public_key,
                ledger_index="validated",
                strict=True
            )
            response = xrp_client.request(request)
            balance = response.result["account_data"]["Balance"]
            return str(int(balance) / 1_000_000)  
        except Exception as e:
            return f"- - - : {e}"

    # Function to get the XLM balance
    def get_xlm_balance(public_key):
        try:
            account = xlm_server.accounts().account_id(public_key).call()
            for balance in account['balances']:
                if balance['asset_type'] == 'native':  # XLM
                    return balance['balance']
        except Exception as e:
            return "- - -"

    # Read file "public_addr"
    with open (public_addr, 'r') as wallet_file:
        lines = wallet_file.readlines()

    # Iterating over each line
    for line in lines:
        line = line.strip()
        if line:
            blockchain, public_key = line.split(": ")
            if blockchain == "xrp":
                balance = get_xrp_balance(public_key)
            elif blockchain == "xlm":
                balance = get_xlm_balance(public_key)
            else:
                balance = "Unknown blockchain."
            print(f"{blockchain} | {public_key} | {balance}")

def create_public_file():
    # Get the absolute path to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    f_write = os.path.join(script_dir,'public_addr')
    xrp_path = os.path.join(script_dir,'xrp') 
    xlm_path = os.path.join(script_dir,'xlm') 

    with open(f_write, 'w') as wallet_file:
        
        for filename in os.listdir(xrp_path):
            file_path = os.path.join(xrp_path, filename)
            
            # Check if it is a file, not a folder
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:

                    # Read the first line and write it to a file
                    lines = file.readlines()
                    if lines: 

                        public_key = lines[0].split(": ")[1].strip()
                        wallet_file.write("xrp: " + public_key + '\n')

        
        for filename in os.listdir(xlm_path):
            file_path = os.path.join(xlm_path, filename)
            
            # Check if it is a file, not a folder
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:

                    # Read the first line and write it to a file
                    lines = file.readlines()
                    if lines: 

                        public_key = lines[0].split(": ")[1].strip()
                        wallet_file.write("xlm: " + public_key + '\n')

    # Message about successful file creation
    print("\n===============")
    print("\n File has been successfully created!")
    print(f" File address: {f_write}")

def xlm_gen():
    # Generate a new key pair
    keypair = Keypair.random()

    # Get public and private keys
    public_key = keypair.public_key
    private_key = keypair.secret
    
    filename = wallet_address(public_key)
    
    print("\n===============") 
    print(" Wallet address / Public key:", public_key)
    print(" Private key: [ secret ]")
    
    # Get the absolute path to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "xlm", filename)
    
    with open(file_path, "w") as file:
        file.write(f"Public Key: {public_key}\n")
        file.write(f"Private Key: {private_key}\n")
    
    print(f" Keys have been saved to {file_path}")

def xrp_gen():
    wallet = Wallet.create()

    # Get public and private keys
    address = wallet.classic_address
    public_key = wallet.public_key
    private_key = wallet.seed
    
    print("\n===============")
    print(f" Wallet address: {address}")
    print(" Public key: [ secret ]")
    print(" Private key: [ secret ]")

    filename = wallet_address(address)

    # Get the absolute path to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "xrp", filename)
    
    with open(file_path, "w") as file:
        file.write(f"Address: {address}\n")
        file.write(f"Public Key: {public_key}\n")
        file.write(f"Private Key: {private_key}\n")
    
    print(f" Keys have been saved to {file_path}")

def wallet_address(address):
    if len(address) < 8:
        return address  # If the address is shorter than 8 characters, return it unchanged
    return f"{address[:4]}...{address[-4:]}"

# === Component: Wallet function ===


# === Component: main ===

if __name__ == "__main__":
    license_agreement()

# === Component: main ===
