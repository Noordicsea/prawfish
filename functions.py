from dotenv import load_dotenv
import os
import colorama
import praw


def get_subreddit_instance(subreddit_name):
    """
    Creates and returns a Reddit subreddit instance using environment variables.
    
    Args:
        subreddit_name (str): Name of the subreddit to access
        
    Returns:
        praw.models.Subreddit: Reddit subreddit instance
    """
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    return reddit.subreddit(subreddit_name)


def get_direct_media_link(submission):
    """
    Extracts direct media links from a Reddit submission.
    
    Args:
        submission: Reddit submission object
        
    Returns:
        str or list or None: Direct media link(s) or None if not found
    """
    # Try to extract direct media links (images, videos, gifs)
    if hasattr(submission, "post_hint"):
        if submission.post_hint == "image" and hasattr(submission, "url"):
            return submission.url
        if submission.post_hint == "hosted:video" and hasattr(submission, "media") and submission.media:
            reddit_video = submission.media.get("reddit_video")
            if reddit_video and "fallback_url" in reddit_video:
                return reddit_video["fallback_url"]
        if submission.post_hint == "rich:video" and hasattr(submission, "media") and submission.media:
            oembed = submission.media.get("oembed")
            if oembed and "thumbnail_url" in oembed:
                return oembed["thumbnail_url"]
    
    # Fallback for galleries
    if hasattr(submission, "is_gallery") and submission.is_gallery:
        media_items = []
        if hasattr(submission, "media_metadata"):
            for item in submission.media_metadata.values():
                if "s" in item and "u" in item["s"]:
                    media_items.append(item["s"]["u"])
        return media_items if media_items else None
    
    # Fallback for gifs or direct links
    if hasattr(submission, "url"):
        if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm')):
            return submission.url
    
    return None


def display_and_select_posts(subreddit, post_limit, num_posts, posts, count):
    """
    Displays posts from a subreddit and allows user to select one.
    
    Args:
        subreddit: Reddit subreddit instance
        post_limit (int): Maximum number of posts to fetch
        num_posts (int): Number of posts to display
        posts (list): List to store post objects
        count (int): Current count of displayed posts
        
    Returns:
        praw.models.Submission or None: Selected post or None if no posts found
    """
    for submission in subreddit.hot(limit=post_limit):
        title_lower = submission.title.lower()
        if "daily thread" not in title_lower and "any political content" not in title_lower:
            posts.append(submission)
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

    if count == 0:
        print(f"{colorama.Fore.RED}No posts found matching the criteria.{colorama.Style.RESET_ALL}")
        return None
    else:
        while True:
            try:
                selection = int(input(f"Select a post by number (1-{count}): "))
                if 1 <= selection <= count:
                    selected_post = posts[selection - 1]
                    break
                else:
                    print(f"{colorama.Fore.RED}Please enter a number between 1 and {count}.{colorama.Style.RESET_ALL}")
            except ValueError:
                print(f"{colorama.Fore.RED}Invalid input. Please enter a number.{colorama.Style.RESET_ALL}")

        print(f"\n{colorama.Fore.CYAN}--- Post Details ---{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Title:{colorama.Fore.GREEN} {selected_post.title}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Author:{colorama.Fore.GREEN} {getattr(selected_post.author, 'name', 'N/A')}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Score:{colorama.Fore.GREEN} {selected_post.score}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}ID:{colorama.Fore.GREEN} {selected_post.id}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}URL:{colorama.Fore.GREEN} {selected_post.url}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Permalink:{colorama.Fore.GREEN} https://reddit.com{selected_post.permalink}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Created (UTC):{colorama.Fore.GREEN} {selected_post.created_utc}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Number of Comments:{colorama.Fore.GREEN} {selected_post.num_comments}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Selftext:{colorama.Fore.GREEN} {selected_post.selftext[:500]}{'...' if len(selected_post.selftext) > 500 else ''}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Is NSFW:{colorama.Fore.GREEN} {selected_post.over_18}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Is Stickied:{colorama.Fore.GREEN} {selected_post.stickied}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Subreddit:{colorama.Fore.GREEN} {selected_post.subreddit.display_name}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.YELLOW}Flair:{colorama.Fore.GREEN} {selected_post.link_flair_text}{colorama.Style.RESET_ALL}")
        
        # Direct media link(s)
        media_link = get_direct_media_link(selected_post)
        if media_link:
            print(f"{colorama.Fore.YELLOW}Direct Media Link(s):{colorama.Style.RESET_ALL}")
            if isinstance(media_link, (list, tuple, set)):
                for link in media_link:
                    print(f"{colorama.Fore.GREEN}{link}{colorama.Style.RESET_ALL}")
            else:
                print(f"{colorama.Fore.GREEN}{media_link}{colorama.Style.RESET_ALL}")
            print()
        else:
            print(f"{colorama.Fore.YELLOW}Direct Media Link(s):{colorama.Fore.RED} None found{colorama.Style.RESET_ALL}")
        
        return selected_post 