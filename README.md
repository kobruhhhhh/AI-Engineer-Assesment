# AI-Engineer-Assesment


A Streamlit web application that uses Amazon Bedrock's Titan AI model to generate physician-perspective LinkedIn posts about AI healthcare articles.

## Features

- Generate professional LinkedIn posts from AI healthcare article summaries
- Customize post generation based on specific physician perspectives
- Analyze perspective alignment and word count
- Simple, intuitive user interface

## Setup and Installation

### Prerequisites

- Python 3.8+
- AWS account with access to Amazon Bedrock
- Proper AWS credentials configured

### Step 1: Clone the repository

```bash
git clone https://github.com/kobruhhhhh/AI-Engineer-Assesment.git
cd Assesment 1
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```


### Step 4: Configure AWS credentials

Create a `.env` file in the project root with your AWS credentials:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_aws_region
```


### Step 5: Run the application

```bash
streamlit run app.py
```


## Code Structure

- `app.py`: Main Streamlit application
- `aws_setup.py`: AWS Bedrock client setup
- `linkedin_post_generator.py`: LinkedIn post generation logic
- `run_tests.py`:  Run the Test Cases
