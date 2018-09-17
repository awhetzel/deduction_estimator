* Author: Aaron Whetzel
* Last Updated: 09/17/2018

## Overview

This is my first adventure with Django. It is a web app developed to
allow employers to calculate and monitor data related to employee
benefit packages.

## Downloading and Running the Application

The following instructions are for linux systems and they assume you
have Git and Python installed.

* Clone the repository from github:

`$ git clone https://github.com/awhetzel/deduction_estimator`

* Create a virtual environment

`$ python3 -m venv proj_venv`

* Activate the virtual environment

`$ source proj_venv/bin/activate`

* Install Django in the virtual environment

`(proj_venv)$ pip install django`

* Install dependency (django crispy forms)

`(proj_venv)$ pip install --upgrade django-crispy-forms`

* Move to the directory containing manage.py

`(proj_venv)$ cd deduction_estimator/mysite`

* Run the development server

`(proj_venv)$ python ./manage.py runserver`

* View the application at: http://127.0.0.1:8000/app1/

## Design Notes and Features
This application was developed based on my interpretation of a somewhat
ambiguous problem statement, so all of the design decisons were made
based on my personal interpretation of the problem.

The problem statement offers some numbers related to the cost of benefit
packages, salaries, etc. I decided that just using the values in the
statement in sort of a 'hard-coded' way would not result in a very useful
application, so I allowed for those specific numbers to be used, but they
can also be changed by a site administrator.

My solution is a two part solution: (1) a simple "quick-calculator" where
users can enter what I thought was the relevant information and see
the resulting cost of benefits and (2) a database backed solution
where approved users can view existing employees and dependents, add
new employees and dependents, delete employees and dependents, and modify
employee information.

Users cannot create new user accounts because I thought of this solution
as one that would be behind a pay wall and time did not allow for adding
payment and email confirmation features. Users can be added, removed, and
modified via the admin site that is bundled with the Django framework.The
admin site can be found at http://127.0.0.1:8000/admin

Usage of the application is pretty straightforward, but I included a 'help'
page that explains how to use the application.


## Testing
So far, I have tested this application by letting my family tinker
with it, and manually testing myself. I was interested in the Django
testing tutorials, but this was a time sensitive learning exercise so I
didn't do any TDD or automated testing.

Currently, the application has only been tested on Fedora 28 with firefox
and konqueror, I plan to test with chrome, Fedora 26, and Windows, I will
update this document when I test on other operating systems and browsers.

### Known Bugs
There are currently no known bugs in the project.


