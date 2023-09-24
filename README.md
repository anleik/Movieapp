# Movieapp

## Functionality:  
Users can:  
* create an account   
* login/logout  
* review movies (text and rating) 
* browse other users' reviews  
* like or dislike other users' reviews  


## Instructions  
Clone the repository and move to it's root directory  
Create a .env file and fill in these variables:  
```
DATABASE_URL=<database-local-path>
SECRET_KEY=<secret-key>
```
  
Activate virtual environment and install dependencies with the commands:  
```
$ python3 -m venv venv  
$ source venv/bin/activate  
$ pip install -r ./requirements.txt  
```

Use the database schema:  
```
$ psql < schema.sql
```
Launch the app with:  
```
$ flask run  
```
  
## Goals  
Users can:
* create an account
* login/logout  
* review movies (text and rating) 
* edit/update their reviews 
* browse other users' reviews
* like or dislike other users' reviews
* change like to dislike and vice versa  

Admins can:
* add new movies
* delete reviews


