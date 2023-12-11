import sys
import os
import grpc
import uuid
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))
import reddit_pb2
import reddit_pb2_grpc

class RedditClient:
    def __init__(self, host='localhost', port=50051):
        channel_address = f'{host}:{port}'
        self.channel = grpc.insecure_channel(channel_address)
        self.stub = reddit_pb2_grpc.RedditServiceStub(self.channel)

    def create_post(self, title, text, media_url, author, subreddit):
        now = datetime.datetime.utcnow()
        publication_date = Timestamp()
        publication_date.FromDatetime(now)

        post_request = reddit_pb2.CreatePostRequest(
            title=title,
            text=text,
            media_url=media_url,
            author=author,
            subreddit=subreddit,
            publication_date=publication_date
        )

        return self.stub.CreatePost(post_request)
    
    def vote_post(self, post_id, upvote=True):
        vote_request = reddit_pb2.VotePostRequest(post_id=post_id, vote=upvote)
        try:
            response = self.stub.VotePost(vote_request)
            print(f"Successfully {'upvoted' if upvote else 'downvoted'} Post ID {post_id}. New Score: {response.new_score}")
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

    def create_comment(self, post_id, content, author, parent_comment=None):
        comment_request = reddit_pb2.CreateCommentRequest(
            post_id=post_id,
            content=content,
            author=author,
            parent_comment=parent_comment
        )

        try:
            response = self.stub.CreateComment(comment_request)
            if response:
                print(f"Comment created with ID: {response.comment.comment_id}")
                print(f"Comment: {response.comment.content}")
                print(f"Author: {response.comment.author}")
                return response
            else:
                print("No response received from server")
                return None
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            return None

    def vote_comment(self, comment_id, upvote=True):
        vote_request = reddit_pb2.VoteCommentRequest(comment_id=comment_id, vote=upvote)
        try:
            response = self.stub.VoteComment(vote_request)
            print(f"Successfully {'upvoted' if upvote else 'downvoted'} Comment ID {comment_id}. New Score: {response.new_score}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")

def main():
    client = RedditClient()
    title = "Sample Post Title"
    text = "This is a sample post."
    media_url = "example.com/media.mp4"
    author = "user123"
    subreddit = "sampleSubreddit"
    
    post_response = client.create_post(title, text, media_url, author, subreddit)

    print("\nPost Created:")
    print(f"Post ID: {post_response.post.post_id}")
    print(f"Title: {post_response.post.title}")
    print(f"Text: {post_response.post.text}")
    print(f"Author: {post_response.post.author}")
    print(f"Score: {post_response.post.score}")
    print(f"State: {reddit_pb2.Post.State.Name(post_response.post.state)}")
    print(f"Subreddit ID: {post_response.post.subreddit_id}")
    print(f"Publication Date: {post_response.post.publication_date}")

    post_id = post_response.post.post_id
    client.vote_post(post_id, upvote=True)
    client.vote_post(post_id, upvote=True)
    client.vote_post(post_id, upvote=False)

    retrieved_post = client.get_post(post_id)
    if retrieved_post:
        print("\nRetrieved Post Content:")
        print(f"Post ID: {retrieved_post.post_id}")
        print(f"Title: {retrieved_post.title}")
        print(f"Text: {retrieved_post.text}")
        print(f"Author: {retrieved_post.author}")
        print(f"Score: {retrieved_post.score}")
        print(f"State: {reddit_pb2.Post.State.Name(retrieved_post.state)}")
        print(f"Subreddit ID: {retrieved_post.subreddit_id}")
        print(f"Publication Date: {retrieved_post.publication_date}")

    comment_text = "This is a sample comment."
    comment_author = "user456"
    comment_response = client.create_comment(post_id, comment_text, comment_author)
    
    if comment_response:
        comment_id = comment_response.comment.comment_id
        client.vote_comment(comment_id, upvote=True)
        client.vote_comment(comment_id, upvote=False)
         
    reply_text = "This is a reply to the sample comment."
    reply_author = "user789"
    reply_response = client.create_comment(post_id, reply_text, reply_author, parent_comment=comment_id)
    if reply_response:
        print(f"Reply created with ID: {reply_response.comment.comment_id}")
        print(f"Reply: {reply_response.comment.content}")
        print(f"Author: {reply_response.comment.author}")
    else:
        print("Failed to create reply")

if __name__ == "__main__":
    main()
