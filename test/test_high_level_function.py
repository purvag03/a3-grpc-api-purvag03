import unittest
import sys
import os
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client'))

import reddit_client
import reddit_pb2

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'high_level_function'))
from high_level_function import RedditPostManager

class TestRetrievePostAndMostUpvotedReply(unittest.TestCase):
    def test_retrieve_post_and_most_upvoted_reply(self):
        # Create a mock Reddit API client
        api_client = MagicMock()

        # Mock the behavior of create_post_comments_votes
        api_client.create_post.return_value = Mock(
            post=Mock(
                post_id="123",
                title="Sample Post Title",
                text="This is a sample post.",
                author="user123",
                score=0,
                state=0,  # Assuming State is an enum with 0 as a valid value
                subreddit_id="456",
                publication_date="2023-01-01T00:00:00Z",
            )
        )
        
        # Mock the behavior of list_top_comments
        api_client.list_top_comments.return_value = [
            Mock(
                comment=Mock(
                    comment_id="789",
                    author="user456",
                    content="This is a sample comment.",
                    score=5,
                    replies=[
                        Mock(
                            comment_id="1011",
                            author="user789",
                            content="This is a reply to the sample comment.",
                            score=10,
                        ),
                        Mock(
                            comment_id="1213",
                            author="user789",
                            content="This is a reply to the sample comment2.",
                            score=8,
                        ),
                    ],
                )
            )
        ]

        # Create an instance of RedditPostManager
        post_manager = RedditPostManager(api_client)

        # Call the method to test
        most_upvoted_comment, most_upvoted_reply = post_manager.retrieve_post_and_most_upvoted_reply()

        # Assertions to check if the highest-scoring comment and reply are being returned
        self.assertIsNotNone(most_upvoted_comment)
        self.assertIsNotNone(most_upvoted_reply)
        self.assertEqual(most_upvoted_comment.comment_id, "789")
        self.assertEqual(most_upvoted_reply.comment_id, "1011")

if __name__ == '__main__':
    unittest.main()
