import requests
import os
from urllib.parse import urlparse

# This is a list of URLs I want to download.
# Challenge Question 1: Modify the program to handle multiple URLs at once.
# I solved this by using a list and looping through each URL.
urls = [
    "https://upload.wikimedia.org/wikipedia/commons/4/4e/Apollo_11_launch_-_GPN-2000-001095.jpg",
    "https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/main_image_star-forming_region_ngc346_hubble_nasa.jpg",
    "https://www.google.com/nonexistent_image.png", # This is an invalid URL to test error handling
    "https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/main_image_star-forming_region_ngc346_hubble_nasa.jpg" # A duplicate URL to test question 3
]

def fetch_and_save_image(url):
    """
    Fetches an image from a given URL and saves it to the Fetched_Images directory.
    Handles errors and implements checks for safety and efficiency.
    """
    try:
        # Extract filename from URL or generate a default one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"
        
        filepath = os.path.join("Fetched_Images", filename)

        # Challenge Question 3: Prevent downloading duplicate images.
        # Check if the file already exists before making a web request.
        if os.path.exists(filepath):
            print(f"ℹ️ Skipping download: {filename} already exists.")
            return
            
        # Fetch the image with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Challenge Question 4: Check important HTTP headers.
        # Check Content-Type to ensure the file is an image and Content-Length to avoid large files.
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            print(f"❌ Warning: URL does not appear to be an image. Content-Type: {content_type}")
            return
        
        # Challenge Question 2: Implement precautions for unknown sources.
        # By checking the Content-Type, I am implementing a key precaution.
        content_length = int(response.headers.get('Content-Length', 0))
        max_size_mb = 5  # Set a max size of 5MB
        max_size_bytes = max_size_mb * 1024 * 1024
        if content_length > max_size_bytes:
            print(f"❌ Skipping download: File size ({content_length} bytes) exceeds the limit of {max_size_mb} MB.")
            return

        # Save the image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✔️ Successfully fetched: {filename}")
        print(f"✔️ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error for {url}: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create the directory if it doesn't exist.
    # I used exist_ok=True to prevent an error if the folder is already there.
    os.makedirs("Fetched_Images", exist_ok=True)
    
    # Loop through the list of URLs and process each one.
    for url in urls:
        print(f"\nAttempting to download from: {url}")
        fetch_and_save_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()