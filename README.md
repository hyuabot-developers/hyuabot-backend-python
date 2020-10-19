Personal fastapi project to operate several projects

## Getting Started

These instructions about how to clone this project for developing and testing purposes. See deployment to know how to deploy the project on a release channel

## Prerequisites
```
python3
```

### Installing
```
# Install python3 and pip for your OS
# Python 3.9 is not supported yet 
$ sudo apt install python3 python3-pip
```

### How to Run
```
# Get required libraries
pip install --user -r requirements.txt

# Update Submodules
git submodule update --init --recursive --force

# Execute main.py
python main.py
```

### Sub directories

* api : Include some information about Hanyang Univ. ERICA Campus as json file. For more info please visit this [repo](https://github.com/jil8885/API-for-ERICA).
* kakao : Chatbot that provides several information for Hanyang Univ. ERICA Campus. For more info please visit this [repo](https://github.com/jil8885/fastapi-kakao-i-hanyang).
* common : Include config variables to use all projects like timezone.
* firebase : Include code to operate firebase.
* food : Include code to crawl food menu from Hanyang Univ. Website and store firebase.
* library : Include code to crawl remained seats in reading room from Hanyang Univ. Website and store firebase.
* transport : Include code to get information about subway, bus and shuttle around Hanyang Univ.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Jeongin Lee** - *Main Developer* - [jil8885](https://github.com/jil8885)

See also the list of [contributors](https://github.com/jil8885/hyuabot-mainline/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details