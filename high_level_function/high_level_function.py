# Import API client
import sys
import os
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client'))

import reddit_client
import reddit_pb2

def retrieve_post_and_most_upvoted_reply(api_client):
    # Create a post and comments, and vote on them
    post_id = create_post_comments_votes(api_client)
    
    # Retrieve the most upvoted reply under the newly created post
    most_upvoted_comment, most_upvoted_reply = get_most_upvoted_comment_and_reply(api_client, post_id)

    if most_upvoted_comment and most_upvoted_reply:
        # Process the most upvoted comment and reply as needed
        print()
        print("Most Upvoted Comment:")
        print(f"Comment ID: {most_upvoted_comment.comment_id}")
        print(f"Author: {most_upvoted_comment.author}")
        print(f"Content: {most_upvoted_comment.content}")
        print(f"Score: {most_upvoted_comment.score}")

        print("\nMost Upvoted Reply:")
        print(f"Reply ID: {most_upvoted_reply.comment_id}")
        print(f"Author: {most_upvoted_reply.author}")
        print(f"Content: {most_upvoted_reply.content}")
        print(f"Score: {most_upvoted_reply.score}")
    else:
        print("No most upvoted comment and reply found.")

def create_post_comments_votes(api_client):
    title = "Sample Post Title"
    text = "This is a sample post."
    media_url = "example.com/media.mp4"
    author = "user123"
    subreddit = "sampleSubreddit"
    
    post_response = api_client.create_post(title, text, media_url, author, subreddit)

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
    api_client.vote_post(post_id, upvote=True)
    api_client.vote_post(post_id, upvote=True)
    api_client.vote_post(post_id, upvote=False)

    # Create comments and vote on them
    comment_text = "This is a sample comment."
    comment_author = "user456"
    comment_response = api_client.create_comment(post_id, comment_text, comment_author)
    
    if comment_response:
        comment_id = comment_response.comment.comment_id
        api_client.vote_comment(comment_id, upvote=True)
        # api_client.vote_comment(comment_id, upvote=False)
    
    reply_text = "This is a reply to the sample comment."
    reply_author = "user789"
    reply_response = api_client.create_comment(post_id, reply_text, reply_author, parent_comment=comment_id)
    
    reply_text = "This is a reply to the sample comment2."
    reply_response = api_client.create_comment(post_id, reply_text, reply_author, parent_comment=comment_id)
    
    return post_id

def get_most_upvoted_comment_and_reply(api_client, post_id):
    # Retrieve the most upvoted comment under the newly created post
    most_upvoted_comments = api_client.list_top_comments(post_id=post_id, number_of_comments=1)

    if most_upvoted_comments:
        most_upvoted_comment = most_upvoted_comments[0].comment

        if most_upvoted_comment.replies:
            # Retrieve the most upvoted reply under the most upvoted comment
            most_upvoted_reply = max(most_upvoted_comment.replies, key=lambda r: r.score)
            return most_upvoted_comment, most_upvoted_reply

    return None, None

if __name__ == "__main__":
    # Create an instance of your API client
    client = reddit_client.RedditClient()

    # Call the function to retrieve a post and the most upvoted comment and reply
    retrieve_post_and_most_upvoted_reply(client)
