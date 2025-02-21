import subprocess
import sys
import os

def install_dependencies():
    """Install Python dependencies from requirements.txt"""
    print("Installing Python dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')

def download_spacy_models():
    """Download required SpaCy models"""
    print("Downloading SpaCy models...")
    # English model
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    # Multi-language model for Romanian support
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "xx_ent_wiki_sm"])

def create_directories():
    """Create necessary directories"""
    print("Creating project directories...")
    directories = [
        'src/uploads',
        'src/static/visualizations',
        'src/static/js',
        'src/static/css',
        'src/templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main setup function"""
    try:
        print("Starting setup...")
        
        # Create directories
        create_directories()
        
        # Install dependencies
        install_dependencies()
        
        # Download required data
        download_nltk_data()
        download_spacy_models()
        
        print("\nSetup completed successfully!")
        print("\nTo start the application, run:")
        print("python run.py")
        
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
