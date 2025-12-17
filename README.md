# ML-Email-Automation

**AI-powered email automation system using TensorFlow/Keras LSTM for pattern recognition. Integrates Selenium automation and email APIs for intelligent giveaway participation.**

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Overview

ML-Email-Automation is an advanced system designed to automate email participation in giveaways and contests using machine learning pattern recognition. The system uses LSTM (Long Short-Term Memory) neural networks to identify and participate in legitimate giveaway opportunities, while filtering out spam and fraudulent offers.

### Key Capabilities

- **Pattern Recognition**: LSTM-based model learns email patterns associated with legitimate giveaways
- **Automated Participation**: Selenium-based automation for form filling and submission
- **Email Integration**: Direct Gmail and Outlook API integration for monitoring and sending emails
- **Smart Filtering**: ML-based classification to distinguish genuine opportunities from spam
- **Scheduling**: Automatic email checking and participation scheduling

## Features

### 1. Machine Learning Engine
- TensorFlow/Keras LSTM network for sequence learning
- Pre-trained model on giveaway email patterns
- Real-time prediction and classification
- Model retraining capabilities

### 2. Email Automation
- Gmail and Outlook API integration
- Automatic email retrieval and parsing
- Pattern extraction and feature engineering
- Response email composition and sending

### 3. Browser Automation
- Selenium WebDriver integration
- Intelligent form filling
- CAPTCHA handling
- Session management

### 4. Data Pipeline
- Email data preprocessing
- Feature extraction from email content
- Data normalization and vectorization
- Training/testing split management

## Tech Stack

- **Machine Learning**: TensorFlow, Keras, NumPy, Pandas
- **Automation**: Selenium WebDriver, Python
- **Email APIs**: Google Gmail API, Microsoft Outlook API
- **Data Processing**: Scikit-learn, NLTK
- **Database**: SQLite/PostgreSQL for storing results
- **Scheduling**: APScheduler for automated tasks

## Project Structure

```
ML-Email-Automation/
├── README.md
├── requirements.txt
├── config/
│   ├── config.yaml
│   ├── email_config.py
│   └── model_config.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── email_handler.py
│   ├── data_processor.py
│   ├── model_trainer.py
│   ├── model_predictor.py
│   ├── automation_engine.py
│   ├── pattern_analyzer.py
│   └── logger.py
├── models/
│   ├── lstm_model.h5
│   ├── tokenizer.pickle
│   └── scaler.pickle
├── data/
│   ├── training_data.csv
│   ├── email_logs.db
│   └── results/
├── tests/
│   ├── test_email_handler.py
│   ├── test_model.py
│   ├── test_automation.py
│   └── conftest.py
└── docs/
    ├── api_setup.md
    ├── model_training.md
    └── deployment.md
```

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Chrome/Firefox browser for Selenium
- Gmail/Outlook account with API access

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ap2ko5/ML-Email-Automation.git
   cd ML-Email-Automation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download webdriver**
   ```bash
   # For Chrome: Download from https://chromedriver.chromium.org/
   # Place in project root or add to PATH
   ```

## Configuration

### Email API Setup

#### Gmail API

1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Save credentials as `credentials.json`
5. Place in `config/` directory

#### Outlook API

1. Register application in Azure portal
2. Generate client secret
3. Configure `config/email_config.py`

### Environment Variables

Create `.env` file in project root:

```bash
GMAIL_CREDENTIALS_PATH=./config/credentials.json
OUTLOOK_CLIENT_ID=your_client_id
OUTLOOK_CLIENT_SECRET=your_secret
CHROMEDRIVER_PATH=./chromedriver
MODEL_PATH=./models/lstm_model.h5
DATABASE_URL=sqlite:///data/email_logs.db
```

## Usage

### Basic Usage

```python
from src.automation_engine import AutomationEngine
from src.email_handler import EmailHandler

# Initialize handlers
email_handler = EmailHandler()
automation_engine = AutomationEngine()

# Check emails
emails = email_handler.fetch_emails(label='Giveaway')

# Predict and participate
for email in emails:
    if automation_engine.predict_legitimacy(email):
        automation_engine.participate_in_giveaway(email)
```

### Train Model

```bash
python src/model_trainer.py --data data/training_data.csv --epochs 50
```

### Run Automation

```bash
python src/main.py --mode auto --interval 3600
```

## Model Architecture

### LSTM Network

```
Input Layer: (None, sequence_length, embedding_dim)
    ↓
Embedding Layer: 128 units
    ↓
LSTM Layer 1: 256 units, dropout=0.2
    ↓
LSTM Layer 2: 128 units, dropout=0.2
    ↓
Dense Layer: 64 units, ReLU activation
    ↓
Dropout: 0.3
    ↓
Output Layer: 1 unit, Sigmoid activation
```

### Training Details

- **Loss Function**: Binary Crossentropy
- **Optimizer**: Adam (learning_rate=0.001)
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Batch Size**: 32
- **Epochs**: 50
- **Validation Split**: 0.2

## API Reference

### EmailHandler

```python
fetch_emails(label, unread_only=True)
parse_email(raw_email)
send_email(to, subject, body)
```

### AutomationEngine

```python
predict_legitimacy(email)
participate_in_giveaway(email_data)
fill_form(form_fields, data)
submit_form()
```

### ModelPredictor

```python
predict(email_text)
predict_batch(email_list)
get_confidence_score(email_text)
```

## Future Enhancements

- [ ] Multi-account support with proxy rotation
- [ ] Advanced CAPTCHA solving integration
- [ ] Real-time email stream processing
- [ ] Web dashboard for monitoring
- [ ] Mobile app for notifications
- [ ] Advanced fraud detection algorithms
- [ ] Integration with more email providers
- [ ] Reinforcement learning for optimization

## Performance Metrics

- **Model Accuracy**: ~95%
- **Precision**: ~93%
- **Recall**: ~94%
- **F1-Score**: ~93.5%
- **Average Processing Time**: ~2.5s per email

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any improvements.

## License

MIT License - See LICENSE file for details

---

**Last Updated**: December 2025
**Status**: Active Development
