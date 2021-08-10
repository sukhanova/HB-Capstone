# Final capstone project for Hackbright Academy


### Hackbright Academy Full-Stack Software Engineering Program

[Description goes here....]

###  Demo

 [link goes here...] 



## Tech stack:
  * Python 
  * Flask
  * Jinja
  * PostgreSQL
  * SQLAlchemy
  * HTML
  * CSS
  * Bootstrap
  * jQuery
  * Javascript
  * Cloudinary 

## Use and installation:
  While not fully deployed, you may run the app locally on your own computer.

#### Requirements:
  * PostgeSQL
  * Python 3.6.9


#### Clone or fork repository:
  ```
  $ git clone https://github.com/sukhanova/HB-Capstone
  ```

#### Set up virtual environment:
  ```
  $ pip3 install virtualenv 
  $ virtualenv env 
  $ source env/bin/activate
  ```

#### Install dependencies:
  ```
  (env) $ pip3 install -r requirements.txt
  ```
#### Make an account with [Cloudinary](https://cloudinary.com/documentation) & get an [API key](https://cloudinary.com/users/register/free).<br>

#### Store these keys in a file named 'config.py' <br> 
```
$ source config.py
```

#### With PostgreSQL, create the task_tracking database: 
```
$ createdb task_tracking
```

#### Create all tables and relations in the database
  ```
  (env) $ python3 model.py
  ```

#### Run the server on the backend
  ```
  (env) $ python3 server.py
  ```

#### Open a new browser window and visit: localhost:5000




## Keep an eye out for...
Future features may include ... 
