import sys
import os
from concurrent import futures
import grpc
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import reddit_pb2
import reddit_pb2_grpc

class RedditService(reddit_pb2_grpc.RedditServiceServicer):
    def __init__(self):
        self.posts = {}

    def CreatePost(self, request, context):
        # Generate a unique ID for the post
        post_id = str(uuid.uuid4())
        
        # Create a new Post object with the generated ID
        new_post = reddit_pb2.Post(
            title=request.title,
            text=request.text,
            author=request.author,
            score=0,  # Initial score
            state=reddit_pb2.Post.NORMAL,
            publication_date=request.publication_date,
            subreddit_id=request.subreddit,
            post_id=post_id  # Set the generated ID
        )

        # Determine the media type and set the appropriate field
        if request.media_url:
            if request.media_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                new_post.image_url = request.media_url
            elif request.media_url.endswith(('.mp4', '.avi', '.mov')):
                new_post.video_url = request.media_url

        # Store the post
        self.posts[post_id] = new_post

        return reddit_pb2.PostResponse(post=new_post)


    def VotePost(self, request, context):
        post_id = request.post_id
        vote = request.vote  # True for upvote, False for downvote

        if post_id in self.posts:
            if vote:
                self.posts[post_id].score += 1
                
            else:
                self.posts[post_id].score -= 1
                

            return reddit_pb2.VoteResponse(new_score=self.posts[post_id].score)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return reddit_pb2.VoteResponse()
        
    def GetPost(self, request, context):
        post_id = request.post_id

        if post_id in self.posts:
            return reddit_pb2.PostResponse(post=self.posts[post_id])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return reddit_pb2.PostResponse()
    
    def CreateComment(self, request, context):
        # Generate a unique ID for the comment
        comment_id = str(uuid.uuid4())

        # Create a new Comment object with the generated ID
        new_comment = reddit_pb2.Comment(
            content=request.content,
            author=request.author,
            comment_id=comment_id  # Set the generated ID
        )

        # Add the comment to the post (you may need to modify your data structure)
        if request.post_id in self.posts:
            self.posts[request.post_id].comments.append(new_comment)

        return reddit_pb2.CommentResponse(comment=new_comment)
    
    def VoteComment(self, request, context):
        comment_id = request.comment_id
        vote = request.vote  # True for upvote, False for downvote

        # Find the comment and update its score
        for post in self.posts.values():
            for comment in post.comments:
                if comment.comment_id == comment_id:
                    if vote:
                        comment.score += 1
                    else:
                        comment.score -= 1
                    return reddit_pb2.VoteResponse(new_score=comment.score)

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Comment not found')
        return reddit_pb2.VoteResponse()



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_pb2_grpc.add_RedditServiceServicer_to_server(RedditService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
