# Import required libraries
import streamlit as st  # For building the web interface
import json  # For handling JSON data
from linkedin_post_generator import generate_linkedin_post  # Import the post generator function

# Configure the Streamlit page settings
st.set_page_config(
    page_title="LinkedIn Healthcare AI Post Generator",  # Browser tab title
    layout="wide"  # Optional: Use wider layout
)

# Set up the main page header and description
st.title("LinkedIn Healthcare AI Post Generator")  # Main title
st.markdown(
    "Generate professional LinkedIn posts from a physician's perspective on healthcare AI topics.")  # Description

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Article URL", "Article Summary"])  # Two input method options

# First tab: URL input method
with tab1:
    # URL input field
    url = st.text_input(
        "Enter article URL:",  # Field label
        placeholder="https://example.com/healthcare-ai-article"  # Example text
    )

    # Submit button for URL method
    url_submit = st.button("Generate Post from URL")

    # Handle URL submission
    if url_submit and url:
        with st.spinner("Generating LinkedIn post..."):  # Show loading spinner
            try:
                # Call the post generator function with the URL
                result = generate_linkedin_post(url)

                # Display success message and results
                st.success("LinkedIn post generated successfully!")

                # Display the generated post in a text area
                st.text_area(
                    "LinkedIn Post",  # Label
                    result["linkedin_post"],  # Generated content
                    height=300  # Display height
                )

                # Show word count metric
                st.metric("Word Count", result["word_count"])

                # Show perspective alignment score
                st.metric("Perspective Alignment", f"{result['perspective_alignment']}/100")

                # List the perspectives used
                st.subheader("Perspectives Used")
                for perspective in result["perspectives_used"]:
                    st.markdown(f"- {perspective}")  # Bullet point format

                # Show confidence explanation
                st.subheader("Confidence Explanation")
                st.write(result["confidence_explanation"])

            except Exception as e:
                # Display error message if generation fails
                st.error(f"Error generating post: {str(e)}")

# Second tab: Summary input method
with tab2:
    # Article title input (optional)
    title = st.text_input(
        "Article Title:",  # Field label
        placeholder="Enter the title of the article"  # Example text
    )

    # Article summary text area
    summary = st.text_area(
        "Article Summary:",  # Field label
        placeholder="Enter a summary of the article...",  # Example text
        height=200  # Input box height
    )

    # Submit button for summary method
    summary_submit = st.button("Generate Post from Summary")

    # Handle summary submission
    if summary_submit and summary:
        with st.spinner("Generating LinkedIn post..."):  # Show loading spinner
            try:
                # Prepare article info dictionary
                article_info = {"title": title, "summary": summary} if title else {"summary": summary}

                # Call the post generator function with the summary
                result = generate_linkedin_post(article_info)

                # Display success message and results (same structure as URL tab)
                st.success("LinkedIn post generated successfully!")
                st.text_area("LinkedIn Post", result["linkedin_post"], height=300)
                st.metric("Word Count", result["word_count"])
                st.metric("Perspective Alignment", f"{result['perspective_alignment']}/100")
                st.subheader("Perspectives Used")
                for perspective in result["perspectives_used"]:
                    st.markdown(f"- {perspective}")
                st.subheader("Confidence Explanation")
                st.write(result["confidence_explanation"])

            except Exception as e:
                # Display error message if generation fails
                st.error(f"Error generating post: {str(e)}")