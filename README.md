UOCIS322 - Project 6
Author : Adrian Martushev 
Email : adrian@tutortree.com

This is continuation of project 5, a brevet time calculator. In addition to the frontend buttons and database we now implement a RESTful API.


Brevet Time Calculations:

Brevet control(e) times are calculated based on the control's distance from the start and predefined minumum and maximum speed limits. The speed limits in ACP Brevets are as follows:

Control Location (km) Minimum Speed (km/hr) Maximum Speed (km/hr) 0 - 200 15 34 200 - 400 15 32 400 - 600 15 30 600 - 1000 11.428 28 1000 - 1300 13.333 26

Calculations are done by dividing the distance by speed (result in hrs) for the given segment. Conversion to hours and minutes is done by subtracting whole hours and multiply remaining fraction by 60. Minutes are rounded to the nearest minute. Brevet times are done sequentially in their respective rows, eg the control time for a 550km brevet would first calculate 0-200, 200-400, then 400-550 with their start and close times respectively.

Example: Consider a control at 890km on a 1000km brevet.

Opening Time 200/34 + 200/32 + 200/30 + 290/28 = 29H09

Closing Time 600/15 + 290/11.428 = 65H2
