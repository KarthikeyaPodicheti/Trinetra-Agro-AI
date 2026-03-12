#!/bin/bash

echo "🔱 Welcome to Trinetra Agro AI Setup 🔱"
echo "Vision Beyond the Fields - The All-Seeing Farming Intelligence"
echo "================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "trinetra-env" ]; then
    python3 -m venv trinetra-env
    echo "✅ Virtual environment created: trinetra-env"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source trinetra-env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ All packages installed successfully!"
else
    echo "❌ requirements.txt not found. Creating basic installation..."
    pip install streamlit pandas numpy matplotlib seaborn opencv-python pillow scikit-learn tensorflow flask
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data/{raw,processed,feedback}
mkdir -p models/trained_models
mkdir -p logs
mkdir -p app/static/{css,js,images}
echo "✅ Directories created"

# Download sample datasets (if not exists)
echo "📊 Setting up sample data..."
mkdir -p data/sample_datasets

# Create a simple dataset info file
cat > data/sample_datasets/README.md << EOL
# Sample Datasets for Trinetra Agro AI

## Disease Detection Dataset
- Download PlantVillage dataset from: https://github.com/spMohanty/PlantVillage-Dataset
- Extract to: data/sample_datasets/plant_disease/

## Market Price Data
- Sample market data will be generated automatically
- Real data can be obtained from: https://data.gov.in/catalog/agricultural-marketing

## Weather Data
- Register at OpenWeatherMap: https://openweathermap.org/api
- Add your API key to .env file

## Soil Data
- Sample soil data included in the knowledge base
- Real soil test data can be integrated via API
EOL

# Create environment file
echo "🔐 Creating environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOL
# Trinetra Agro AI Environment Configuration

# OpenAI API (for advanced chat features)
OPENAI_API_KEY=your_openai_api_key_here

# Weather API
WEATHER_API_KEY=your_weather_api_key_here

# Database
DATABASE_URL=sqlite:///trinetra.db

# Environment
ENVIRONMENT=development

# Application settings
DEBUG=True
SECRET_KEY=your_secret_key_here
EOL
    echo "✅ Environment file created (.env)"
    echo "📝 Please edit .env file and add your API keys"
else
    echo "✅ Environment file already exists"
fi

# Create initial database (placeholder)
echo "🗄️ Initializing database..."
python3 -c "
import sqlite3
import os

db_path = 'trinetra.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create farmers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    land_size REAL,
    soil_type TEXT,
    budget REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create conversations table  
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    message TEXT,
    response TEXT,
    intent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
)
''')

# Create feedback table
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    feature TEXT,
    rating INTEGER,
    comments TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers (id)
)
''')

conn.commit()
conn.close()
print('✅ Database initialized successfully!')
"

# Download NLTK data (if needed)
echo "📚 Downloading language processing data..."
python3 -c "
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    print('✅ NLTK data downloaded')
except ImportError:
    print('⚠️ NLTK not installed - skipping download')
"

# Set up Git hooks (if git is available)
if command -v git &> /dev/null; then
    echo "📋 Setting up Git hooks..."
    if [ -d ".git" ]; then
        # Create pre-commit hook for code formatting
        mkdir -p .git/hooks
        cat > .git/hooks/pre-commit << 'EOL'
#!/bin/bash
# Auto-format Python code before commit
if command -v black &> /dev/null; then
    echo "Running black formatter..."
    black app/ --exclude="/(migrations|venv|env|build|dist)/"
fi
EOL
        chmod +x .git/hooks/pre-commit
        echo "✅ Git hooks configured"
    fi
fi

# Create startup script
echo "🚀 Creating startup script..."
cat > start_trinetra.sh << 'EOL'
#!/bin/bash
echo "🔱 Starting Trinetra Agro AI..."

# Activate virtual environment
source trinetra-env/bin/activate

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/app"

# Start the application
echo "🌐 Starting Streamlit application..."
echo "🔗 Open your browser and go to: http://localhost:8501"
echo "⏹️ Press Ctrl+C to stop the application"

streamlit run app/main.py --server.port=8501 --server.address=localhost
EOL

chmod +x start_trinetra.sh

# Create development script
cat > dev_trinetra.sh << 'EOL'
#!/bin/bash
echo "🛠️ Starting Trinetra Agro AI in Development Mode..."

# Activate virtual environment
source trinetra-env/bin/activate

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/app"
export ENVIRONMENT=development

# Start with hot reload
streamlit run app/main.py --server.port=8501 --server.address=localhost --server.runOnSave=true
EOL

chmod +x dev_trinetra.sh

echo ""
echo "🎉 Setup Complete! 🎉"
echo "================================================="
echo ""
echo "🚀 Next Steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run: ./start_trinetra.sh (for production)"
echo "3. Run: ./dev_trinetra.sh (for development with hot reload)"
echo ""
echo "📝 Additional Setup:"
echo "• Download disease detection dataset"
echo "• Configure weather API key"
echo "• Set up market data sources"
echo ""
echo "📖 Documentation: See ROADMAP.md for detailed development guide"
echo "🐛 Issues: Report issues on GitHub"
echo ""
echo "🔱 Happy Farming with AI! 🔱"