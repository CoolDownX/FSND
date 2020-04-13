# Introduction

This API was built to fullfill the requests from the UDACITY-Trivia game and to feed it with real data from a connected database.
Users can access different questions within five categories and submit new questions within the given categories.
The user can further delete questions and use the play mechanics which are shown within Trivia-API-game.
You will find further details on this, later in this specification.

# Getting started

To learn how to set up the local development environment, I will refer to the provided ```Readme.md```-files within the Project structure.
You can find these in: 
* ``` /frontend ```
* ```/backend ```

## Base URL

The base URL is the following: ``` http://127.0.0.1:5000/ ``` or ``` http://localhost:5000/ ```.
With this endpoint, you will only recieve a "welcome"-message and success set to ```True``` but no further data.

The response should look like this:
``` JSON
{
     "message": "Welcome! You are requesting the Trivia-API",
     "success": true
}
```

# HTTP - Responses

The API follows the typical ```HTTP``` convension of response codes.
What errors may occur while using the API, can you see in the list below.  

For further details on requesting endpoints please read through the chapter: **Endpoints**

# Errors


## 400 - Bad Request

Full error message: 
``` JSON
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
This error may occur if you send a wrong formatted request to any endpoint.


## 404 - Ressource not Found

Full error message: 
``` JSON
{
    "success": False, 
    "error": 404,
    "message": "Ressource not found"
}
```

This error may occur if you call an endpoint and refer to an ID of questions or categories which arent available in the database.


## 405 - Method not allowed

Full error message: 
``` JSON
{
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
}
```

This error may occur if you call an endpoint with the wrong request-method.


## 422 - Unprocessable

Full error message: 
``` JSON
{
    "success": False, 
    "error": 422,
    "message": "Unprocessable"
}
```

This error may occur if you try to add a new question and provide a wrong formatted JSON-Object or if the datatypes of the JSON-Content is wrong and doesnt fit into the database constraints.


## 500 - Internal Server error

Full error message: 
``` JSON
{
    "success": False, 
    "error": 500,
    "message": "Internal Server error"
}
```
This error may occur if the application is not able to connect to the database.

# Endpoints

This Chapter is about using the endpoints and provides always an example ```Curl-Request``` which is formatted to use it on ```Windows ``` and the associated JSON-Object from the response. 

Please note that all lists of questions within the response are **limited to 10** due to pagination. 
To access further data, set the ```?page=1``` - argument to another number. 

The JSON-Objects which are shown below contain only 2 entries of Lists from category and questions to keep it readable.
The real responses will contain more data.

Enough information, lets get right into the endpoints.

## GET /questions

This endpoint will provide all questions and all categories that are available in the database.

##### URL:

```/questions?page=1 ```

##### Request arguments: 

```None ```

##### Example request as curl: 
```curl -X GET http://127.0.0.1:5000/questions?page=1  ```

##### Response information: 

This endpoint will provide a JSON-Object with the following content: 
* ```categories```:  provides a simple ```list``` with all categories
* ```questions```: provides a ```list``` of all questions (Maximum 10 due to pagination) 
* ```success```: provides the success-message set to ```True```
* ```total_questions```: contains the amount of total questions over all categories as ```integer``` 

The questions and categories are ordered by ID.

##### Returned object: 

``` JSON
{
  "categories": [
    "Science",
    "Sports",
  ],
  "questions": [
    {
      "answer": "Uruguay",
      "category": 5,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },{
      "answer": "Uruguay",
      "category": 5,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
  ],
  "success": true,
  "total_questions": 19
}
```

## POST /questions (no refering URL)

This Endpoint responds with a list of matching questions from the database associated to the given ```searchTerm```.

##### URL:

```/questions?page=1 ```

##### Request arguments: 

``` JSON
{
  "searchTerm":"Replace_this_String_with_the_Search_term"
}
```

##### Example request as curl: 

```curl -X POST http://127.0.0.1:5000/questions?page=1 -H "Content-Type: application/json" -d "{\"searchTerm\":\"a\"}```


##### Response information: 

This endpoint will provide a JSON-Object with the following content: 
* ```questions```: provides the ```questions``` - object with all matching hits (Max 10) 
* ```success```: provides the success-message set to ```True```
* ```total_hits_in_database```: contains the amount of all questions which match the ```searchTerm``` as ```integer``` 

The questions are ordered by ID.

##### Returned object:  

``` JSON
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 4,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 4,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "success": true,
  "total_hits_in_database": 17
}
```

## POST /questions (with refering URL "/add")

This Endpoint creates a new insert in the database based on the given information.
I should mention, that this endpoint looks if the ```Referer``` - header contains ```/add```.

##### URL:

```/questions?page=1 ```

##### Request arguments: 

``` JSON
{
    "question":"How are you?",
    "answer":"I am good, thanks!",
    "difficulty": 1,
    "category": 2
}
```

##### Example request as curl: 
```curl -X POST http://127.0.0.1:5000/questions?page=1 -e "Any_Refering_Site_But_with:/add" -H "Content-Type: application/json" -d "{\"question\":\"How are you?\",\"answer\":\"I am good, thanks!\",\"difficulty\":1,\"category\":2}"```

##### Response information:

This endpoint will return a JSON-Object with the following content: 
* ```id```: will provide the ID of the newly created insert
* ```success```: provides the success-message set to ```True``` 

##### Returned object: 

``` JSON
{
  "id": 41,
  "success": true
}
```

## GET /categories/{category_id}/questions'


##### URL:

```/categories/{category_id}/questions ```

##### Request arguments: 

```None ```

##### Example request:
```curl -X GET http://127.0.0.1:5000/categories/1/questions?page=1  ```

##### Response information:

This endpoint will provide a JSON-Object with the following content:
* ```current_category```: provides the name of the requested category as ```String```
* ```questions```: provides a ```list``` of all questions within the choosen category (Maximum 10 due to pagination) 
* ```success```: provides the success-message set to ```True```
* ```total_questions```: contains the amount of total questions within the category as ```integer``` 
 
The questions are ordered by ID.

##### Returned object: 

``` JSON
{
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 1,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 1,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
  ],
  "success": true,
  "total_questions": 4
}
```

## GET /categories

##### URL:

```/categories ```

##### Request arguments: 

```None ```

##### Example request: 
```curl -X GET http://127.0.0.1:5000/categories```

##### Response information:

This endpoint will provide a JSON-Object with the following content:
* ```categories```: provides a simple ```list``` of all categories
* ```success```: provides the success-message set to ```True```
 
The categories are ordered by ID.

##### Returned object: 

``` JSON
{
  "categories": [
    "Science",
    "Art",
  ],
  "success": true
}
```

## DELETE /questions/{question_id}

##### URL:

```/questions/{question_id} ```

##### Request arguments: 

```None ```

##### Example request: 
```curl -X DELETE http://127.0.0.1:5000/questions/1```

##### Response information: 

This endpoint will delete the ID requested in the URL and provide a JSON-Object with the following content:
* ```id```: provides the ID of the deleted question
* ```success```: provides the success-message set to ```True```

##### Returned object: 

``` JSON
{
  "success": true,
  "id": 1
}
```

## POST /quizzes

This endpoint represents the game mechanics.
I should mention that this endpoint requires the ```quiz_category``` and a ```list``` of the previous questions, which should be excluded in the random choice. 

##### URL:

```/quizzes ```

##### Request arguments: 

Example JSON-Object to be sent to the endpoint **with no** excluded questions:

``` JSON
{
  "previous_questions": [],
  "quiz_category":
    {
      "id": 5,
      "type": "Sports"
    }
}
```

Example JSON-Object to be sent to the endpoint **with** excluded questions:

``` JSON
{
  "previous_questions": [10,11],
  "quiz_category":
    {
      "id": 5,
      "type": "Sports"
    }
}
```

##### Example request: 
```curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d "{\"previous_questions\": [10],\"quiz_category\":{\"id\": 5,\"type\": \"Sports\"}}"```

##### Response information: 

This endpoint will query all questions based on the category you choose in the request or if the category is set to ```0``` then questions out of all categories will get queried.
There will only be one question in the response and its randomized from the list of questions that fit the needs of the request.
To exclude questions from the randomizing process, mention them with the ID in the ```previous_questions``` - list.
If there are no more questions available the response will only contain the ```success``` Entry.

The response will contain the following data: 
* ```question```: provides the question-object
* ```success```: provides the success-message set to ```True```

##### Returned object: 

``` JSON
{
  "question": {
    "answer": "One",
    "category": 1,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true
}
```

