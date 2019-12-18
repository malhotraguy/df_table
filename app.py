from datetime import datetime

import pandas as pd
from flask import Flask, request, render_template, abort

from get_posts import get_updates, get_post_link_and_social_activity, get_url
from linkedin_engagements import get_engagements
from linkedin_id import get_linkedin_id
from linkedin_tool_helpers import get_company_name, get_linkedin_object

app = Flask(__name__)
linkedin_object = get_linkedin_object()


@app.route("/", methods=["GET", "POST"])
def welcome():
    return "Welcome to LinkedIn Tool"


@app.route("/id", methods=("POST", "GET"))
def id_html_table():
    start_time = datetime.now()
    company_identifier = request.args.get("company")
    company = get_company_name(input_string=company_identifier)
    df_ids = get_linkedin_id(company_name=company, linkedin_object=linkedin_object)
    print(f"Time taken to fetch the result= {datetime.now() - start_time}")
    print("=" * 130)
    return render_template(
        "simple.html",
        page_title=f"IDs for {company}",
        tables=[
            df_ids.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_ids.columns.values,
    )


@app.route("/posts", methods=("POST", "GET"))
def posts_html_table():
    start_time = datetime.now()
    company_identifier = request.args.get("company")
    company = get_company_name(input_string=company_identifier)
    company_updates = get_updates(linkedin_object=linkedin_object, company_name=company)
    if not company_updates:
        return f"No post for :{company_identifier}"
    df_post = pd.DataFrame()
    for update in company_updates:
        linkedin_post_link, total_likes = get_post_link_and_social_activity(item=update)
        shared_url = get_url(item=update)
        df_post = df_post.append(
            {
                "LinkedIn Post Url": linkedin_post_link,
                "Total Likes": total_likes,
                "Shared Url": shared_url,
            },
            ignore_index=True,
        )
    print(f"Time taken to fetch the result= {datetime.now() - start_time}")
    print("=" * 130)
    return render_template(
        "simple.html",
        page_title=f"Posts for {company}",
        tables=[
            df_post.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_post.columns.values,
    )


@app.route("/compare", methods=("POST", "GET"))
def compare_engagements():
    companies = request.args.getlist("company", type=str)
    print(companies)
    if type(companies) is not list or len(companies) == 0:
        abort(400, "Check the arguments passed with 'company' parameter of the URL")
    df_engagements = pd.DataFrame()
    for company in companies:
        total_posts, total_likes = get_engagements(linkedin_object, company)
        df_engagements = df_engagements.append(
            {
                "Company": company,
                "Total Posts": total_posts,
                "Total Likes": total_likes,
            },
            ignore_index=True,
        )
    return render_template(
        "simple.html",
        page_title=f"Comparing Engagements",
        tables=[
            df_engagements.to_html(
                classes=["table-bordered", "table-striped", "table-hover"],
                justify="initial",
                render_links=True,
                escape=False,
                float_format="{:,.0f}".format,
            )
        ],
        titles=df_engagements.columns.values,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
