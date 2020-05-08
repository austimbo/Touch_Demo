# Touch Buddy

Touch Buddy is  a task reporting, tracking scheduling system for establishments that have multiple meeting rooms, such as as executive briefing centres that utilise Cisco's codec with the Tough-10 control panel. 

A common problem in such centres is that there are usually a finite number of technical-support resources allocated to a site. During events it is sometimes necessary for meeting hosts request assistance from these resources, without disrupting the meeting. It is also important to track the utilisation of support resources and the types of issues reported.

![alt text](https://github.com/austimbo/touch_Demo/images/Touch_Buddy_overview.jpg?raw=true)

## Touch Buddy Fundamentals

Touch buddy requires that all meeting rooms be equipped with Cisco codec that is equipped with the Cisco Telepresence Touch-10 control panel. The Touch Buddy Python code then utilises several APIs, such as the Codecs **Room Control**,  "**Webex Team's** api and Python's embedded **sqite3** to provide a fully functional resource alerting and trackingand reporting system  

### Prerequisites

When Considering this solution it is important to understand that the solution required users meeting rooms to be equipped with Cisco codecs using CE9.x software and to have access to Cisco Webex teams. 

The python code has been developed under Python 3.7. The was developed under MacOs 10.14 only so far. There's noting limiting it to MacOs. It will soon be testing under Linus and Windows. 

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

