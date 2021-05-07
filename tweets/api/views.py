from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetCreateSerializer
from tweets.models import Tweet


class TweetViewSet(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

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

        serializer = TweetSerializer(tweets, many=True)
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

        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            },status=400)

        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data,status=201)
