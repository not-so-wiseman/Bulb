:bulb: *This README.md is best read on Github at https://github.com/not-so-wiseman/Bulb/*

# Bulb
<img src="Logo.png" width="200"/>
Bulb is a simple companion app for Brightspace :copyright: D2L. Students can easiliy view upcoming course events and statistics on their grades all without entering any data! 

## Getting Started
These instructions will help you get a copy of the project up and running in your browser or android phone.

### Prerequisites
What things you need to install the software and how to install them

- [x] A stable internet connection
- [x] If you are using an Android phone to view the project you will need to have at least version Jelly Bean (SDK version 16) of Android OS installed.
- [x] To view the project in your browser you will need a stable version of Chrome

### Android Phone
1. Download the app's APK file [__**Bulb.apk**__](https://github.com/not-so-wiseman/Bulb/blob/master/bulb.apk) from the main folder. 

2. Transfer the APK file onto your Android phone.

3. Under your phone's __**Downloads folder**__ select the file and click **install** when prompted. 
<img src="/screenshots/a_install.png" width="150"/>

4. Your will get a warning, "Blocked by Play Protect", saying the app's developer is not recognized. This is because the app is not on the play store and we have not registered as developers. Click **install anyway** to go ahead with the installation. 
<img src="/screenshots/b_install_anyway.png" width="150"/>

5. You will get another warning, "Send app for scanning", click **don't send** to go to the app installation. 
<img src="/screenshots/c_no_report.png" width="150"/> 

6. To use the app follow the instructions under [**Using the App**](#using-the-app)


### Browser
1. Go to [Appetize.io](https://appetize.io/embed/wttkyjxwuvk1x6rmeua3v94kt4?device=pixel4&scale=100&orientation=portrait&osVersion=10.0&deviceColor=white). Appetize.io simulates android apps in the browser, this link will bring you to a custom simulator for Bulb (i.e. the APK is already setup and ready to start)

2. To use the app follow the instructions under [**Using the App**](#using-the-app)

## Using the App
Bulb is currently connected to MUN's D2L test server. To explore the app use one of the fictional students from the table below. Each student is registered to one course called "Wiseman/James APP Development". 
You can loggin to see the student's full mock D2L account at [muntest.brightspace.com](https://muntest.brightspace.com/d2l/)

| no. | Username      | Password      |
| ---:|:-------------:|:-------------:|
|   1.| EWCJ_Student1 | EWCJ_Student1 |
|   2.| EWCJ_Student2 | EWCJ_Student2 |

0. When the app opens click the **Login** button to start

1. To get started log in a student by clicking **D2L-only login**, enter the student's credentials and then press login.
<img src="/screenshots/1_d2l_login_page.png" width="150"/>    <img src="/screenshots/2_press_login.png" width="150"/>

2. On Bulb's first page you can view the student's grades. You will see the student's overall average, what percentage of course material (overall) remains to be completed, and details for each course. To change the course details displayed click the course name. A dropdown will appear with other courses to choose from ( :heavy_exclamation_mark: this isn't applicable for the demo).
<img src="/screenshots/3_select_course.png" width="150"/>

3. Scroll down the "My Grades" page to see more. For each course you will see:

    :one: What the student needs to reach their goal for the course and an edit button to change the course goal  
    :two: The student's average for the course.  
    :three: All grade items for the course and their grades  
    
<img src="/screenshots/4_grades_page.png" width="150"/>

4. Click the edit button to change the goal average for the course.
<img src="/screenshots/5_update_goal.png" width="150"/>

5. Next, explore the "My Calendar" page by clicking the calendar button in the top-right corner.
<img src="/screenshots/6_nav_to_calendar.png" width="150"/>

6. On the "My Calendar" page you will see a monthly calendar with the current date highlighted. Click the arrows above the calendar to change the calendar month.
<img src="/screenshots/7_calandar_home.png" width="150"/>

7. The "My Calendar" page has two main features:

    :one: A calendar with all upcoming events highlighted in blue  
    :two: A list of all upcoming events and their due dates  
    
<img src="/screenshots/8_calenader_events.png" width="150"/>

8. To see the events set for this month scroll to the buttom of the page to view **Upcoming Events**
<img src="/screenshots/9_calendar_list.png" width="150"/>

# Project Archetice
The design for Bulb can be viewed in two parts:

1. the backend API
2. the android application.

The backend for Bulb is a custom RESTful API designed in Flask and hosted on Heroku. This API provides the
data used by the android application.

The android app acts as the user interface for Bulb. In the future a web site will be added. 

The diagram below illustrates the relationship between Bulb's two parts:

<img src="/project_diagram.png" width="250"/>

# File Structure 
Below is a simplied file structure tree of the project with notable files highlighted.

```
assests
├───Bulb *Android App Folder*
|   ├───build
|   ├───gradle
│   └───app
│       └───src
│           └───main
│               ├───res
│               └───java
│                   └───com
│                       └───a_wiseman_once_said
│                           └───bulb
│                               └─── Calendar.java  //Logic for My Calendar Page**
│                               └─── editGradeLogic.java  //Code for the popup dialog "edit grades"*
│                               └─── GradesPage.java  //Logic for My Grades Page*
│                               └─── Login.java  //Logic for Logging a user in
│                               └─── MainActivity.java  //Splash page
└───RestAPI
    ├───docs
    └───src
        ├───app.py  //Main entry for the Flask application (i.e. serves the REST API)
        ├───LampAPI
        │   ├───utils
        │   │   └─── calendar.py
        │   │   └─── courses.py
        │   │   └─── gradulator.py
        │   │   └─── nlp.py
        │   ├─── authenticate.py
        │   ├─── config.py
        │   └─── lamp.py
        └─── templates  //Contains HTML pages*
```

# Authors
* Emily Wiseman
* Christian James

