# Casper-HC

A friendly HipChat plugin to Jamf Pro that allows a room to search inventory and receive notifications from webhook events.

> This application should be considered in an alpha state. While much of the core feature set is complete much of the code base may change between updates that could break existing databases and require re-setup of the application.

![Screenshot](/images/casper-hc.png)

## Features

### Inventory Search

* Computers
    * Supports wildcards `*`
    * Matches on most device identifiers and location data
    * Single and list results
    * Does not match on `id`
* Mobile Devices
    * Supports wildcards `*`
    * Matches on most device identifiers and location data
    * Single and list results
    * Does not match on `id`
* Users
    * Does not support wildcards
    * Matches on usernames and email addresses
    * Single results only

![Screenshot](/images/search-single.png)

![Screenshot](/images/search-list.png)

### Notifications

Supported inbound Jamf Pro webhook events:

* ComputerAdded
* ComputerCheckIn
* ComputerInventoryCompleted
* JSSShutdown
* JSSStartup
* MobileDeviceCheckIn
* MobileDeviceEnrolled
* MobileDeviceUnEnrolled
* PatchSoftwareTitleUpdated
* RestAPIOperation

![Screenshot](/images/notifications.png)

## Basic Setup

This application uses environment variables to configure itself.

> You may alternatively hard code these values into your local copy of `casper/config.py` but it is **not recommended**.

To set an environment variable use the following command:

```
~$ export VARIABLE_NAME=VALUE
```

The following environment variables will configure the MySQL server connection:

```
MYSQL_SERVER
MYSQL_ROOT_PASSWORD (for Docker)
MYSQL_DATABASE
MYSQL_USER
MYSQL_PASSWORD
```

Flask will attempt to read a `FLASK_CONFIG_FILE` environment variable containing the path to your own configuration file.

The file should use Python syntax and populate the needed values to customize the application at runtime.

Here is an example `flask_env` file:

```python
DEBUG = True
SERVER_DOMAIN = 'casper.example.com'
DATABASE_KEY = '\xd7M\xdcK\n\xe2\xbb5\x8c\x9e\x88\x1bn\xae\xa2D'
SECRET_KEY = '_\x11"k\x9f\x94\xee]\xe6\xfa\xaa\x7f\xc4Z\xec\x13'
```

> Another alternative to the MySQL environment variables above is to include a `SQLALCHEMY_DATABASE_URI` constant in your Flask config with the full URI to connect to the database:
>
> ```
> SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@server/database?charset=utf8'
> ```

### Creating the database and secret keys

Generate random bytes for the values of the `DATABASE_KEY` and `SECRET_KEY`.

The `DATABASE_KEY` is used to encrypt saved service accounts in the database.

The `SECRET_KEY` is used to secure active sessions by enabling cookie signing.

*(see [Flask: Sessions](http://flask.pocoo.org/docs/0.12/quickstart/#sessions))*

The following code will produce sufficiently random keys:

```
>>> import os
>>> os.urandom(32)
'\xfc\x86\x7f=\xc53\xfbyA\x08\x91\xb5\x03\xff\x8d+s\xdc\xd4\xb79\x17\x82\xb4\x94\x7f\x14.\xc0\xd8KL'
>>>
```

...or...

```
>>> from Crypto.Random import get_random_bytes
>>> get_random_bytes(32)
'\xc6\xe4i\xf0w\t\\\xf0\x114\x06\x98\x81\xa9\xa8\xefB\x15\xef\x99\xe3\xf1-Z\x0cOW\x0f\xed\xfa\xb3\xe7'
>>> len(get_random_bytes(32))
```

## Creating the Database

From the application directory run the commands below to create the initial database.

**Be sure to have the environment variables for the MySQL database, user and password set first.**

```o
>>> from jamfy import db
>>> db.create_all()
```

*(Optional)* To use Flask-Migrate's migration feature initialize a migration repository with the following command in the application directory:

```
~$ python manage_db.py db init
```

*See the [Flask-Migrate docs](https://flask-migrate.readthedocs.io/en/latest/) for more details.*

## Local / Development Testing

The application can be launched by executing `run.py`:

```
~$ python run.py
```

To properly test your application use a tunneling service such as [ngrok](https://ngrok.com/) to make it accessible to the internet.

```
~$ ngrok http 5000 --bind-tls true
```

A randomized URL will be made available that tunnels traffic from port `443` through a secure tunnel to port `5000` on your machine where the application is running.

See [Start a ngrok tunnel](https://developer.atlassian.com/hipchat/tutorials/getting-started-with-atlassian-connect-express-node-js#Gettingstartedwithatlassian-connect-express(Node.js)-Startangroktunnel) for more detailed instructions.

### Install to HipChat Room

The application's capabilities descriptor will be reachable at:

```
https://{subdomain}.ngrok.com/hipchat/capabilities
```

See [Install the add-on in HipChat](https://developer.atlassian.com/hipchat/tutorials/getting-started-with-atlassian-connect-express-node-js#Gettingstartedwithatlassian-connect-express(Node.js)-Installtheadd-oninHipChat) for more detailed instructions on how to manually install the application.

### Configure Jamf Pro Service Account

> A service account is only required for enabling the search features of the plugin. Notifications can be used without adding a service account.

From the configuration page you may enter a Jamf Pro URL with a username and password for a service account to enable the plugin to perform API requests.

![Screenshot](/images/configure.png)
