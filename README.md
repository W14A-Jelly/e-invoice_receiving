# Sprint 3 #

# e-invoice_visualiser #
Frontend of application

## Priority of features for Application ##

1. - [ ] Visualize stored e-invoices (Call /invoice/rendering/upload Build, Collaborate & Integrate APIs | SwaggerHub )

2. - [ ] Filter e-invoices (Default: Newest e-invoice, Filter by: time, sender, cost range)  Colby create use case

3. - [ ] File management system (Create directories) [Expand on this in sprint 4] Zijie create use case

4. - [ ] Mark unread e-invoice (Add a visual marker) Elise create use case

5. - [ ] Accounts (Same account system as e-invoice receiving API)

6. - [ ] Blacklist sender (Not necessary right now)

## Features for e-invoice receiving API ##
* - [ ] SMS (or use another groups)

* - [ ] Send error communication report to sender if e-invoice is not in UBL 2.1 standard.

* - [ ] Notify user if there are storage problems

* - [ ] /list/filenames/ Route that returns all file names that belongs to the user.  {'filenames' : [filename, filename2]} using ownership table

* - [ ] /list/filter/ Route that returns a list of filenames that meet filter criteria {'filenames' : ['filename1', 'filename2']} using ownership table

* - [ ] Database has to store directory structure for each user id (Create this in sprint 4)

* - [ ] Database stores information about email, SMS number

## Roles ##

* Colby: Frontend basic UI design, Database, Notify user if there are storage problems, ownership table new ‘sender’, ‘time’, ‘price'. Create SMS table ‘user_id’, ‘SMS number’. Create ‘blacklist’ table, ‘user_id’, 'ignore’

* Elise: Mark unread e-invoice, /list/filenames/, Blacklist sender

* Zijie: Filter e-invoices, File management system, Store information of sender to database

* Kian: Accounts, SMS, Send error communication report, /list/filter/