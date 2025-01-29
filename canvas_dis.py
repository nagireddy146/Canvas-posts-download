import requests
import pandas as pd
from bs4 import BeautifulSoup

# Canvas API Configuration
INSTITUTE = "" #add your institute ID
COURSE_ID = ""  # Replace with your COURSE ID
DISCUSSION_ID = ""  # Replace with your Discussion ID

# Authorization Header
headers = {
    "Authorization": "Bearer "  # Replace with your actual token ( you can get this token from canvas settings)
}

# Function to fetch the list of users
def get_users(course_id):
    """Fetches the list of users with their names and SIS IDs."""
    print("Fetching user list...")
    url = f"https://{INSTITUTE}.instructure.com/api/v1/courses/{course_id}/users"
    params = {"enrollment_type": "student", "per_page": 100}
    user_mapping = {}

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch users: {response.status_code}, {response.text}")
            exit()

        data = response.json()
        for user in data:
            user_id = user.get("id")
            sis_id = user.get("sis_user_id", None)  # SIS ID
            name = user.get("name", f"User_{user_id}")
            if sis_id:  # Link SIS ID to name
                user_mapping[user_id] = {"name": name, "uid": sis_id}

        # Pagination
        url = response.links.get("next", {}).get("url")

    return user_mapping

# Function to extract main messages from HTML
def extract_main_message(html_content):
    """Extract message content inside <p> tags."""
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = soup.find_all("p")
    return " ".join(p.get_text(strip=True) for p in paragraphs)

# Fetch and process the discussion data
def fetch_discussion(course_id, discussion_id, user_mapping):
    """Fetch and process discussion data with UID mapping."""
    print(f"Fetching discussion {discussion_id}...")
    url = f"https://{INSTITUTE}.instructure.com/api/v1/courses/{course_id}/discussion_topics/{discussion_id}/view?include_new_entries=1"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch discussion: {response.status_code}, {response.text}")
        exit()

    discussion_data = response.json()
    initial_comments = []
    replies = []

    for entry in discussion_data.get("view", []):
        user_id = entry.get("user_id")
        user_info = user_mapping.get(user_id, {})
        main_student_name = user_info.get("name", f"User_{user_id}")
        main_student_uid = user_info.get("uid", "Unknown")
        main_comment_html = entry.get("message", "")
        main_comment = extract_main_message(main_comment_html)

        # Add initial comment to list
        initial_comments.append({
            "UID": main_student_uid,
            "Name": main_student_name,
            "Comment": main_comment,
        })

        # Process replies
        for reply in entry.get("replies", []):
            replied_user_id = reply.get("user_id")
            replied_user_info = user_mapping.get(replied_user_id, {})
            reply_student_name = replied_user_info.get("name", None)
            reply_student_uid = replied_user_info.get("uid", None)
            reply_message_html = reply.get("message", "")
            reply_message = extract_main_message(reply_message_html)

            # Add reply only if valid
            if reply_student_name and reply_student_uid and reply_message:
                replies.append({
                    "Reply Student UID": reply_student_uid,
                    "Reply Student Name": reply_student_name,
                    "Reply": reply_message,
                    "Original Post": main_comment
                })

    return initial_comments, replies

# Save the results
def save_results(initial_comments, replies, course_id, discussion_id):
    """Save the output to Excel with two sheets."""
    output_excel_file = f"{INSTITUTE}_discussion_{discussion_id}_output_filtered.xlsx"

    # Create Pandas DataFrames
    initial_comments_df = pd.DataFrame(initial_comments)
    replies_df = pd.DataFrame(replies)

    # Write to Excel with two sheets
    with pd.ExcelWriter(output_excel_file) as writer:
        initial_comments_df.to_excel(writer, sheet_name="Initial Comments", index=False)
        replies_df.to_excel(writer, sheet_name="Replies", index=False)

    print(f"Excel file saved as {output_excel_file}")

# Main Script Execution
if __name__ == "__main__":
    # Step 1: Fetch user list
    user_mapping = get_users(COURSE_ID)

    # Step 2: Fetch discussion data and process it
    initial_comments, replies = fetch_discussion(COURSE_ID, DISCUSSION_ID, user_mapping)

    # Step 3: Save results to Excel
    save_results(initial_comments, replies, COURSE_ID, DISCUSSION_ID)
