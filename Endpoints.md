# Project Endpoints
Endpoints for the Restaurants Review website using Django's Rest Framework, PostgreSQL and React

## The Website has the following Endpoints

### 1. Registration
- POST: Register new user by asking for an email (send email validation code) 
```/api/registration/```
- POST: Validate a new registered user with validation code sent by email
```/api/registration/validation/ ```

### 2. Auth
- POST: Get a new JWT by passing username and password.
```/api/auth/token/  ```
- POST: Get a new JWT by passing an old still valid JWT. 
```/api/auth/token/refresh/ ```
- POST: Verify a token by passing the token in the body 
```/api/auth/token/verify/ ```
-  POST: Reset users password by sending a validation code in a email
```/api/auth/password-reset/ ```
- POST: Validate password reset token and set new password for the user.
```/api/auth/password-reset/validate/```

### 3. Search
- POST: Search a comment by keyword in body, example:/api/comments/search/?search=<keyword in body>
```/api/comments/search```
- POST: Search a Restaurant by name, category, city, country
```/api/restaurants/search```
- POST: Search a User by username, first name, last name, email
```/api/users/search```

### 4. Comments
- GET: get all Comments or create a new Comment for a Restaurant
 ```/api/comments/``` 
 - GET/PUT/DELETE: Get or update or delete a Comment by id
```/api/comments/<int:pk>/``` 
- GET: get all the Comments by a specific User in chronological order
```/api/comments/user/<int:user_id>/```
- POST/DELETE: post or delete a like from a Comment
```/api/comments/reaction/<comment_id>```
- GET: get all Reactions on Comments
```/api/comments/reactions/```

### 5. Restaurants
- GET/POST: get the list of all Restaurants or create a new Restaurant 
 ```/api/restaurants/``` 
- GET/PUT/DELETE: get or update or delete a Restaurant by id
```/api/restaurants/<int:pk>/``` 
- GET: get all the categories  of the Restaurants
```/api/restaurants/categories/<str:category>/```
- GET: get all the Restaurants by specific category 
```/api/restaurants/categories/<str:category>/```
- GET: get all the Restaurants by owner
```/api/restaurants/user/<int:user_id>/```

### 6. Users
- GET: get all the Users
 ```/api/users/``` 
- GET: get all User Profiles 
```/api/users/profiles``` 
- GET/UPDATE: get or update the loged in User's Profile 
```/api/users/me/```
- GET: get a specific User  Profile by user_id
```/api/users/<int:pk>//```
