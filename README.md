# PayPwn Capture The Flag

## Background

This capture the flag consists of 4 fake websites. The websites mimic PayPal (PayBuddy), eBay (eBid), Facebook (Friendbook), and Hotmail (Coldmail). Content on these sites is periodically auto generated by ChatGPT and cached, thus making them seem like fully functioning sites with live user data. The objective is one that everyone is very familiar with, to get money. Auto generated users on the system have money, and you need to figure out how to make it yours.

### Solution (Spoilers)

The PayBuddy website has a customer support chat bot you can communicate with. You need to get access to a user's email, and collect enough information about that user to social engineer the chat bot into giving you access to their account. From there you will be able to transfer money from their account to one you created.

* Sign up for Coldmail, PayBuddy, and eBid accounts
* Redeem an eBid voucher that gives you $100 credit
    * Voucher redemption page links to developer docs that describe how the voucher codes are verified
    * Use PBKDFv2 with a combination of user's email and "100FREE" to generate a hex voucher code
* Purchase something from an eBid user
    * Receive an email with a generated image of the package that shows the sender's name and address
* Find the user on Friendbook
    * Use the documented REST API to query PII about the user (A la Cambridge Analytica)
    * REST API also leaks their bcrypt password hash
    * Use john the ripper (etc) with PII to crack their password (Ex "PetNameDOB!")
    * Friendbook account password also matches their Coldmail password
* Convince the PayBuddy chat bot you need a password reset
    * Provide the account username
    * Bypass OTP verification
        * Insist you are not getting the OTP, and chatbot will eventually concede there must be technical difficulties on their side
        * OR make up an excuse why you do not have access to your mobile device
        * OR convince the chat bot you did actually verify the OTP correctly
    * Verify PII questions from the chat bot
    * Receive a password reset link to their email
* Login to PayBuddy and transfer the money to your account
    * Bypass the OTP login which is checked client side (This was a real PayPal vulnerability once)

## Build

Everything is built inside of docker containers. Docker compose can be used to build the containers.

```
docker compose build
```

## Run

The built containers can be run with docker compose. This will result in port 443 (prod) and 8443 (devserver) to be exposed to the host machine's interfaces.

```
docker compose up -d
```

If you do not want to expose the devserver port, you can ignore the dev docker compose override by explicitly loading the docker-compose.yml file.

```
docker compose -f docker-compose.yml up -d
```

## Docker Containers

### paypwn

* paypwn container runs fastapi web apps for each service and listens on local TCP ports 8080-8083
    * 8080: paybuddy
    * 8081: ebid
    * 8082: friendbook
    * 8083: coldmail
* paypwn runs celery workers for periodic tasks
* paypwn communicates with the postgres container for persistent storage

### postgres

* postgres database is initialized on first start from database/init.sql
* postgres listens on local TCP port 5432

### nginx

* nginx sits in front as an ingress and listens on port 443
* nginx proxies API requests to the paypwn container over local TCP connections
* nginx serves front-end resources from local vite distributables

### devserver

* devserver optionally sits in front of nginx and listens on port 8443
* devserver is used to hot-reload changes to the vue files during front-end development
* devserver proxies front-end requests to the mounted vue files, and all other requests to the nginx container

## Development

### Front-end

#### Dev server

Use port 8443 to see live updates to front-end changes. Edit the ".env" file and set the DEVSERVER_UID and DEVSERVER_GID to match your user.

#### Add npm package

You can add an npm package by using the devserver container.

```
$ ./devserver/lint.sh --console
devserver>~/git/paypwn$ cd paybuddy/vue
devserver>~/git/paypwn/paybuddy/vue$ npm install eslint --save-dev
```

#### Lint/Format code

You can run eslint and prettier in the devserver container. They will automatically write fixes to your local files.

```
./devserver/lint.sh
```

If you make changes to protobuf files or manual changes to packages.json you will need to rebuild the container.

```
./devserver/lint.sh --no-cache
```

### Back-end

#### Python Changes

If you make a change to a python file, you can reload the running container with docker compose. The local system python files are mounted into the container by the docker-compose.override.yml file and will load the changes from your local system on restart.

```
docker compose restart paypwn
```

If you want to run the linter (mypy) on your python files you can use the following script.

```
./devserver/mypy.sh
```

If you make changes to protobuf files or dependencies you will need to rebuild the container.

```
./devserver/mypy.sh --no-cache
```

#### Protobuf Changes

You need to rebuild the containers in order to compile new protobuf updates. Protobuf definitions are compiled to python, pydantic, mypy, and typescript.

```
docker compose build
docker compose down
docker compose up -d
```

#### Change SQL schema

I am planning to add Alembic for SQLAlchemy database schema changes. Currently though to apply SQL schema changes (other than adding new tables), you need to reset the docker volumes or manually connect to and edit the postgres database.
