import sys
import os
import grpc
from concurrent import futures
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import reddit_pb2
import reddit_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp
import datetime

class RedditClient:
    def __init__(self, host='localhost', port=50051):
        channel_address = f'{host}:{port}'
        self.channel = grpc.insecure_channel(channel_address)
        self.stub = reddit_pb2_grpc.RedditServiceStub(self.channel)

    def create_post(self, title, text, media_url, author, subreddit):
        # Create a Timestamp for the current time
        now = datetime.datetime.utcnow()
        publication_date = Timestamp()
        publication_date.FromDatetime(now)
        
        # Convert the Timestamp to a datetime object
        publication_datetime = publication_date.ToDatetime()

        # Format the datetime object into a readable string
        readable_date = publication_datetime.strftime("%Y-%m-%d %H:%M:%S.%f UTC")

        post_request = reddit_pb2.CreatePostRequest(
            title=title,
            text=text,
            media_url=media_url,
            author=author,
            subreddit=subreddit,
            publication_date=publication_date
        )
        
        if media_url:
            if media_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                media = reddit_pb2.Post(image_url=media_url)
            elif media_url.endswith(('.mp4', '.avi', '.mov')):
                media = reddit_pb2.Post(video_url=media_url)

        return self.stub.CreatePost(post_request)
    
    def convert_timestamp_to_readable(seconds, nanos):
        # Convert to datetime
        timestamp = datetime.datetime.utcfromtimestamp(seconds) + datetime.timedelta(microseconds=nanos / 1000)

        # Format to a readable string
        return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f UTC")

def main():
    client = RedditClient()
    title = "Sample Post Title"
    text = "This is a sample post."
    media_url = "example.com/media.jpg"  # Could be an image or video URL
    author = "user123"
    subreddit = "sampleSubreddit"
    
    response = client.create_post(title, text, media_url, author, subreddit)

    # Printing the entire Post object
    print("Post Created:")
    print(f"Post ID: {response.post.post_id}")
    print(f"Title: {response.post.title}")
    print(f"Text: {response.post.text}")
    print(f"Author: {response.post.author}")
    print(f"Score: {response.post.score}")
    print(f"State: {reddit_pb2.Post.State.Name(response.post.state)}")
    print(f"Publication Date: {response.post.publication_date}")
    print(f"Subreddit ID: {response.post.subreddit_id}")
    # Check which media field is set and print it
    if response.post.HasField('video_url'):
        print(f"Video URL: {response.post.video_url}")
    elif response.post.HasField('image_url'):
        print(f"Image URL: {response.post.image_url}")


if __name__ == "__main__":
    main()
