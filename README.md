# Sport Club App

How can a sports club allow customers to smoothly enroll in the classes it offers? This is the problem this application aims to solve. It allows users to register for different sports classes, and the admins can, in turn, view who has registered for which classes.

Here's a more detailed description of the app's functionalities:
- Users can sign up, log in, and log out.
- On the front page, users see the different classes offered by the club.
- Users can read a description of each available class.
- Users can register for one or more of the available classes.
- Users can cancel their enrollments.
- Users can view all the classes for which they have enrolled.
- Users can leave comments about the classes.
- Admins can create and remove sports classes.
- Admins can view who has registered for the club's classes.
- Admins can remove individuals from the classes.

## Testing the App

The app can be tested at the following URL: [https://database-app-project-patient-surf-6165.fly.dev/](https://database-app-project-patient-surf-6165.fly.dev/)

Note that when opening the URL, the app might take quite a bit of time to load since the machines running it will go idle if not used for one hour. Additionally, when the app resumes from idling, it is possible that you get an Internal Server Error in the beginning. If this happens, simply refresh the page and move on. The server sometimes seems to get overloaded when it leaves the idle state.

Once the page has loaded, you will be presented with a login screen. To test the admin functionalities of the app, the user can log into an admin account with the following credentials:
- username: admin
- password: keepsecret

The admin can create new classes by clicking on the green button at the index page. He can also delete any class by clicking on a class, and then pressing the red deletion button. On class pages he can also view and cancel enrollments as well as delete comments .

At any time, the user can go back to the index page by clicking on "Sporttimonnit" in the navbar. From the index, the admin can also view all members of the club clicking on the blue button. From there, the admin has the possiblity to remove any member, which will erase all data related to that account, and the user will no longer be able to log in.

There are also 3 premade user accounts that can be used to test the app's functionalities on normal users. They use the following credentials:

|  username  |     password     |
| ---------- | ---------------- |
| smartboyXZ | foobar           |
| IidaLOL    | oleniidahehe     |
| aku964     | oispajoperjantai |

Regular users can view the description for any class by selecting a class from the index page. At the class description page, the user can enroll or cancel the enrollment fo that class. He can also leave comments, and delete his own comments.

In the navbar, there is a link from which the user can view all courses for which he has registered.

Instead of using one of the premade accounts, a user can of course create his own account by clicking on the registration button presented at the index page when no one is logged in. The password provided during registration will have to be at least 6 characters long.
