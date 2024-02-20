
# Note-Taking Application

A RESTful API for a simple note-taking application. The API will allow users to register , login for perform basic CRUD operations (Create, Read, Update, Delete) on notes moreover users can also share thier notes with other users


## Features

- User Registration and Login :
   
   Users can create thier account by providing their name, email, and password. After registration, they can log in to the application everytime using their email and password

- JWT Authentication :

  The application ensures the api is well secured and protected by using JWT (JSON Web Tokens) for authentication. Upon successful login, the server generates a JWT token containing the user's ID and expiration time. This token is required while accessing all other api.

- CRUD operations on notes :

   Authenticated users can Create and view a new note, Retrieve a specific note by its ID, Update an existing note and the admin of the note can delete his note

- Sharing Notes with other users :

  Users can share their notes with other users by specifying the email of the user they want to share the note with. The server verifies the ownership of the note and the existence of the recipient user before allowing the note to be shared.

- Version History :

  Users can view the version history of a note, including details such as the last updated time and the user who made the last update.

- validation and sanitization :

  All the input data from various api request is validated upon different criteria and even used bleach module to Sanitize input data to remove potentially malicious content or escape special characters

 

- Logging and Monitoring:

   Implemented application.log file for logging and monitoring to track and analyze API activity for suspicious behavior or security incidents


## API Reference

#### User Registration

```http
  POST /register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. user name |
| `email` | `string` | **Required**. user email address |
| `password` | `string` | **Required**. user password |

sample request json :

{

    "name":"nihalc",
    "email": "nihalc@gmail.com",
    "password": "Abcd828"
}

sample response json :

{

    "message": "User registered successfully, Please login to continue."
}


#### User Login


```http
  POST /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. input registered email |
| `password` | `string` | **Required**. input registered password |

sample request json :

{

    "email": "nihalc@gmail.com",
    "password": "Abcd828"
}

sample response json :

{

    "Message": "Login Successfull",
    "token": "eyJhbGciOiCI6IkpXVCJ9.eyJ1TV9.v03QrP5pKo3y_DEWd-5Ococ"
}



#### Create a new note.


```http
  POST /notes/create
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token for request authorization|
| `noteTitle` | `string` | **Required**. provide the topic for note |
| `noteText` | `string` | **Required**. provide the content for note |

sample request json :

{

    "noteTitle": "Meeting",
    "noteText": "Teach team standup meeting to held tommorow "
}

sample response json :

{
    
    "message": "Note created successfully."
}


#### Share the note with other users


```http
  POST /notes/share
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token for request authorization|
| `noteid` | `Integer` | **Required**. provide the id of the note which you want to share |
| `email` | `string` | **Required**. provide email of the user whom you want to share |

sample request json :

{

    "noteid": "1",
    "email": "nihal@gmail.com"
}

sample response json :

{
    
    "message": "Note shared successfully."
}


#### Retrieve a specific note by its ID


```http
  GET /notes/<int:id>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. parse the note id in param |
| `Authorization` | `string` | **Required**. JWT token for request authorization|


#### Update an existing note.


```http
  PUT /notes/<int:id>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. parse the note id in param |
| `Authorization` | `string` | **Required**. JWT token for request authorization|
| `noteText`      | `string` | **Required**. input the notetext you want to update |




#### GET all the changes associated with the note


```http
  GET /notes/version-history/<int:id>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. parse the note id in param |
| `Authorization` | `string` | **Required**. JWT token for request authorization|






## Run Locally

Clone the project

```bash
  git clone https://github.com/Muhammadnihalc/Note-Taking-Application
```

create your virtual environment and activate

```bash
  python -m venv venv
  venv\Scripts\activate

```

Install dependencies

```bash
  pip install -r requirements.txt

```

Start the server

```bash
  set FLASK_APP = app.py
  flask run

  Running on http://127.0.0.1:5000

```

