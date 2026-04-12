from wallet.manager import WalletManager

def simulate():
    print("🚀 Starting Wallet Import Simulation...")
    
    # Define o caminho para o arquivo que você mandou para o Jeiel
    path = "my-wallet.json" 
    
    try:
        # Tenta importar a carteira usando o seu código
        wallet = WalletManager.import_from_json(path)
        
        print(f"✅ Success! Wallet imported.")
        print(f"🔑 Public Key (Address): {wallet.pubkey()}")
        
        print("\n--- Verification ---")
        print("Compare the address above with your terminal command 'solana address'.")
        print("If they match, your code is 100% working!")

    except Exception as e:
        print(f"❌ Error during simulation: {e}")

if __name__ == "__main__":
    simulate()