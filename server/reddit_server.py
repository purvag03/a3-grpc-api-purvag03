import sys
import os
from concurrent import futures
import grpc
import uuid
from datetime import datetime

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
            publication_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            comment_id=comment_id,
            author=request.author,
            content=request.content,
            score=0,  # Initial score
            state=reddit_pb2.Comment.NORMAL,
            publication_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            parent_id=request.post_id if not request.parent_comment else request.parent_comment
        )

        # If the comment is a reply to a post
        if not request.parent_comment:
            if request.post_id in self.posts:
                self.posts[request.post_id].comments.append(new_comment)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Post not found')
                return reddit_pb2.CommentResponse()

        # If the comment is a reply to another comment
        else:
            parent_found = False
            for post in self.posts.values():
                for parent_comment in post.comments:
                    if parent_comment.comment_id == request.parent_comment:
                        # Check if the parent comment already has a 'replies' attribute
                        if not hasattr(parent_comment, 'replies'):
                            parent_comment.replies = []
                        
                        # Append the new comment as a reply to the parent comment
                        parent_comment.replies.append(new_comment)
                        parent_found = True
                        break

                if parent_found:
                    break

            if not parent_found:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Parent comment not found')
                return reddit_pb2.CommentResponse()

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

    def TopComments(self, request, context):
        post_id = request.post_id
        number_of_comments = request.number_of_comments

        if post_id not in self.posts:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return reddit_pb2.TopCommentsResponse()

        post = self.posts[post_id]
        sorted_comments = sorted(post.comments, key=lambda c: c.score, reverse=True)[:number_of_comments]

        response = reddit_pb2.TopCommentsResponse()
        for comment in sorted_comments:
            comment_with_replies = response.comments.add()
            comment_with_replies.comment.CopyFrom(comment)
            comment_with_replies.has_replies = self._has_replies(comment.comment_id)

        return response

    def _has_replies(self, comment_id):
        for post in self.posts.values():
            for comment in post.comments:
                # Check direct comments
                if comment.comment_id == comment_id and hasattr(comment, 'replies') and comment.replies:
                    return True
                # Check nested replies
                if self._check_replies_for_comment(comment.replies, comment_id):
                    return True
        return False

    def _check_replies_for_comment(self, replies, comment_id):
        for reply in replies:
            if reply.comment_id == comment_id and hasattr(reply, 'replies') and reply.replies:
                return True
            # Recursively check for nested replies
            if self._check_replies_for_comment(reply.replies, comment_id):
                return True
        return False

    def _get_top_comments(self, comments, number_of_comments):
        return sorted(comments, key=lambda c: c.score, reverse=True)[:number_of_comments]
    
    def ExpandCommentBranch(self, request, context):
        comment_id = request.comment_id
        number_of_comments = request.number_of_comments

        comment_tree = []

        for post in self.posts.values():
            for comment in post.comments:
                if comment.comment_id == comment_id:
                    # Create a CommentTree for the main comment
                    comment_tree_node = reddit_pb2.ExpandCommentBranchResponse.CommentTree(comment=comment)
                    # Get top N replies for the main comment
                    top_replies = self._get_top_comments(comment.replies, number_of_comments)

                    for reply in top_replies:
                        # Append each top reply to the replies of the main comment
                        comment_tree_node.replies.append(reply)

                        # For each top reply, get its top N replies
                        reply_top_replies = self._get_top_comments(reply.replies, number_of_comments)
                        for reply_top_reply in reply_top_replies:
                            # Each of these replies is directly added to the replies of the main comment
                            comment_tree_node.replies.append(reply_top_reply)

                    comment_tree.append(comment_tree_node)
                    break

        return reddit_pb2.ExpandCommentBranchResponse(comments=comment_tree)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_pb2_grpc.add_RedditServiceServicer_to_server(RedditService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
