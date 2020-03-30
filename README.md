# Project Title

Biazza

## Getting Started

This project is about creating an interactive medium for students and instructors such that, 
1) Instructors can post assignements, set due dates, view progress of the class through question/answers
2) Students can view upcoming/recent assignments
3) Students can message peers/instructors if they have any questions
4) Students can switch between multiple classes
5) Students can view different due dates via the calendar option. 
6) Students can also post questions

* <a href="https://www.youtube.com/watch?v=JzQQVPEuGzI&feature=youtu.be">Phase 1 Demo Link</a>
* Phase 2 later
* Phase 3 later

### Prerequisites

Docker

### Running the server

In order to run the server, you simply need to follow these steps.

1. Clone the repository locally
2. Navigate to the root of the project folder
3. Enter the following to build the image
    ```
    docker-compose build
    ```
4. Enter the following to run an instance of the image
    ```
    docker-compose up -d
    ```

From here you will be able to got to http://localhost:8000 to view the webpage.

If you need to connect to the MySQL image, you should be able to connect to the database using
* Username: root
* Password: password
* Hostname: localhost:3306

## How to test

Phase 1:
```
<insert tests>
```
<insert tests>

### Languages structures Used

1) HTML
2) Flask
3) CSS
4) AJAX
5) <more if needed>

```
refer to report <link for report here> for more details on the code used.
```

## Deployment

Done using docker. You can follow the steps mentioned in the section above "Installing"

## Built With

* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - Web Design 
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Styles for HTML
* [AJAX](https://api.jquery.com/category/ajax/) - Client Side framework
* [Flask](https://palletsprojects.com/p/flask/) - Web Framework
* [more if needed](https://api.jquery.com/category/ajax/) - Client Side framework

## Authors

* **Liam O** - *Initial work* - [Orrbit](https://github.com/Orrbit)
* **Sam Marchant** - *Initial work* - [sam21marchant](https://github.com/sam21marchant)
* **Shazmaan Malek** - *Initial work* - [Shazmaan](https://github.com/Shazmaan)
* **Anant Patni** - *Initial work* - [anantpat](https://github.com/anantpat)

## License 

<if needed>
This project is licensed under the <license> - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thank you piazza :)
