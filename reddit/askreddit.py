from utils.console import print_markdown, print_step, print_substep
import praw
import random
from dotenv import load_dotenv
import os


def get_askreddit_threads():
    """
    Returns a list of threads from the AskReddit subreddit.
    """

    print_step("Getting AskReddit threads...")

    content = {}
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing AskReddit threads",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )
    askreddit = reddit.subreddit("askreddit")
    # change to update number of choices that show up in console
    number_choices = 25
    choices_string = ""
    number = 1
    for thread in askreddit.hot(limit=number_choices):
        choices_string += f"{number}) {thread.title}\n"
        number += 1
    submissionChoice = input(f"{choices_string}\nWhich thread would you like to use? ")
    submission = list(askreddit.hot(limit=number_choices))[int(submissionChoice) - 1]
    print_substep(f"Video will be: {submission.title} :thumbsup:")
    try:

        content["thread_url"] = submission.url
        content["thread_title"] = submission.title
        content["comments"] = []

        for top_level_comment in submission.comments:
            content["comments"].append(
                {
                    "comment_body": top_level_comment.body,
                    "comment_url": top_level_comment.permalink,
                    "comment_id": top_level_comment.id,
                }
            )

    except AttributeError as e:
        pass
    print_substep("Received AskReddit threads Successfully.", style="bold green")
    return content
