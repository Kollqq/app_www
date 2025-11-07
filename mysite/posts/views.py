from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        qs = Post.objects.select_related('topic', 'topic__category', 'created_by').all()
        serializer = PostSimpleSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = PostSimpleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        obj = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"detail": "Nie znaleziono wpisu."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSimpleSerializer(obj)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PostSimpleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
