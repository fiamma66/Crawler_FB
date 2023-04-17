# FB Crawler - Base on Selenium Chrome

------

Crawl FB Group every post content & comment
write to file in POST folder (create if not exists)
comment and image will write to list


## Getting Started

-----

Clone the project 

`git clone `

Cd to working directory

`cd Crawler_FB`

## Prerequisites

----

Need to use pipenv to install

`pip install pipenv`

Then install dependency

`pipenv install Pipfile`

Activate pipenv

`pipenv shell`

## Installing

---

Simply Install with setup.py

`python3 setup.py install --record files.txt`

`--record` option to Keep installing file list

## Running Test

---

### Prepare Testing 

1. prepare Facebook Account that can log in
2. prepare chromedriver - either place it into tools or use it as env

---

#### Prepare Account Prop
```properties
ACCOUNT=example@mail.com
PASSWORD=example
```

---

#### Prepare Chromedriver as env

Set chromedriver as env

Windows

Place chromedriver to C:\WebDriver\bin

or anywhere else to be placed
```batch
setx PATH "%PATH%;C:\WebDriver\bin"
where chromedriver
```

Linux & MacOS
```shell
cp chromedriver /usr/bin/local/
which chromedriver
```

---

### Run test without install

---

Can simply run testing without install

`python3 -m tests.DEV_CrawlerTest.main`


---

Run test after install

```shell
python3 app.py
```

---
