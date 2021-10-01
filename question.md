# Milestone 1

In this milestone, we'll see how to add, get, update and delete the Articles.

## ArticleHub API Specifications

Here is our specification for the API.

* **Post the Article**
* **Get all the Articles**
* **Get the Article**
* **Update the Article**
* **Delete the Article**

## Running API tests locally

To locally run the provided Postman collection against your backend, execute:

```
APIURL=http://localhost:5000/api ./run_postman_tests.sh
```

For more details, see [`run_postman_tests.sh`](run_postman_tests.sh).

### Authentication Header:

`Authorization: Token jwt.token.here`

## JSON Objects returned by API:

Make sure the right content type like `Content-Type: application/json; charset=utf-8` is correctly returned.

### Single Article

```JSON
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "image": "https://image.flaticon.com/icons/svg/2522/2522160.svg",
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "author": "Jake"
  }
}
```

### Multiple Articles

```JSON
{
  "articles":[{
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "image": "https://image.flaticon.com/icons/svg/2522/2522160.svg",
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "author": "Jake"
  }, {
    "slug": "how-to-train-your-dragon-2",
    "title": "How to train your dragon 2",
    "description": "So toothless",
    "body": "It a dragon",
    "image": "https://image.flaticon.com/icons/svg/2522/2522160.svg",
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "author": "Jane"
  }],
  "articlesCount": 2
}
```

### Errors and Status Codes

200 for Successful requests, when a request is successful

304 for Unmodified requests, when a request doesn't make any changes

401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfil the request


## Endpoints:

### Create Article

`POST /api/articles`

Example request body:

```JSON
{
  "article": {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "image": "https://image.flaticon.com/icons/svg/2522/2522160.svg",
    "author": "Jake"
  }
}
```

It will return an [Article](#single-article)

Required fields: `title`, `description`, `body`



### List Articles

`GET /api/articles`

Returns most recent articles globally by default

It will return [multiple articles](#multiple-articles), ordered by most recent first



### Get Article

`GET /api/articles/:slug`

It will return [single article](#single-article)



### Update Article

`PUT /api/articles/:slug`

Example request body:

```JSON
{
  "article": {
    "title": "Did you train your dragon?"
  }
}
```

It will return the updated [Article](#single-article)

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed



### Delete Article

`DELETE /api/articles/:slug`

It will return the [Article](#single-article)
