from config import configure_model, configure_api_key

def configure():
    """Simple CLI to configure embedding model and API key"""
    print("🔧 Configuration Setup")
    print("=" * 40)
    
    # Get model choice
    print("\nSelect embedding model:")
    print("1. local (free, runs locally)")
    print("2. gemini (requires API key)")
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        model = "local"
        print("✅ Set to local model")
        configure_model(model)
        print("✅ Configuration saved!")
        
    elif choice == "2":
        model = "gemini"
        api_key = input("Enter your Gemini API key: ").strip()
        
        if not api_key:
            print("❌ API key cannot be empty")
            return
        
        configure_model(model)
        configure_api_key(api_key)
        print("✅ Configuration saved!")
        
    else:
        print("❌ Invalid choice")
        return

if __name__ == "__main__":
    configure()
