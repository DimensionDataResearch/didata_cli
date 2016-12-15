Changelog
=========

changes with didata_cli 0.2.4
-----------------------------

general
~~~~~~~
- Tagging calls added [jadunham1]

server
~~~~~~
- Added add_disk to server [jadunham1]

changes with didata_cli 0.2.0
-----------------------------

This marks a new minor version upgrade.
Mainly due to the fact that new parameters have been added to all functions

general
~~~~~~~

- Added ability to have multiple output types: json, grid, mediawiki, rst, ect. [jadunham1]
- Added --query to some CLI parameters.  Can currently query ReturnKeys and ReturnCount [jadunham1]

server
~~~~~~
- Added add_disk to server [jadunham1]
- Added remove_disk to server [jadunham1]
- Added modify_disk_disk to server [jadunham1]

changes with didata_cli 0.1.12
------------------------------

general
~~~~~~~

- Added documentation [jadunham1]
- Added unit tests from cmd_server [jadunham1]

network
~~~~~~~
- Add public ip blocks [lawrencelui-dd]
- List public ip blocks [lawrencelui-dd]
- Delete public ip blocks [lawrencelui-dd]

changes with didata_cli 0.1.11
------------------------------

server
~~~~~~
- better output for servers displaying all disk info [jadunham1]

bugs
~~~~

- fixing unicode issues from libcloud [jadunham1]

Changes with didata_cli 0.1.10
------------------------------

Network
~~~~~~~
-  Add create firewall rule [lawrencelui-dd]
-  Add list firewall rules [lawrencelui-dd]
-  Add delete firewall rule [lawrencelui-dd]

Changes with didata_cli 0.1.9
-----------------------------

Server
~~~~~~~
-  Add info command [lawrencelui-dd]
