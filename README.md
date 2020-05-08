# Touch Buddy

Touch Buddy is  a task reporting, tracking scheduling system for establishments that have multiple meeting rooms, such as as executive briefing centres that utilise Cisco's codec with the Tough-10 control panel. 

A common problem in such centres is that the's usually a finite number of technical-support staff and multiple rooms. Tech staff are often working on one issue when subsequent issues are reported. Touch Buddy is a low-cost scalable and non intrusive and trackable means for tech staff to be altered to issues whilst working on others. 

![Graphical Overview](https://github.com/austimbo/Touch_Demo/blob/master/images/Touch_Buddy_overview.jpg?raw=true)

## Touch Buddy Fundamentals

Touch buddy was designed for meeting rooms that utilise Cisco codes with Touch 10 control panels. The **Touch buddy** makes use of the codecs **room control** API which presents a help panel as an option to each meeting room. Users can choose an issue-type from a customisable menu. The request is passed to the Touch Buddy server which ten uses a **Webex Teams**  API to alert the appropriate support resource for that team. 

When support team members receive a support alert (via Webex Teams), they are presented a **Microsoft Adaptive Card**. The support team member who presses the acknowledge button on the **MS Card** has their details passed through to the appropriate rooms touch 10 panel. 



### Prerequisites
This solution requires meeting rooms to be equipped with Cisco codecs running CE9.x software, it also requires that all meeting room codecs are equipped with Cisco **Touch 10** control panels.  

The python code has been developed under Python 3.7. The was developed under MacOs 10.14 only so far. There's noting limiting it to MacOs. It will soon be testing under Linus and Windows. 

```
Give examples
```

### Installing

TBA

## License

This project is a standard Beerware licence (you play with it, buy me a beer sometime )unless used for commercial use (we need to talk, as it might help feed my family some day). 

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

