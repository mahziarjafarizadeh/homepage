import os
import requests
import json

# Get the Access Token from an environment variable for security
# In GitHub Actions, this will be a "Secret"
token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
if not token:
    raise ValueError("INSTAGRAM_ACCESS_TOKEN environment variable not set!")

# Define the fields you want to get from the API
# You can customize this list based on your needs
fields = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,like_count,comments_count"
limit = 24  # How many recent posts to fetch

# Construct the API URL
url = f"https://graph.instagram.com/me/media?fields={fields}&access_token={token}&limit={limit}"

print("Fetching latest Instagram posts...")

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    
    data = response.json().get('data', [])
    
    if not data:
        print("No posts found or API response was empty.")
    else:
        # Create a new list with just the data we need
        # This simplifies the JSON file and ensures consistency
        simplified_posts = []
        for post in data:
            simplified_posts.append({
                'id': post.get('id'),
                'caption': post.get('caption', ''), # Use a default empty string if no caption
                'media_type': post.get('media_type'),
                'media_url': post.get('media_url'),
                'permalink': post.get('permalink'),
                'thumbnail_url': post.get('thumbnail_url', None), # May not exist for images
                'timestamp': post.get('timestamp'),
                'like_count': post.get('like_count', 0),
                'comments_count': post.get('comments_count', 0)
            })

        # Save the data to a JSON file in the root of your project
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(simplified_posts, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully fetched and saved {len(simplified_posts)} posts to posts.json.")

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
