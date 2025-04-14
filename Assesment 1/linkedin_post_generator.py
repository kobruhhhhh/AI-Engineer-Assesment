# Import required libraries
import json  # For working with JSON data
import boto3  # AWS SDK for interacting with AWS services
import requests  # For making HTTP requests to fetch web content
from bs4 import BeautifulSoup  # For parsing and extracting HTML content
import re  # Regular expressions for text processing
from urllib.parse import urlparse  # For URL parsing and validation

# Initialize AWS Bedrock client for generative AI capabilities
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",  # Specifies the Bedrock runtime service
    region_name="ap-south-1"  # AWS region where the Titan model is available
)

# Core physician perspectives on healthcare AI that should be reflected in generated content
PHYSICIAN_PERSPECTIVES = [
    "AI should augment healthcare professionals, not replace them",
    "Patient care quality and safety must remain the top priority when implementing AI",
    "AI tools should reduce administrative burden, allowing more time with patients",
    "Healthcare AI must be explainable and transparent in its decision-making",
    "AI implementation should address healthcare disparities, not amplify them",
    "Data privacy and security are non-negotiable in healthcare AI applications",
    "Clinicians should be involved in developing and validating healthcare AI tools"
]


def extract_article_content(url):
    """Extract the title and main content from an article URL"""
    try:
        # Set headers to mimic a browser request
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Fetch the webpage content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title from HTML <title> tag
        title = soup.find('title').text.strip()

        # Extract main content by collecting text from paragraphs
        article_text = ""
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text().strip()
            # Filter out short paragraphs (likely navigation or ads)
            if len(text) > 100:
                article_text += text + "\n\n"

        return {
            "title": title,
            "content": article_text[:5000]  # Limit content size for model input
        }
    except Exception as e:
        return {
            "title": "Error extracting content",
            "content": f"Failed to extract content from {url}: {str(e)}"
        }


def create_prompt(article_info, perspectives=PHYSICIAN_PERSPECTIVES):
    """Create a structured prompt for the AI model"""

    # Initialize variables for article content
    article_text = ""
    article_title = ""

    # Handle different input types (URL string, text, or dictionary)
    if isinstance(article_info, str):
        # Check if input is a valid URL
        parsed_url = urlparse(article_info)
        if parsed_url.scheme and parsed_url.netloc:
            extracted = extract_article_content(article_info)
            article_title = extracted["title"]
            article_text = extracted["content"]
        else:
            # Treat as plain text input
            article_text = article_info
    elif isinstance(article_info, dict):
        # Extract from dictionary structure
        article_title = article_info.get("title", "")
        article_text = article_info.get("content", article_info.get("summary", ""))

    # Construct detailed prompt for the AI model
    prompt = f"""
Write a LinkedIn post (200-250 words) as a physician reflecting on this healthcare AI article:

ARTICLE TITLE: {article_title}

ARTICLE CONTENT/SUMMARY:
{article_text}

Include these physician perspectives on AI in healthcare:
{chr(10).join(f"- {perspective}" for perspective in perspectives)}

Format your response as a JSON object with:
- "linkedin_post": The complete post text
- "word_count": Total word count
- "perspective_alignment": A score from 1-100 showing alignment with the given perspectives
- "perspectives_used": List of perspectives reflected in the post
- "confidence_explanation": Brief explanation of the confidence score

Make the post insightful, professional, and 200-250 words long.
"""
    return prompt


def generate_linkedin_post(article_info):
    """Generate a LinkedIn post using AWS Bedrock's Titan model"""

    # Create the AI prompt
    prompt = create_prompt(article_info)

    try:
        # Call AWS Bedrock's Titan model
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-text-express-v1",  # Specify the Titan model
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1500,  # Limit response length
                    "temperature": 0.7,  # Controls randomness (0-1)
                    "topP": 0.9  # Controls diversity of responses
                }
            })
        )

        # Parse the model response
        response_body = json.loads(response.get("body").read().decode())
        raw_content = response_body.get("results", [{}])[0].get("outputText", "")

        # Clean up the response content
        content = re.sub(r'```[\w-]*\n|\n```', '', raw_content)  # Remove code blocks

        # Try to extract JSON from response if present
        try:
            matches = re.findall(r'\{.+\}', content, re.DOTALL)
            if matches:
                for match in matches:
                    try:
                        json_data = json.loads(match)
                        if "linkedin_post" in json_data:
                            content = json_data["linkedin_post"]
                            break
                        elif "rows" in json_data and len(json_data["rows"]) > 0:
                            if "linkedin_post" in json_data["rows"][0]:
                                content = json_data["rows"][0]["linkedin_post"]
                                break
                    except:
                        continue
        except:
            pass

        # Fallback extraction if JSON parsing fails
        if content.strip().startswith('{') and '"linkedin_post"' in content:
            match = re.search(r'"linkedin_post"\s*:\s*"([^"]+)"', content)
            if match:
                content = match.group(1)

        # Final content cleanup
        content = content.strip()

        # Analyze which physician perspectives were included
        perspectives_used = []
        for perspective in PHYSICIAN_PERSPECTIVES:
            if perspective.lower() in content.lower() or any(
                    keyword.lower() in content.lower() for keyword in perspective.split()):
                perspectives_used.append(perspective)

        # Calculate alignment score (percentage of perspectives included)
        perspective_alignment = min(100, int((len(perspectives_used) / len(PHYSICIAN_PERSPECTIVES)) * 100))

        return {
            "linkedin_post": content,
            "word_count": len(content.split()),
            "perspective_alignment": perspective_alignment,
            "perspectives_used": perspectives_used,
            "confidence_explanation": f"Generated using Titan Text G1 - Express. Contains {len(perspectives_used)} of {len(PHYSICIAN_PERSPECTIVES)} perspectives."
        }

    except Exception as e:
        return {
            "linkedin_post": f"Error generating post: {str(e)}",
            "word_count": 0,
            "perspective_alignment": 0,
            "perspectives_used": [],
            "confidence_explanation": f"Error: {str(e)}"
        }


def handle_request(event, context=None):
    """AWS Lambda handler function for API integration"""
    try:
        # Parse incoming request
        body = json.loads(event.get('body', '{}'))
        article_info = body.get('article_info', {})

        if not article_info:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing article_info in request body'})
            }

        # Generate and return the LinkedIn post
        result = generate_linkedin_post(article_info)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# Command Line Interface
if __name__ == "__main__":
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate LinkedIn posts about healthcare AI articles')
    parser.add_argument('--url', help='URL of the healthcare AI article')
    parser.add_argument('--title', help='Title of the article')
    parser.add_argument('--summary', help='Summary of the article')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    # Process input based on provided arguments
    if args.url:
        article_info = args.url
    elif args.title and args.summary:
        article_info = {
            "title": args.title,
            "summary": args.summary
        }
    elif args.summary:
        article_info = {
            "summary": args.summary
        }
    else:
        print("Error: Please provide either a URL or article summary")
        parser.print_help()
        exit(1)

    # Generate and display results
    try:
        result = generate_linkedin_post(article_info)

        # Print formatted output
        print("\n=== Generated LinkedIn Post ===\n")
        print(result["linkedin_post"])
        print(f"\nWord Count: {result['word_count']}")
        print(f"Perspective Alignment: {result['perspective_alignment']}/100")
        print("\nPerspectives Used:")
        for perspective in result["perspectives_used"]:
            print(f"- {perspective}")
        print(f"\nConfidence Explanation: {result['confidence_explanation']}")

        # Save to file if output path specified
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nFull results saved to {args.output}")

    except Exception as e:
        print(f"Error generating LinkedIn post: {str(e)}")