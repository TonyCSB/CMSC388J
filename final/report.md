# Secret Santa Gift Exchange

## Member

- Sibei Chen

## Link

[https://cmsc388j.tonychen.page](https://cmsc388j.tonychen.page)

## Requirements

### Registration & Login

`flask_app/users/routes.py`

User needs to register an account to post and exchange gifts. Password requirements are being enforced by js in frontend and python in backend. Passwords are saved in hashes.

### Forms

`flask_app/forms.py`

Forms are as follows:

1. Registration Form
2. Login Form
3. Request Gift Form
4. Update Tracking Form
5. Comment Form

### Database

`flask_app/__init__.py`

MongoDB is used for storing all data.

### Security

`flask_app/__init__.py`

Talisman and CSRF are used to protect the website. CSP is used to control content security.

### Blueprints

`flask_app/users/routes.py`

1. [Login Page](https://cmsc388j.tonychen.page/user/login)
2. [Register Page](https://cmsc388j.tonychen.page/user/register)
3. [Account Detail Page](https://cmsc388j.tonychen.page/user/account)

`flask_app/gifts/routes.py`

1. [Gift Request Page](https://cmsc388j.tonychen.page/request)
2. [Gift Matched Selection Page (Needs Gift ID in Link)](https://cmsc388j.tonychen.page/matched/<id>)
3. [Gift Detail Page (Needs Gift ID in Link)](https://cmsc388j.tonychen.page/gift/detail/<id>)

### Presentation/Appearance

Bootstrap is used in all pages.

### Use of new Python package

`flask_app/forms.py`

`flask_app/templates/giftdetail.html`

`Flask-Pagedown` and `Flask-Markdown`, they are used in gift detail page to submit and display comment in Markdown format.

### Evidence of Usage

Create an account and make a wish. I have already created dummy account with wish list entered. You will be matched with a secret santa, and in account detail page, you will be able to experience all the process within the gift exchange process.

## Changes from the Proposal

Originally planned to allow users to post images and display on the front page. The plan was discarded due to the excess amount of work involved.
