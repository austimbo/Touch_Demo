# Touch Buddy

Touch Buddy is  a task reporting, tracking scheduling system for establishments that have multiple meeting rooms, such as as executive briefing centres that utilise Cisco's codec with the Tough-10 control panel. 

A common problem in such centres is that the's usually a finite number of technical-support staff and multiple rooms. Tech staff are often working on one issue when subsequent issues are reported. Touch Buddy is a low-cost scalable and non intrusive and trackable means for tech staff to be altered to issues whilst working on others. 

Here is a youtube video explaining how the system works:

https://www.youtube.com/watch?v=vV-nV3DDqFg

![Graphical Overview](https://github.com/austimbo/Touch_Demo/blob/master/images/Touch_Buddy_overview.jpg?raw=true)

## Touch Buddy Fundamentals

Touch buddy was designed for meeting rooms that utilise Cisco codes with Touch 10 control panels. The **Touch buddy** makes use of the codecs **room control** API which presents a help panel as an option to each meeting room. Users can choose an issue-type from a customisable menu. The request is passed to the Touch Buddy server which ten uses a **Webex Teams**  API to alert the appropriate support resource for that team. 

When support team members receive a support alert (via Webex Teams), they are presented a **Microsoft Adaptive Card**. The support team member who presses the acknowledge button on the **MS Card** has their details passed through to the appropriate rooms touch 10 panel. 



### Prerequisites
This solution requires meeting rooms to be equipped with Cisco codecs with the Cisco **Touch 10** control panels.There is no limit to the number of codec systems supported.  My development environment was running code version **ce 9.9.9.3** .
 
The python code was developed using Python 3.7 on a mac using **mac os 10.14**.  It will soon be testing under Linux and Windows. 

**Cisco Webex Teams** access is required. The application uses  Two-way communication with Webex Teams. The messaging API is used to post event alerts and webhooks are used to communicate acknowledgments back to the application. As Webex Teams initiates HTTP communications inbound to the API server (webhook), the application server needs to be reachable via webbed teams. I have used **ngrok** to make my API reachable from outside of my natted lab environment. Currently  this is set up manually, I have plans to automate registering ngrok's URL with Webex teams. For now, webhooks need to be to be set up manually. Details can be found at: 

https://developer.webex.com/docs/api/guides/webhooks


```
Give examples
```

### Installing



## License

This project is a standard Beerware licence (you play with it, buy me a beer sometime )unless used for commercial use (we need to talk, as it might help feed my family some day). 

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

