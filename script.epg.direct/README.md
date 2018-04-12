EPG-Direct 
==========

**No longer maintained - feel free to fork the project though!**

> Current version: v0.6.7

[![EPG-Direct](https://s19.postimg.cc/760xuqdyb/screenshot017.png)](https://postimg.cc/image/fbizsw273/)

EPG-Direct is an open source TV Guide for [Kodi](https://kodi.tv) that makes use of TV schedules data provided by [SchedulesDirect.org](https://schedulesdirect.org) via its JSON-API.

**Note:** In order the be able to use this addon fully you will require a valid subscription form [SchedulesDirect.org](https://schedulesdirect.org) which will enable you to access the entire channel lineup of legally licenced guide data.

Download the Repository from [HERE](https://raw.github.com/bluezed/repository.bluezed/master/zips/repository.bluezed/repository.bluezed-1.1.zip)

Here are the basic steps to install EPG-Direct on your Kodi box.

# Prerequisites
* Kodi 16 or higher
* The downloaded Repository Zip-file
* Place the file somewhere you can get to easily on your Kodi box

# Installation
1. Go to System -> Addons and select "Install from Zip-file"                                          

2. Select the Zip file you downloaded earlier. This should install the Bluezed Repository on your box.

3. Now go to "Install from repository" and then "Bluezed Repository"                                                                   

4. Go to "Progrm add-ons" and select "EPG-Direct"                                      

5. A window should open where you need to select "Install"                                              

This should now install EPG-Direct on your system and will be located under "Programs".

# First start
Before you start the program you will be required to enter your SchedulesDirect login details.
If you don't have an account there yet you can sign up for a free 7 day trial here: [SchedulesDirect.org](https://www.schedulesdirect.org/signup)

Once done open the program settings of EPG-Direct and enter the login credentials.
You can now start using the program.

## Settings
[![SD-Settings](https://s19.postimg.cc/kke0qrkm7/screenshot013.png)](https://postimg.cc/image/kke0qrkm7/)

- First you need to select the lineups you want to use. A lineup is basically a set of available channels in a certain country and region.
Click on "Add lineup" and select the country you want and then enter a post-code. Usually the post-code is pre-filled to a generic valid one for the country but feel free to enter a different one.
That will now give you list of providers for that area. Select one and it will be saved as your first lineup.
**Note:** There is a limit on the number of lineups you can have in your SchedulesDirect account! The numbers displayed at the top of the Country selection dialog indicate how many lineups you already have compared to how many you are allowed.
 
- Once you selected at least one lineup you can start adding the channels you would like to have shown in the guide.
Click on "Edit channels" and you will see the list of your current lineups.
Select the lineup you want and a window with two columns will appear.
On the left all the available channels for this lineup are listed. You can scroll through the list and select channels by clicking on them. That will add them to the list on the right.
Once you're happy with the selection click on "Save" and your channels will be saved to the database.
You can now repeat this process for any other lineups you have.
**Note:** To change the order of the channels you need to start the guide and enter the context menu.

[![Channel-Selection](https://s19.postimg.cc/sr60icaov/screenshot016.png)](https://postimg.cc/image/sr60icaov/)

- You can delete lineups by selecting "Delete lineup" and simply selecting the lineup you want to remove.
**Note:** Deleting a lineup will also delete all channels you have selected from that lineup!

- With "Days of guide data to load" you can select for how many days the data should be downloaded. The default is 3 days.
**Note:** The more days you select the longer the download process will take!

- The "Schedules check interval" defines how often the program checks on SchedulesDirect for new guide data. The default is 24 hours.

- The "addons.ini" file is used to map channels to streams. There is one included in with the application but you can also provide your own file here.

## The Guide

If you have selected your channels and start the guide it will first load the data from SchedulesDirect and then present you with the program grid.

[![The Guide](https://s19.postimg.cc/fbizsw273/screenshot017.png)](https://postimg.cc/image/fbizsw273/)

### Watching a channel
You can scroll through the guide up, down, left and right. If you click on a program that is currently on the guide will try to open the corresponding stream or addon by looking for the Channel name in your Kodi favourites.
If it cannot find the channel there it will try the same with the addons.ini file, either the default one or the one you have configured.
If it has no luck there a dialog will appear where you have the choice to manually select where to play the program from. This selection will them be stored as the default for this channel.

### Reminders
When you click on a program that is on in the future a dialog appears where you can set a "Reminder". The program will the be marked red and you will get a notification 5 minuts before the program starts and then a pop-up at the time the program is scheduled. This pop-up allows you to open the guide directly or just dismiss it and also has a count-down that will close it automatically when that times out.

[![Reminder](https://s19.postimg.cc/a1e11lhy7/screenshot018.png)](https://postimg.cc/image/a1e11lhy7/)

### Sorting Channels
In the same dialog where you saw the "Remind" button you can change the channel order by clicking on "Channels". That will open a list of all your channels with instructions on how to change the sort order.

Press left to pull a channel out, then move it up or down. When in place, press right again to set. Pressing on a channel in the list will enable or disable it. 
On touch devices long press on a channel to pull it out, move the list to the desired place and then long press on the pulled out channel to put it in its new place.

[![Channel sorting](https://s19.postimg.cc/yj2geht0f/screenshot_CH.png)](https://postimg.cc/image/yj2geht0f/)


# Help & Support

To get help or report issues with this Kodi addon please either raise an issue on [GitHub](https://github.com/bluezed/repository.bluezed/issues) or post on the [Kodi forum](https://forum.kodi.tv/showthread.php?tid=287868).

For issues with the actual guide data, stations or lineups you should report this to SchedulesDirect [Lineup Support](https://www.schedulesdirect.org/lineupsupport) directly.

