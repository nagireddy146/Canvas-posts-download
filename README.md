# Canvas Discussion Grading Automation
Automates the extraction and organization of Canvas LMS discussion data to streamline grading workflows and reduce manual effort.

# Overview
This Python-based tool connects to the Canvas LMS using the Canvas REST APIs, fetches student discussion posts and replies, extracts meaningful content using HTML parsing, and exports the data into a structured Excel file with separate sheets for original posts and replies.

# Features
1. Fetches student user information (Name, UID) from a Canvas course.

2. Extracts discussion posts and replies using the Canvas API.

3. Parses HTML message bodies to extract clean text from <p> tags using BeautifulSoup.

4. Saves the extracted data into a two-sheet Excel file using Pandas:

       (i)Initial Comments
       (ii) Replies

5.Handles pagination automatically for large datasets.

6.Robust error handling for failed API requests.

# Technologies Used
Python 3.x
requests (API calls)
BeautifulSoup4 (HTML parsing)
pandas (Excel file generation)

# Setup Instructions
Clone this repository:

bash
Copy
Edit
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Update the following variables in the script:

INSTITUTE: Your Canvas domain/institution ID

COURSE_ID: Your course ID

DISCUSSION_ID: Your discussion topic ID

Authorization: Your Canvas API token (available from user settings)

Run the script:

bash
Copy
Edit
python your_script_name.py
The output Excel file will be saved in the project directory.

# Example Output
XYZ_discussion_1234_output_filtered.xlsx

Sheet 1: Initial Comments

Sheet 2: Replies

# Important Notes
Make sure your Canvas API token has permission to access course users and discussions.

Respect your institution's data privacy guidelines when handling student information.


# BONUS: Requirements.txt
For completeness, create a requirements.txt file like this:

nginx
Copy
Edit
requests
beautifulsoup4
pandas
