Disclaimer: these are just personal notes, stuff could be wrong.

1. Add domains to Splunk via splunk script. (data input in Splunk and execute daily)
2. Add alert to Splunk via search. (execute daily after data input)
3. Create app in Splunk in order to execute custom script (new method)
4. Use custom script to send new found domains to monday.com


After creating app in Splunk:
add monday.py (named it scriptalert.py) to /opt/splunk/etc/apps/scriptalert/bin

add following to alert_actions.conf in: /opt/splunk/etc/apps/scriptalert/default
[scriptalert]
is_custom = 1
label = script alert
payload_format = json

Add following to app.conf in: /opt/splunk/etc/apps/scriptalert/default
[install]
is_configured = 1

[ui]
is_visible = 0
label = scriptalert

[launcher]
author = 
description = scriptalert
version = 1.0.0

