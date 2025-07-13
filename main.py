from dotenv import load_dotenv
import os
import colorama
import praw

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

subreddit_name = input("Enter the subreddit name: ")
num_posts = int(input("Enter the number of posts to display: "))
post_limit = num_posts + 10
subreddit = reddit.subreddit(subreddit_name)
count = 0
for submission in subreddit.hot(limit=post_limit):
    title_lower = submission.title.lower()
    if "daily thread" not in title_lower and "any political content" not in title_lower:
        print(
            f"{colorama.Fore.RED}{count + 1}. {colorama.Style.RESET_ALL}"
            f"{colorama.Fore.YELLOW}Title:{colorama.Fore.GREEN} {submission.title} "
            f"{colorama.Fore.MAGENTA}| "
            f"{colorama.Fore.YELLOW}Upvotes:{colorama.Fore.GREEN} {submission.score}{colorama.Style.RESET_ALL}"
        )
        count += 1
        if count == num_posts:
            break

print(f"{colorama.Fore.RED}Total posts displayed: {colorama.Fore.GREEN}{count}{colorama.Style.RESET_ALL}")