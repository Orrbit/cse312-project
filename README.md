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

```
insert video demo here.
```

Images for the above if needed...
```
images...
```

### Prerequisites

Docker

```
Install Docker and the rest if we have any...
```

### Installing

To get the server up, build an image using:

```
docker build -t biazza-image:latest
```
And then run an instance of that image using

```
docker run -d -p 8000:8000 biazza-image:latest
```
Verify that the image is running with port 8000 open using

```
docker ps -a
```
Navigate to localhost:8000

And repeat above if you want to create multiple images

```
insert docker image example if needed.
```

<Insert docker image exmaple here if needed>

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
