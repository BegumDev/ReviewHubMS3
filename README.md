1. Purpose of the project
2. user stories
3. Features
4. future features
5. Typography and color scheme
6. wireframes
7. Technology
8. testing
   8.1 code validations
   8.2 test cases (user story based with screenshots)
   8.3 fixed bugs
   8.4 supported screens and browsers
9. Deployment
   9.1 via gitpod
   9.2 via github pages
10. credits

<h1 align="center">Review Hub</h1>

[View the live project here] 

![Image of the website on desktop, laptop, tablet and mobile]

### This project is a fictational reviews website to enable users to create, read, update and delete their reviews on one platform.

## User Experience (UX)
***
- ### User stories
    - #### Visitor goals:
        1. I want to be able to log in and delete any of my reviews.
        2. I want to create my own reviews on the website.
        3. I want to be able to receive feedback on my progress when creating or deleting content.

- ### Design
    * #### Color Scheme
        -  
    * #### Typography
        - 
    * #### Imagery
        1. 
        2. 
        3. 

- ### Wireframes
    <details><summary>Main Page Wireframe:</summary>

    ![Main Page Wireframe](reviewhub/static/images/readme-images/wireframes/main-page-wireframe.JPG)
    </details>

    <details><summary>My Account Wireframe:</summary>

    ![My Account Wireframe](reviewhub/static/images/readme-images/wireframes/my-account-wireframe.JPG)

    </details>

## Features
***
* ### Current Features
    1. Logging In
    2. Admin can add or delete reviews (related db will also delete reviews with it.)
    3. My account has own reviews in it where you can edit and delete.
    4. Log out.
    5. Populates all reviews on main page.
    
* ### Future Features
    1. Edit own details and delete own account.

    
        
## Technologies Used
***
* ### Languages Used
    * Frontend;
        - HTML, CSS, jQuery.
    * Backend;
        - Python
* ### Development Tools.
    * Github.
        - Used to store the projects after being pushed using Git.
    * Gitpod.
        - Hosts the coding workspace.
    * Heroku.
        - Cloud platform for deploying the app.

### Frameworks, Libraries & Programs Used
* MaterialzeCSS.
    - Used for responsiveness.
* Flask.
    - A web-framework app responsible to render templates.
* Balsamiq
    - Used to create wireframes of the website.
* Jinja.
    - Template language for python for easy creation of backend code through to the frintend.
* Werkzeug Security.
    - Used for password hashing and password authorisation.

### Database structure.
* PostgreSQL.
    - Storage for relational data to implement CRUD functionality.


## Testing
***
* ### Testing user stories from user experience (UX).
    * #### Aim 1 - I want to be able to log in and delete any of my reviews.
        - Once a logged in, a user can;
            1. Click on my account.
            2. All their own reviews are visible on their account page.
            3. Buttons are accessible to delete straight from the same page.
            4. Once clicked a modal will pop up.
            5. Click yes will confirm deletion and clicking no will return them back.

    * #### Aim 2 -I want to create my own reviews on the website.
        - Once a logged in, a user can;
            1. Click on 'add a review' in their menu tab.
            2. Users will be guided to a form to add a review.
            3. Once filled out and submitted; the users review will pop up on the main website page aswell as their own.
    
    * #### Aim 3 - I want to be able to receive feedback on my progress when creating or deleting content.
        - Logging out;
            1. When the user logs out, a flash message will appear at the top of the page confirming they are logged out.
        - Deleting a review;
            1. Users click on the delete button.
            2. This will throw up a modal to confirm if they want to proceed or not.
            3. 
        
* ### Code validation.
    1. Admin unable to delete reviews.
        - Fix:
            - Add to the line of code where; those who created the review can delete it - by enbaling the admin to do so aswell.
    * 
    * 

* ### Supported screens and browsers.
    * 
    * 
    * 
    

* ### Fixed bugs.
    * 
    * 
    * 
    


## Deployment
***
1. Working with a local copy.
    - PSQL
2. Deploying to Heroku.
    - Add PostgreSQL to the Heroku app. Create db...


## Credits
***
* ### Code


* ### Content


* ### Media


* ### Acknowledgements
