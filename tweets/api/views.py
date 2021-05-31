from newsfeeds.services import NewsFeedService
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import (
    TweetSerializer,
    TweetSerializerForCreate,
    TweetSerialzierForDetail,
)
from tweets.models import Tweet
from utils.decorators import required_params


class TweetViewSet(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializerForCreate

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):

        # <HOMEWORK 1> 通过某个 query 参数 with_all_comments 来决定是否需要带上所有 comments
        # <HOMEWORK 2> 通过某个 query 参数 with_preview_comments 来决定是否需要带上前三条 comments
        serializer = TweetSerialzierForDetail(
            self.get_object(),
            context={'request': request},
        )

        return Response(serializer.data)


    @required_params(params=['user_id'])
    def list(self, request, *args, **kwargs):
        """
        重载list方法，不列出所有tweets，必须指定user_id作为筛选条件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)

        # select * from twitter_tweets
        # where user_id = XXX
        # order by created_at desc
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')

        # many=True意思是返回的是一个dict类型
        serializer = TweetSerializer(
            tweets,
            context={'request': request},
            many=True,
        )
        # 一般来说json格式的response默认都要用hash格式，而不能用list格式
        return Response({'tweets': serializer.data})

    def create(self, request, *args, **kwargs):
        """
        重载create方法，因为需要默认用当前登录用户作为tweet.user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)

        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        serializer = TweetSerializer(tweet, context={'request': request})

        return Response(serializer.data, status=201)
