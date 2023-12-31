# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import reddit_pb2 as reddit__pb2


class RedditServiceStub(object):
    """Service definitions
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePost = channel.unary_unary(
                '/reddit.RedditService/CreatePost',
                request_serializer=reddit__pb2.CreatePostRequest.SerializeToString,
                response_deserializer=reddit__pb2.PostResponse.FromString,
                )
        self.VotePost = channel.unary_unary(
                '/reddit.RedditService/VotePost',
                request_serializer=reddit__pb2.VotePostRequest.SerializeToString,
                response_deserializer=reddit__pb2.VoteResponse.FromString,
                )
        self.GetPost = channel.unary_unary(
                '/reddit.RedditService/GetPost',
                request_serializer=reddit__pb2.GetPostRequest.SerializeToString,
                response_deserializer=reddit__pb2.PostResponse.FromString,
                )
        self.CreateComment = channel.unary_unary(
                '/reddit.RedditService/CreateComment',
                request_serializer=reddit__pb2.CreateCommentRequest.SerializeToString,
                response_deserializer=reddit__pb2.CommentResponse.FromString,
                )
        self.VoteComment = channel.unary_unary(
                '/reddit.RedditService/VoteComment',
                request_serializer=reddit__pb2.VoteCommentRequest.SerializeToString,
                response_deserializer=reddit__pb2.VoteResponse.FromString,
                )
        self.TopComments = channel.unary_unary(
                '/reddit.RedditService/TopComments',
                request_serializer=reddit__pb2.TopCommentsRequest.SerializeToString,
                response_deserializer=reddit__pb2.TopCommentsResponse.FromString,
                )
        self.ExpandCommentBranch = channel.unary_unary(
                '/reddit.RedditService/ExpandCommentBranch',
                request_serializer=reddit__pb2.ExpandCommentBranchRequest.SerializeToString,
                response_deserializer=reddit__pb2.ExpandCommentBranchResponse.FromString,
                )
        self.MonitorUpdates = channel.unary_stream(
                '/reddit.RedditService/MonitorUpdates',
                request_serializer=reddit__pb2.MonitorUpdatesRequest.SerializeToString,
                response_deserializer=reddit__pb2.UpdateResponse.FromString,
                )


class RedditServiceServicer(object):
    """Service definitions
    """

    def CreatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VotePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateComment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VoteComment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TopComments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExpandCommentBranch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MonitorUpdates(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RedditServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePost,
                    request_deserializer=reddit__pb2.CreatePostRequest.FromString,
                    response_serializer=reddit__pb2.PostResponse.SerializeToString,
            ),
            'VotePost': grpc.unary_unary_rpc_method_handler(
                    servicer.VotePost,
                    request_deserializer=reddit__pb2.VotePostRequest.FromString,
                    response_serializer=reddit__pb2.VoteResponse.SerializeToString,
            ),
            'GetPost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPost,
                    request_deserializer=reddit__pb2.GetPostRequest.FromString,
                    response_serializer=reddit__pb2.PostResponse.SerializeToString,
            ),
            'CreateComment': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateComment,
                    request_deserializer=reddit__pb2.CreateCommentRequest.FromString,
                    response_serializer=reddit__pb2.CommentResponse.SerializeToString,
            ),
            'VoteComment': grpc.unary_unary_rpc_method_handler(
                    servicer.VoteComment,
                    request_deserializer=reddit__pb2.VoteCommentRequest.FromString,
                    response_serializer=reddit__pb2.VoteResponse.SerializeToString,
            ),
            'TopComments': grpc.unary_unary_rpc_method_handler(
                    servicer.TopComments,
                    request_deserializer=reddit__pb2.TopCommentsRequest.FromString,
                    response_serializer=reddit__pb2.TopCommentsResponse.SerializeToString,
            ),
            'ExpandCommentBranch': grpc.unary_unary_rpc_method_handler(
                    servicer.ExpandCommentBranch,
                    request_deserializer=reddit__pb2.ExpandCommentBranchRequest.FromString,
                    response_serializer=reddit__pb2.ExpandCommentBranchResponse.SerializeToString,
            ),
            'MonitorUpdates': grpc.unary_stream_rpc_method_handler(
                    servicer.MonitorUpdates,
                    request_deserializer=reddit__pb2.MonitorUpdatesRequest.FromString,
                    response_serializer=reddit__pb2.UpdateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'reddit.RedditService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RedditService(object):
    """Service definitions
    """

    @staticmethod
    def CreatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/CreatePost',
            reddit__pb2.CreatePostRequest.SerializeToString,
            reddit__pb2.PostResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VotePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/VotePost',
            reddit__pb2.VotePostRequest.SerializeToString,
            reddit__pb2.VoteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/GetPost',
            reddit__pb2.GetPostRequest.SerializeToString,
            reddit__pb2.PostResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/CreateComment',
            reddit__pb2.CreateCommentRequest.SerializeToString,
            reddit__pb2.CommentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VoteComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/VoteComment',
            reddit__pb2.VoteCommentRequest.SerializeToString,
            reddit__pb2.VoteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TopComments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/TopComments',
            reddit__pb2.TopCommentsRequest.SerializeToString,
            reddit__pb2.TopCommentsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExpandCommentBranch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/reddit.RedditService/ExpandCommentBranch',
            reddit__pb2.ExpandCommentBranchRequest.SerializeToString,
            reddit__pb2.ExpandCommentBranchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MonitorUpdates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/reddit.RedditService/MonitorUpdates',
            reddit__pb2.MonitorUpdatesRequest.SerializeToString,
            reddit__pb2.UpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
