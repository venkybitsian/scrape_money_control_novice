-----------------------------------README_EXECUTE_SQL-----------------------------------

step 1: sql loader tech has been used, observe mc.sh, mc.ctl

step 2: place in shell env

step 3: ftp file moneycontrol_after_cleaning_analyze_forsql.csv in same path

step4: setup env variable DATABASE

step 5: sh mc.sh

------below re LOGS------





-rw-r--r-- 1 rd687a4 netcrk    52786 Jun 17 07:49 moneycontrol_after_cleaning_analyze_forsql.csv
[rd687a4@devapp687cn venk]$ export DATABASE=MIGR_ITER_10/MIGR_ITER_10
[rd687a4@devapp687cn venk]$ sh mc.sh


Enter The Source Files Directory:
/u02/netcracker/rbm/rd687a4/infinys_root/migration/venk

Enter The Table Name u Want
mc
The Source Directory and TableName is :/u02/netcracker/rbm/rd687a4/infinys_root/migration/venk
 mc
Processing Started:
/u02/netcracker/rbm/rd687a4/infinys_root/migration/venk
Trying to Drop the table if it is already there
/u02/netcracker/rbm/rd687a4/infinys_root/migration/venk
hi
mc

SQL*Loader: Release 12.1.0.2.0 - Production on Sun Jun 17 07:50:21 2018

Copyright (c) 1982, 2014, Oracle and/or its affiliates.  All rights reserved.

Path used:      Conventional
Commit point reached - logical record count 64
Commit point reached - logical record count 128
Commit point reached - logical record count 192
Commit point reached - logical record count 256
Commit point reached - logical record count 320
Commit point reached - logical record count 384
Commit point reached - logical record count 443

Table MC:
  443 Rows successfully loaded.

Check the log file:
  moneycontrol_input.log
for more information about the load.
Process Ended ....
[rd687a4@devapp687cn venk]$

-----RUN THE SQL QUERIES AND GENERATE REPORT-------------------------------------



