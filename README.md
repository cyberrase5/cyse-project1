# Cyber Security Base Project I
Course project for Cyber Security Base with 5 vulnerabilites as per the assignment

### Starting up
In project root
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py runserver

### User Guide
A simple Twitter/X -style app, where you can leave messages for everyone to see. There are two kinds of users, normal and admin users. Everyone can send messages, but only admins can remove them. I think you can figure out the rest.

Start the app at http://127.0.0.1:8000/chat/

No logging out because I'm lazy lol

## The 5 Vulnerabilities
I've chosen the 2017 list https://owasp.org/www-project-top-ten/2017/Top_10 plus CSRF, as it's allowed in the assignment

### A1:2017-Injection
https://github.com/cyberrase5/cyse-project1/blob/master/chat/views.py#L39 (and the couple of lines below)

#### Description
Before creating an account, the server checks whether an account with this name already exists, because Django handles the situation by giving an error page, not very elegant. If an account already exists, the registration page is rendered again with a helpful red error message, including the attempted name (pulled from the database!). The query string is constructed unsafely, which makes the app vulnerable to SQL injections.

#### Test it yourself
First, create an account, the details don't matter, just remember the username. Now try to create an account with the same name, and you'll get an error message "Username [({chosen_name},)] already in use". Because the query is unsafe and the entire SQL response is given to the message, finding the correct text to input as username will result in data leaking. You can try to figure it out yourself or check it below:
<details>
  <summary>Spoiler warning</summary>
  
  {chosen_name}' UNION SELECT password FROM auth_user --
  
</details>
Now create an account with the malicious "username", and this time you will not only get the username but also the list of all the passwords hashed. While the passwords are hashed, the leak is still pretty bad. 

#### Fixing it
Link here\
The main fix is parameterized queries. Also fetchall() has been changed to fetchone() and in the return render command response[0] is used as additional security, so that even if the response contained passwords, only the first one would be leaked. Now test the fixed version. Comment the code between the comments BEGIN and END BROKEN VERSION and uncomment the FIXED VERSION one and test the previous injection, it doesn't work.

### A5:2017-Broken Access Control
https://github.com/cyberrase5/cyse-project1/blob/master/chat/views.py#L66

#### Description
The app has admin and regular users with different privileges. Admins have their own page, where they can delete messages and view logs, and this page should be accessed only by admins. Try logging in as admin and regular user, you'll see that regular users don't have the admin page button. However, since the backend doesn't check whether the user is admin or not, you can access the admin view as a regular user if you can find the URL for it. This needs to be fixed.\
(NOTE: I know that you can't delete posts as regular user because it has the decorator, but I left it there because it's needed later)

#### Test it yourself
Login as user and navigate to http://127.0.0.1:8000/chat/admin/ As mentioned above, you can't do other admin stuff than view the log (more on that later), but I think you'll get the idea

#### Fixing it
Django has a built-in decorator @staff_member_required, which checks the logged in user's is_staff (bool) field. If you tried to delete a message as normal user in the admin view, it will open the Django admin login page with an error message. If you uncomment the decorator linked above, trying to access the admin panel as regular user will result in the same error and the vulnerability is fixed.

### A7:2017-Cross-Site Scripting (XSS)

#### Description
Much like in the earlier injection section, you shouldn't trust user input blindly. In this implementation I deliberately let the user send any kind of messages without "sanitizing" the input, which leads to possible problems.

#### Test it yourself
Try sending a message ```<script>alert("Distressing message");</script>```, and everyone reading the main page will get an annoying popup. If you want to try something more daring, log in as regular user, send a couple of messages normally, then send a message like this: ```<img src="http://127.0.0.1:8000/chat/delete/{message_id}">``` the message is sent, but nothing happens, as delete/ route is protected by the aforementioned decorator. But now log in as admin user and refresh the page, you'll see that the message which id you sent the "image" has disappeared. 

#### Fixing it
https://github.com/cyberrase5/cyse-project1/blob/master/chat/templates/pages/index.html#L19 \
Just remove the |safe part, fixed version on the line above commented. Now the app will sanitize the input, leaving only the raw text without the effects they earlier had.

### A10:2017-Insufficient Logging & Monitoring
https://github.com/cyberrase5/cyse-project1/blob/master/chat/views.py#L59

#### Description
Apps with logins connected to internet will inevitably face all sorts of low-end attacks, such as bruteforcing passwords. Therefore it's important to keep logs of (attempted) logins and other important events for possible later examination. If certain IP-ranges are responsible for bruteforce attacks, the range can be banned from accessing the sites or logging actual logins might be useful if some foul play suspected.

I'm too afraid (and lazy) to overwrite the default Django login, so I decided to log registrations. It's not exactly the same thing, but if you look at the code I'm sure you'll understand how my implementation is pretty much the same thing as logging logins.

#### Test it yourself
Uncomment log_register(), register an account and check the automatically created file log.txt

#### Fixing it
See above

### CSRF
https://github.com/cyberrase5/cyse-project1/blob/master/chat/views.py#L13 \
https://github.com/cyberrase5/cyse-project1/blob/master/chat/templates/pages/index.html#L9

#### Description
I have removed CSRF safeguards in posting new messages by using the @csrf_exempt decorator in views.py index(). Maybe a long theoretical explanation isn't needed as it's explained in the course material, so let's jump into practice.

#### Test it yourself
I'm not entirely sure if I did it correct, but here's what I did: I fired up my old Tsoha app (which uses Flask and starts an app at localhost:5000), modified one of the html forms to 1. ```<form action="http://127.0.0.1:8000/chat/" method="POST">``` and 2. added field ```<input type="hidden" name="content" value="I will kill you all hahahha">```. Submitting the form redirects you to the chat app front page. which contains the nasty message that you didn't send.

Even if this isn't how it actually works (because of the same address localhost the app thinks it's the same site or something like that.) the idea is the same, a site has a malicious form that posts to somewhere else you think it does etc. I don't have access to a site in the real internet, so this will have to do.

#### Fixing it
Remove the @csrf_exempt decorator from views.py index() and uncomment the {% csrf_token %} in index.html. If you now attempt the above, it will redirect to Forbidden 403 Django page.

### Honorable Mentions
- SECRET_KEY in mysite/settings.py is hardcoded; everyone can see it. .env file where the secret key is defined should be created, and in settings.py the hardcoded key should be replaced with something like os.getenv("SECRET_KEY")
