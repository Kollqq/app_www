# Lab 8 – zadania GraphQL

## 1. Podstawowe zapytania

### 1.1 Wszystkie kategorie

```graphql
query {
  allCategories {
    id
    name
    description
  }
}
```

### 1.2 Pojedyncza kategoria po ID

```graphql
query {
  categoryById(id: 1) {
    id
    name
    description
  }
}
```

### 1.3 Wszystkie tematy

```graphql
query {
  allTopics {
    id
    name
    created
    category {
      id
      name
    }
  }
}
```

### 1.4 Pojedynczy temat po ID

```graphql
query {
  topicById(id: 1) {
    id
    name
    created
    category {
      id
      name
      description
    }
  }
}
```

### 1.5 Wszystkie posty

```graphql
query {
  allPosts {
    id
    title
    text
    slug
    createdAt
    updatedAt
    topic {
      id
      name
      category {
        id
        name
      }
    }
    createdBy {
      id
      username
    }
  }
}
```

### 1.6 Post po ID

```graphql
query {
  postById(id: 1) {
    id
    title
    text
    slug
    createdAt
    updatedAt
    topic {
      id
      name
    }
    createdBy {
      id
      username
    }
  }
}
```

### 1.7 Wyszukiwanie postów po fragmencie tytułu (`q`)

```graphql
query {
  allPosts(q: "django") {
    id
    title
    slug
  }
}
```

---

## 2. Dodatkowe resolvery

### 2.1 Kategorie zawierające fragment nazwy (`categoriesByName`)

```graphql
query {
  categoriesByName(substr: "dev") {
    id
    name
    description
  }
}
```

### 2.2 Tematy zawierające fragment nazwy (`topicsByName`)

```graphql
query {
  topicsByName(substr: "python") {
    id
    name
    created
    category {
      id
      name
    }
  }
}
```

### 2.3 Liczba postów danego użytkownika (`postsCountByUser`)

```graphql
query {
  postsCountByUser(userId: 1)
}
```

---

## 3. Mutacje dla modelu `Post`

### 3.1 Tworzenie posta (`createPost`)

```graphql
mutation {
  createPost(
    title: "Nowy post z GraphQL"
    text: "Treść posta utworzonego przez mutację."
    slug: "nowy-post-graphql"
    topicId: 1
    createdById: 1
  ) {
    post {
      id
      title
      slug
      createdAt
      topic {
        id
        name
      }
      createdBy {
        id
        username
      }
    }
  }
}
```

### 3.2 Edycja posta (`updatePost`)

```graphql
mutation {
  updatePost(
    id: 1
    title: "Zaktualizowany tytuł posta"
    text: "Zmieniona treść posta."
    slug: "zaktualizowany-tytul-posta"
  ) {
    post {
      id
      title
      text
      slug
      updatedAt
      topic {
        id
        name
      }
    }
  }
}
```

### 3.3 Usuwanie posta (`deletePost`)

```graphql
mutation {
  deletePost(id: 1) {
    ok
  }
}
```
