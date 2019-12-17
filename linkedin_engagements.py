import os
import sys
from datetime import datetime

from linkedin_api import Linkedin

from get_posts import get_updates, get_post_link_and_social_activity
from linkedin_tool_helpers import get_company_name, get_key


def get_engagements(linkedin_object, company, total_likes=0, total_posts=0):
    company_universal_name = get_company_name(company)
    print(f"Looking engagements for : {company_universal_name}")
    company_updates = get_updates(
        linkedin_object=linkedin_object, company_name=company_universal_name
    )
    if company_updates:
        for post in company_updates:
            post_link, post_like = get_post_link_and_social_activity(item=post)
            total_likes += post_like
        total_posts += len(company_updates)
        return total_posts, total_likes
    else:
        print("Company doesnt have any post and likes!!")
        return None, None


def compare_engagements(linkedin_object, companies=[]):
    response = input(
        "Enter the company urn or linkedin url or type done to start comparing or type exit: "
    ).strip()
    if response.lower() == "exit":
        sys.exit("Quiting the Tool!!")
    elif response.lower() == "done":
        os.system("clear")
        print(f"Selected comapnies: {companies}")
        print("=" * 130)
        for company in companies:
            start_time = datetime.now()
            total_posts, total_likes = get_engagements(linkedin_object, company)
            print(f"Total Posts= {total_posts}, Total Likes= {total_likes}")
            print(f"Time taken to fetch the result= {datetime.now() - start_time}")
            print("=" * 130)
        return compare_engagements(linkedin_object, companies=[])
    elif len(response) == 0:
        os.system("clear")
        print(f"Selected comapnies: {companies}")
        print("Response cant be empty!.Try again", file=sys.stderr)
        return compare_engagements(linkedin_object, companies=companies)
    else:
        companies.append(response)
        os.system("clear")
        print(f"Selected comapnies: {companies}")
        return compare_engagements(linkedin_object, companies=companies)


if __name__ == "__main__":
    username, password = get_key()
    # Authenticate using any Linkedin account credentials
    linkedin_object = Linkedin(username=username, password=password)
    compare_engagements(linkedin_object)
