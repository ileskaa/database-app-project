# Sport Club App

How can a sports club allow customers to smoothly enroll in the classes it offers? This is the problem this application aims to solve. It allows users to register for different sports classes, and the admins can, in turn, view who has registered for which classes.

Here's a more detailed description of the app's functionalities:
- Users can sign up, log in, and log out.
- On the front page, users see the different classes offered by the club.
- Users can read a description of each available class.
- Users can register for one or more of the available classes.
- Users can cancel their enrollments if the classes have not yet started.
- Users can view all the classes for which they have enrolled.
- Admins can create and remove sports classes.
- Admins can view who has registered for the club's classes.
- Admins can remove individuals from the classes.

## Running the app locally

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

Moreover, the following environment variables must be set in your `.env` file:  
DATABASE_URL  
SECRET_KEY

Note: it is recommended you create a separate database when testing this app. The DATABASE_URL within your .env should then point to that databae.

Initialize the database tables by running `psql -f sql/init_db.sql`
