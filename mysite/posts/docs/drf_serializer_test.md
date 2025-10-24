## Importy wspólne

```python
from posts.models import Category, Topic
from posts.serializers import TopicSerializer, PostSimpleSerializer

from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


# 1) TopicSerializer — ModelSerializer

# 1.1. Stworzenie nowego obiektu modelu (opcjonalne) i utrwalenie w DB


cat, _ = Category.objects.get_or_create(
    name="Programming",
    defaults={"description": "All about IT"}
)

topic = Topic(name="Django", category=cat)
topic.save()



# 1.2. Inicjalizacja serializatora i podgląd danych natywnych (dict)


serializer = TopicSerializer(topic)
serializer.data
# przykładowy output:
# {'id': 1, 'name': 'Django',
#  'category': {'id': 1, 'name': 'Programming', 'description': 'All about IT'},
#  'created': '...'}


# 1.3. Serializacja do formatu JSON (bytes)


content = JSONRenderer().render(serializer.data)
content
# b'{"id":1,"name":"Django","category":{"id":1,"name":"Programming","description":"All about IT"},"created":"..."}'


# 1.4. Parsowanie JSON (bytes) → dict


stream = io.BytesIO(content)
data = JSONParser().parse(stream)
data
# {'id': 1, 'name': 'Django',
#  'category': {'id': 1, 'name': 'Programming', 'description': 'All about IT'},
#  'created': '...'}


# 1.5. Deserializacja danych wejściowych (payload z klienta) i walidacja


payload = {"name": "Django REST", "category_id": cat.id}
deserializer = TopicSerializer(data=payload)
deserializer.is_valid()         # -> True/False
deserializer.errors             # -> słownik błędów (jeśli są)
# podejrzenie pól
deserializer.fields             # lub repr(deserializer)
deserializer.validated_data     # -> OrderedDict([('name','Django REST'), ('category', <Category ...>)])


# 1.6. Zapis do bazy


topic2 = deserializer.save()
TopicSerializer(topic2).data
# {'id': 2, 'name': 'Django REST',
#  'category': {'id': 1, 'name': 'Programming', 'description': 'All about IT'},
#  'created': '...'}


# 2) PostSimpleSerializer — ręczny Serializer


# 2.1. Przygotowanie użytkownika oraz danych


User = get_user_model()
user = User.objects.first() or User.objects.create_user(username="lab_user", password="lab_pass")

# upewnijmy się, że mamy jakiś topic:
topic = Topic.objects.first() or Topic.objects.create(name="Intro", category=cat)

post_input = {
    "title": "Testowy post",
    "text": "To jest przykładowa treść posta.",
    "slug": "testowy-post",
    "topic_id": topic.id,
}


# 2.2. Inicjalizacja serializatora, walidacja i podejrzenie błędów


serializer = PostSimpleSerializer(data=post_input)
serializer.is_valid()       # -> True/False
serializer.errors           # -> słownik błędów (jeśli są)
serializer.fields           # lub repr(serializer) — jak zdefiniowane są pola
serializer.validated_data   # -> dane po walidacji (OrderedDict(...))


# 2.3. Zapis obiektu (create) — przekazujemy created_by_id


post = serializer.save(created_by_id=user.id)
serializer.data
# {'id': ..., 'title': 'Testowy post', 'text': 'To jest przykładowa treść posta.',
#  'slug': 'testowy-post', 'topic_id': topic.id, 'created_by_id': user.id,
#  'created_at': '...', 'updated_at': '...'}


# 2.4. Serializacja do JSON (bytes) i ponowna deserializacja


content = JSONRenderer().render(serializer.data)
content
# b'{"id":...,"title":"Testowy post","text":"To jest przykładowa treść posta.","slug":"testowy-post",...}'

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
data
# {'id': ..., 'title': 'Testowy post', 'text': 'To jest przykładowa treść posta.',
#  'slug': 'testowy-post', 'topic_id': ..., 'created_by_id': ...,
#  'created_at': '...', 'updated_at': '...'}


# 2.5. Aktualizacja (partial update) i ponowna serializacja


patch_input = {"title": "Zmieniony tytuł"}
deserializer = PostSimpleSerializer(instance=post, data=patch_input, partial=True)
deserializer.is_valid()     # -> True/False
deserializer.errors
post = deserializer.save()
deserializer.data
# {'id': ..., 'title': 'Zmieniony tytuł', 'text': 'To jest przykładowa treść posta.',
#  'slug': 'testowy-post', 'topic_id': topic.id, 'created_by_id': user.id,
#  'created_at': '...', 'updated_at': '...'}
