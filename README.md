Tabletki.UA orders checker

Telegram
Please provide YOUR bot token and chatid to send message to

Local env:
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

Docker/Portainer deployment:

>> We use nginx-lets-encrypt companion - so for seamless integration we need pre-create webproxy network
>> #docker network create webproxy --opt encrypted=true

PROD:
1. Copy env.dev file to env.prod. Modife variables inside env.prod
2. Source env file
#source env.prod
3. Run deploy to portainer via deploy.py script
#python deploy.py

DEV:
1. Edit env.dev file to set real values for DB host
#vim env.dev
2. Source env file and run docker-compose
#source env.dev && docker-compose -f docker-compose.dev.yml up
3. to rebuild - just rerun same container - as code mounted as folder to container
# tabletki_orders_checker
