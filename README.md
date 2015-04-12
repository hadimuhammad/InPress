# InPress
InPress is a web-based application, which allows students in universities and colleges to respond in real time to questions posted by their instructor. It is supported on any internet-enabled device including tablets and mobile devices. The goal is to improve student engagement in the classroom through the use of the latest technologies.

### Screenshot
![](http://i.imgur.com/MILRIGI.png)

### Technologies Used
![](http://i.imgur.com/72THO8U.png)

### Configuring the Server
1. InPress requires a physical or virtual machine to act as a server. The minimum requirements are below:
  1. Operating System: Microsoft Windows, Apple Mac OS, Linux
  2. RAM:2GBofRAM
  3. Hard Drive: 250 MB of hard drive space
  4. Processor: 1 Core 2.6 GHZ
2. Install the following packages on the server:
  1. Python (http://www.python.org/downloads/)
  2. Django (http://www.python.org/downloads/)
  3. PostgresSQL (http://www.postgresql.org/download/)
  4. PgAdmin (http://www.pgadmin.org/download/)
  5. Apache Server ( http://httpd.apache.org/ )

3. Configure PostgreSQL:
  1. Open PgAdmin
  2. Create a server with the following credentials:
     1. name: inpress
     2. user: postgres
     3. password:
     4. host: localhost
     5. port: 5555
  3. Once a server has been successfully created, create a database named ‘inpressdb’ within the server you created in step b.

### Configuring InPress
1. Navigate to the following URL: https://github.com/hadimuhammad/InPress, and click on Download Zip (Located on the right)
2. Unzip the zip file you obtained in Step 4 in a location where you wish to deploy your InPress (e.g ~/inPress)
3. Navigate to the following location in your InPress directory – InPress/ and execute the following commands:
  1. python manage.py syncdb [If the above command yields errors, ensure that you database is setup and ensure that the settings in InPress/inPress/settings.py are correct and match up the settings in Step 3]
  2. ￼￼￼￼￼￼If this is your first executing this command, then you will be asked to provide a user name, password, email address for the admin console. Ensure you keep these credentials in a safe place. If you lose it you will have to re- create the database!
4. In order to run InPress, execute the following: python manage.py runserver <server_address>:<port> where port is the port number you would like to use (i.e. inpress.com:8132, inpress.com is the server address and 8132 is the port).

### Bringing InPress to Production

1. Install mod_wsgi (https://code.google.com/p/modwsgi/)
2. Go to your home directory and create inpress.wsgi
3. Input the following into inpress.wsgi
import os
import sys
sys.path = ['/var/www/inPress'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'inPress.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
4. Copy all of InPress files to “/var/www”
5. Go to the directory “/etc/apache2/sites-avaliable”
6. Create the file “inpress.conf” , and make sure you are in SUDO or ROOT
7. Input the following into “inpress.conf”
<VirtualHost *:80>
WSGISCriptAlias / <your inpress.wsgi full-path>
Servername <hostname / IP>
Alias /static /var/www/inPress/module/static
<Directory /var/www/inPress/> Order allow,deny
Allow from all
</Directory>
</VirtualHost>
8. Change directory to “/var/www/inPress/inPress”
9. Open the file “settings.py”
10. Turn DEBUG to FALSE (DEBUG = False)
11. Save and Reload apache service (service apache2 reload)





Copyright © 2014 by InPress All rights reserved.
No part of this publication may be reproduced, stored or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise without prior written permission by InPress®
Reproduction prohibitions do not apply to the forms contained in this product when reproduced for personal use.
