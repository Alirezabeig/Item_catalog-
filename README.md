Item Catalog
You can find it in my repository in github here: https://github.com/Alirezabeig/Item_catalog-

Project Overview:

Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Moreover, Registered users will have the ability to post, edit and delete their own items.


What did I learn?

Developing a web application using the Python framework Flask
Implementing third-party OAuth authentication such as facebook and google
Implementing CRUD (create, read, update and delete) operations.


PreRequisites:

Python ~2.7
Vagrant
VirtualBox
Setup Project:
Install Vagrant and VirtualBox
Download or Clone this  repository.

How to Run?
Launch the Vagrant VM using command:
  $ vagrant up
	$ Vagrant ssh 
Change the directory:
cd /vagrant 
run: python Database_set_FinalProject.py
run: python CategoryMore.py to add categories to your database 

Pints to consider: 

******** In order to have categories in your file, you should run this code: python CategoryMore.py  ****
******** Also don't forget this program allows you to only edit, delete and add new items as a logged in user to only existing categories.*****
In order to set up the detabas run this code:
python Database_set_FinalProject.py

Run your application within the VM
  $ python /vagrant/catalog/project.py
Access and test your application by visiting http://localhost:5000.
