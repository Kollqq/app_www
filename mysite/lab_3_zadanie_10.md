>>> Category.objects.all()

<QuerySet \[<Category: Test\_Cat>, <Category: Zabawki>]>



>>> Category.objects.get(id=3)

<Category: Test\_Cat>



>>> Category.objects.filter(name\_\_istartswith='T')

<QuerySet \[<Category: Test\_Cat>]>



>>> Topic.objects.values\_list('category\_\_name', flat=True).distinct()

<QuerySet \['Zabawki', 'Test\_Cat']>



>>> Post.objects.order\_by('-title').values\_list('title', flat=True)

<QuerySet \['Test\_Title', 'Post\_about\_nothing', 'New\_Post']>



>>> Category.objects.create(name='Nowa kategoria', description='Opis opcjonalny')

<Category: Nowa kategoria>

