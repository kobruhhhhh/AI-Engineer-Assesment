# Import the LinkedIn post generator function from your module
from linkedin_post_generator import generate_linkedin_post
import json  # For saving test results to JSON files

# Define test articles with titles and summaries that represent different healthcare AI scenarios
test_articles = [
    {
        "title": "AI-Powered Diagnostic Tool Shows Promise in Early Detection of Alzheimer's",
        "summary": "Researchers have developed a new AI algorithm that can detect early signs of Alzheimer's disease from standard MRI scans with 94% accuracy, potentially allowing for earlier intervention and treatment planning. The system analyzes subtle patterns that human radiologists might miss and provides explanatory outputs for clinician review. Clinical trials are expected to begin next year, with researchers emphasizing that the tool is designed to augment, not replace, physician expertise."
    },
    {
        "title": "Study Finds AI Chatbots Reducing Administrative Burden for Primary Care Physicians",
        "summary": "A recent study published in JAMA Network Open showed that implementing AI-powered chatbots for routine patient inquiries reduced physician documentation time by 37%. The six-month trial involved 120 primary care practices and demonstrated that physicians using the AI tools reported higher job satisfaction and spent an average of 12 more minutes per day in direct patient care. Privacy concerns and patient acceptance were noted as ongoing challenges, with older patients expressing more reservations about the technology."
    },
    {
        "title": "Ethical Concerns Raised Over Black-Box AI in Clinical Decision Support Systems",
        "summary": "Healthcare ethicists are raising alarms about the increasing use of 'black-box' AI algorithms in clinical decision support systems. A position paper published by the American College of Physicians notes that many AI tools being deployed lack transparency in their decision-making processes, making it difficult for physicians to understand, validate, or override algorithmic recommendations. The paper calls for new regulatory standards requiring explainability in healthcare AI and emphasizes the importance of maintaining physician autonomy in clinical decisions."
    }
]

# Execute test cases for each article
for i, article in enumerate(test_articles):  # i = index, article = test case data
    # Print test case header with number and title
    print(f"\n==== Test Case {i + 1}: {article['title']} ====\n")

    try:
        # Generate LinkedIn post using the imported function
        result = generate_linkedin_post(article)

        # Print the generated post and metrics
        print("LinkedIn Post:")
        print(result["linkedin_post"])  # The main generated content
        print(f"\nWord Count: {result['word_count']}")  # Length metric
        print(f"Perspective Alignment: {result['perspective_alignment']}/100")  # Quality score

        # List which physician perspectives were incorporated
        print("\nPerspectives Used:")
        for perspective in result["perspectives_used"]:
            print(f"- {perspective}")

        # Print explanation of the confidence score
        print(f"\nConfidence Explanation: {result['confidence_explanation']}")

        # Save the complete results to a JSON file for later analysis
        with open(f"test_case_{i + 1}_output.json", "w") as f:
            json.dump(result, f, indent=2)  # Pretty-print JSON with 2-space indentation

    except Exception as e:
        # Handle any errors that occur during processing
        print(f"Error processing test case {i + 1}: {str(e)}")

    # Print separator between test cases for better readability
    print("\n" + "=" * 50)