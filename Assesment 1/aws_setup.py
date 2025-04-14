# Import the boto3 library for interacting with AWS services
import boto3  

# Import load_dotenv to read environment variables from a .env file  
from dotenv import load_dotenv  

# Import the os module to interact with the operating system (e.g., environment variables)  
import os  

# Load environment variables from the .env file in the current directory  
load_dotenv()  # Reads key-value pairs from .env and makes them available in os.getenv()  

# Define a function to test the AWS Bedrock connection  
def test_connection():  
    try:  
        # Initialize the AWS Bedrock client using credentials from environment variables  
        bedrock = boto3.client(  
            'bedrock',  # Specifies the AWS service (Bedrock)  
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),  # Retrieves AWS access key from .env  
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),  # Retrieves AWS secret key from .env  
            region_name=os.getenv('AWS_DEFAULT_REGION')  # Retrieves AWS region (e.g., 'us-west-2') from .env  
        )  

    # Handle exceptions (e.g., invalid credentials, network issues)  
    except Exception as e:  
        # Print an error message if connection fails  
        print(f"Error connecting to AWS Bedrock: {str(e)}")  
        # Return False to indicate failure  
        return False  

# Execute the test_connection() function only if this script is run directly (not imported)  
if __name__ == "__main__":  
    test_connection()  # Calls the connection test function  