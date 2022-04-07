# inorg
A functionality focused social networking site, with concentration on how it works and why it works

## Structure and functionalities

This project is crud focused with implementation of crud in various aspect of it, almost all it's functionalities are crud based and it uses Django generic class based views for it's views [ `from django.views import Views` ] which makes the work more plain, redable and makes it's assessing method super clear.

The project houses various functionalities with the base of it being:

- Sharing a post

The post shared has its full CRUD functionality for the creator user only, meaning he can Create a post, Read his posts in his profile, Update his post and Delete his posts.

- Comment and Replies

Every registered user can share a comment on the post and another user can as well replied the comments, this comments also has their full CRUD functionality taken care of.

- Like and Dislike

A registered user can like a post and dislike a post, but he can not like and dislike a post at the same time [ permissions taken care of ]

- User Profile

A profile is created for a user automatically after signing up, this is achieved with the use of `Django signals` which take the User model as sender and the profile creation function as receiver.

- Messaging

The messaging functionality is taken care of and is done with just CRUD, a user can message another user and the messaged user can reply or respond to his messages.

- Notifications

The Notification module of the project take care of notifying a user once he has a new message, someone liked his post or someone commented on one of his posts, this way, each user can easily find what's going on in his space.

- Use of context processors

Context processors were used to share number of comments and new messages to the navbar.


## Test the site

A like has been shared up there as the site is currently running on Heroku.

## Run this project

This project can be run on your local machine and you can as well improve it by cloning or downloading this repo, once that is done change directory into the project folder and make sure your current directory is the directory that houses `manage.py` then run `pip install -r requirements.txt` to install project dependencies, however you'll need to generate new `secret key` and set `Debug= True` in the `settings.py` file in other to run this project.
 
