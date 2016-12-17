# IS211 Course Project

#############################################################
A Blogging Application

  This program allows people to log in into a web application
to effectively run a blog. In this case, a blog is a collection of
posts that someone has written that is shown in reverse
chronological order. Posts consists of a title, a date when it was
written, an author, and text that may contain HTML as well. The root URL
used is http://127.0.0.1:5000/ and it is the website to see the 
interactive web application. In this specific program, it utilizes Flask 
and SQLite3 to create a cohesive application that has a multitude of
controllers. 


These controllers include:  /,  /login, /dashboard, /post, /delete, /edit, /publish,
/unpublish, /blogpost,  /category,  and /logout. Each of these controllers are initiated
with an SQL query that pulls up information the SQL schema. The table is linked to an id
for Users and Posts and it is effectively used as means to create an interactive experience. There
is also a list of functions that are used throughout the program such as logged_in(), 
generate_list_of_posts(), and rtemplate(). logged_in() is a function that confirms if a user is
logged in or not. generate_list_of_posts() is a function that uses data from a database
 to generate a list of posts as an object. rtemplate() assists generate_list_of_posts() and
pulls up information for HTML through the template html files. Ultimately, the blogging
application allows a user to log in, log out, add a post, delete a post, go into the dashboard,
edit a post, publish a post, unpublish a post, connects posts to specific permalink URL, and categorize
posts to view one page as well. 

To log into the program: 

**Username**  | **Password**
------------------------- | -------------------------
Lido    |    norway
Flume  |    australia
Rustie   |   scotland
JaiWolf  |    america
ManilaKilla | philippines



#############################################################
