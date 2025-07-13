from functions import get_subreddit_instance, display_and_select_posts
from downloader.downloader import download_media_from_link

subreddit_name = input("Enter the subreddit name: ")
num_posts = int(input("Enter the number of posts to display: "))
post_limit = num_posts + 10
posts = []
count = 0

subreddit = get_subreddit_instance(subreddit_name)
selected_post = display_and_select_posts(subreddit, post_limit, num_posts, posts, count)

if selected_post:
    # Feed the Reddit post URL directly to yt-dlp, not the direct media link
    post_url = selected_post.url
    print(f"Attempting to download media from post URL: {post_url}")
    downloaded_path = download_media_from_link(post_url)
    if downloaded_path:
        import os
        actual_path = downloaded_path
        # If the output path contains yt-dlp template variables, try to resolve the actual file path
        if "%(title)s" in downloaded_path or "%(ext)s" in downloaded_path:
            # Try to find the downloaded file in the downloads directory
            downloads_dir = "downloads"
            if os.path.isdir(downloads_dir):
                files = os.listdir(downloads_dir)
                if files:
                    # Get the most recently modified file
                    files = [os.path.join(downloads_dir, f) for f in files]
                    actual_path = max(files, key=os.path.getmtime)
        print(f"Media downloaded successfully to: {actual_path}")
    else:
        print("Failed to download media.")
else:
    print("No post was selected.")
