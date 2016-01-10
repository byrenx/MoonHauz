MoonHauz
====================

MoonHauz is real estate properties management and advertising application. It is built 
in Google App Engine platform, Ferris 2 framework, 
Bootstrap (which is subject to be replace with material design lite), and AngularJS.

Currently it is under development.


### Installing Frontend dependencies

Go to angular-app forlder then type the command `bower install` to install the dependencies being described in bower.json

To install bower
First install npm which is included in nodejs so you to install nodejs, for instructions visit [https://nodejs.org/en/download/package-manager/](https://nodejs.org/en/download/package-manager/)
Next, use install bower `npm install -g bower`

### Setting Up GCS:

1. Enable billing to create a bucket
2. Create a bucket name `moonhauz` and a folder named `images` inside the bucket
3. Edit the bucket objects default permission, then
   add new User which are `allUsers` to make uploaded file
   to be publicly accessible and for the bucket to work as a CDN.

