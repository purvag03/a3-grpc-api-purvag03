import sys
import os
import grpc
import uuid
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))
import reddit_pb2
import reddit_pb2_grpc

class RedditClient:
    def __init__(self, host='localhost', port=50051):
        channel_address = f'{host}:{port}'
        self.channel = grpc.insecure_channel(channel_address)
        self.stub = reddit_pb2_grpc.RedditServiceStub(self.channel)
        

    def create_post(self, title, text, media_url, author, subreddit):
        # Create a request to create a new post
        post_request = reddit_pb2.CreatePostRequest(
            title=title,
            text=text,
            media_url=media_url,
            author=author,
            subreddit=subreddit
        )

        # Send the request to the server
        post_response = self.stub.CreatePost(post_request)
        return post_response
    
    def vote_post(self, post_id, upvote=True):
        # Create a request to vote on a post
        vote_request = reddit_pb2.VotePostRequest(post_id=post_id, vote=upvote)
        try:
            # Send the vote request to the server
            response = self.stub.VotePost(vote_request)
            print(f"Successfully {'upvoted' if upvote else 'downvoted'} Post ID {post_id}. New Score: {response.new_score}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            
    def get_post(self, post_id):
        # Create a request to get a post by ID
        get_post_request = reddit_pb2.GetPostRequest(post_id=post_id)
        try:
            # Send the request to the server
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
        # Create a request to create a new comment
        comment_request = reddit_pb2.CreateCommentRequest(
            post_id=post_id,
            content=content,
            author=author,
            parent_comment=parent_comment
        )

        try:
            # Send the comment creation request to the server
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
        # Create a request to vote on a comment
        vote_request = reddit_pb2.VoteCommentRequest(comment_id=comment_id, vote=upvote)
        try:
            # Send the vote request to the server
            response = self.stub.VoteComment(vote_request)
            print(f"Successfully {'upvoted' if upvote else 'downvoted'} Comment ID {comment_id}. New Score: {response.new_score}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            
    def list_top_comments(self, post_id, number_of_comments):
        # Create a request to get the top comments for a post
        request = reddit_pb2.TopCommentsRequest(post_id=post_id, number_of_comments=number_of_comments)
        try:
            # Send the request to the server
            response = self.stub.TopComments(request)
            for comment in response.comments:
                print(f"Comment ID: {comment.comment.comment_id}, Score: {comment.comment.score}, Has Replies: {'Yes' if comment.has_replies else 'No'}")
            return response.comments
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            return None
    
    def expand_comment_branch(self, comment_id, number_of_comments):
        # Create a request to expand a comment branch
        request = reddit_pb2.ExpandCommentBranchRequest(comment_id=comment_id, number_of_comments=number_of_comments)
        try:
            # Send the request to the server
            response = self.stub.ExpandCommentBranch(request)
            for comment_tree in response.comments:
                self._print_comment_tree(comment_tree.comment, "  ", comment_tree.replies)
            return response
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")
            return None

    def _print_comment_tree(self, comment, indent, replies):
        # Print the comment tree with indentation
        print(f"{indent}Comment ID: {comment.comment_id}, Score: {comment.score}")
        for reply in replies:
            self._print_comment_tree(reply, indent + "  ", reply.replies)
        
    
    
    
#Added for Manual Testing Purposes 
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
    comment_response = client.create_comment
