# Cyber Security Base Project I
Course project for Cyber Security Base with 5 vulnerabilites as per the assignment

### Starting up
- öas
- las

### User Guide
A simple Twitter/X -style app, where you can leave messages for everyone to see. There are two kinds of users, normal and admin users. Everyone can send messages, but only admins can remove them. I think you can figure out the rest.

Start the app at http://127.0.0.1:8000/chat/

No logging out because I'm lazy lol

## The 5 Vulnerabilities
I've chosen the 2017 list https://owasp.org/www-project-top-ten/2017/Top_10 plus CSRF, as it's allowed in the assignment

### A1:2017-Injection
https://github.com/cyberrase5/cyse-project1/blob/master/chat/views.py#L35 (and the couple of lines below)

Description\
Before creating an account, the server checks whether an account with this name already exists, because Django handles the situation by giving an error page, not very elegant. If an account already exists, the registration page is rendered again with a helpful red error message, including the attempted name (pulled from the database!). The query string is constructed unsafely, which makes the app vulnerable to SQL injections.

Test it yourself\
First, create an account, the details don't matter, just remember the username. Now try to create an account with the same name, and you'll get an error message "Username [({chosen_name},)] already in use". Because the query is unsafe and the entire SQL response is given to the message, finding the correct text to input as username will result in data leaking. You can try to figure it out yourself or check it below:
<details>
  <summary>Spoiler warning</summary>
  
  {chosen_name}' UNION SELECT password FROM auth_user --
  
</details>
Now create an account with the malicious "username", and this time you will not only get the username but also the list of all the passwords hashed. While the passwords are hashed, the leak is still pretty bad. 

Fixing it\
Link here\
The main fix is parameterized queries. Also fetchall() has been changed to fetchone() and in the retrun render command response[0] is used as additional security, so that even if the response contained passwords, only the first one would be leaked. Now test the fixed version. comment the code between the comments BEGIN and END BROKEN VERSION and uncomment the FIXED VERSION one and test the previous injection, it doesn't work.

### A5:2017-Broken Access Control

Description\
asd

Test it yourself\
asd

Fixing it\
asd

### A7:2017-Cross-Site Scripting (XSS)

Description\
asd

Test it yourself\
asd

Fixing it\
asd

### A10:2017-Insufficient Logging & Monitoring

Description\
asd

Test it yourself\
asd

Fixing it\
asd

### CSRF

Description\
asd

Test it yourself\
asd

Fixing it\
asd

### Misc
Here are some honorable mentions:
- SECRET_KEY in mysite/settings.py is hardcoded; everyone can see it. .env file where the secret key is defined should be created, and in settings.py the hardcoded key should be replaced with something like os.getenv("SECRET_KEY")
