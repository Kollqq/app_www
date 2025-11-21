from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .authentication import BearerTokenAuthentication
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSimpleSerializer


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        qs = Category.objects.all()
        serializer = CategorySerializer(qs, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        obj = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"detail": "Nie znaleziono kategorii."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(obj)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_search_by_name(request, query):
    qs = Category.objects.filter(name__icontains=query)
    serializer = CategorySerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
def category_topics(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"detail": "Nie znaleziono kategorii."}, status=status.HTTP_404_NOT_FOUND)

    qs = Topic.objects.filter(category=category)
    serializer = TopicSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        qs = Topic.objects.select_related('category').all()
        serializer = TopicSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def topic_detail(request, pk):
    try:
        obj = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response({"detail": "Nie znaleziono tematu."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(obj)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TopicSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def topic_search_by_name(request, query):
    qs = Topic.objects.filter(name__icontains=query).select_related('category')
    serializer = TopicSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def category_permission_test(request, pk):
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied("Brak uprawnienia view_category.")

    try:
        obj = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"detail": "Nie znaleziono kategorii."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(obj)
    return Response(serializer.data)

class PostListAPIView(APIView):
    def get(self, request):
        qs = Post.objects.select_related('topic', 'topic__category', 'created_by').all()
        q = request.query_params.get('q')
        if q:
            qs = qs.filter(title__icontains=q)

        serializer = PostSimpleSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSimpleSerializer(data=request.data)
        if serializer.is_valid():
            author = request.user if request.user.is_authenticated else User.objects.first()
            serializer.save(created_by=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Nie znaleziono wpisu."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSimpleSerializer(obj)
        return Response(serializer.data)

class PostUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Nie znaleziono wpisu."}, status=status.HTTP_404_NOT_FOUND)

        if obj.created_by != request.user:
            if not request.user.has_perm('posts.can_edit_others_posts'):
                return Response(
                    {"detail": "Brak uprawnień do edycji cudzego posta."},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = PostSimpleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteAPIView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"detail": "Nie znaleziono wpisu."}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    if request.method == 'GET':
        qs = Post.objects.filter(created_by=request.user)
        serializer = PostSimpleSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = PostSimpleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
