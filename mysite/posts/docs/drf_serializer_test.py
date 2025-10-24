from posts.serializers import TopicSerializer, PostSimpleSerializer
from posts.models import Category
from django.contrib.auth.models import User

cat = Category.objects.create(name="Programming", description="All about IT")

topic_data = {"name": "Django REST", "category_id": cat.id}
topic_ser = TopicSerializer(data=topic_data)
topic_ser.is_valid(raise_exception=True)
topic = topic_ser.save()
print("Topic:", topic_ser.data)

user = User.objects.first()
post_data = {
    "title": "DRF Intro",
    "text": "Pierwszy post o Django REST Framework",
    "slug": "drf-intro",
    "topic_id": topic.id,
}
post_ser = PostSimpleSerializer(data=post_data)
post_ser.is_valid(raise_exception=True)
post = post_ser.save(created_by_id=user.id)
print("Post:", post_ser.data)
