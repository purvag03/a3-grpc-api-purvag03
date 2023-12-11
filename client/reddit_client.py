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
    
    def vote_post(self, post_id, upvote=True):
        # Determine the vote type (upvote or downvote)
        vote_type = "upvoted" if upvote else "downvoted"
        
        vote_request = reddit_pb2.VotePostRequest(post_id=post_id, vote=upvote)
        try:
            response = self.stub.VotePost(vote_request)
            print(f"Successfully {vote_type} Post ID {post_id}. New Score: {response.new_score}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            
    def get_post(self, post_id):
        get_post_request = reddit_pb2.GetPostRequest(post_id=post_id)
        try:
            response = self.stub.GetPost(get_post_request)
            if response.post:
                return response.post
            else:
                print("Post not found")
                return None
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            return None

    def get_all_post_ids(self):
        return list(self.posts.keys())  # You can modify this to match your data structure

def main():
    client = RedditClient()
    title = "Sample Post Title"
    text = "This is a sample post."
    media_url = "example.com/media.mp4"  # Could be an image or video URL
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
    print(f"Subreddit ID: {response.post.subreddit_id}")
    # Check which media field is set and print it
    if response.post.HasField('video_url'):
        print(f"Video URL: {response.post.video_url}")
    elif response.post.HasField('image_url'):
        print(f"Image URL: {response.post.image_url}")
    print(f"Publication Date: {response.post.publication_date}")
    
    # Vote on a post
    post_id = response.post.post_id
    client.vote_post(post_id, upvote=True)  # Upvote the post
    client.vote_post(post_id, upvote=True) # Upvote the post again 
    client.vote_post(post_id, upvote=False)  # Downvote the post

    # Retrieve the content of the post
    retrieved_post = client.get_post(post_id)
    if retrieved_post:
        print("Retrieved Post Content:")
        print(f"Post ID: {retrieved_post.post_id}")
        print(f"Title: {retrieved_post.title}")
        print(f"Text: {retrieved_post.text}")
        print(f"Author: {retrieved_post.author}")
        print(f"Score: {retrieved_post.score}")
        print(f"State: {reddit_pb2.Post.State.Name(retrieved_post.state)}")
        print(f"Subreddit ID: {retrieved_post.subreddit_id}")
        # Check which media field is set and print it
        if retrieved_post.HasField('video_url'):
            print(f"Video URL: {retrieved_post.video_url}")
        elif retrieved_post.HasField('image_url'):
            print(f"Image URL: {retrieved_post.image_url}")
        print(f"Publication Date: {retrieved_post.publication_date}")

if __name__ == "__main__":
    main()
