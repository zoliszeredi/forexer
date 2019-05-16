Forexer Trading
===============


Requirements
------------
As it's configured to use docker-compose, you need it and docker readily available to start.
Before doing *up*, you need to set you Fixer API keys in the docker-compose.yml file.

Afterwards do:

docker-compose up -d

You need to create a superuser/user to access the Admin

docker-compose exec django ./manage.py createsuperuser

and don't forget to run the migrations

docker-compose exec django ./manage.py migrate


REST API [req1]
---------------


The Django Application exposes the following main REST endpoint:
http://forexer.lvh.me:8000/api/trades/

There are also specific endpoints for listing of currencies and rates:
- http://forexer.lvh.me:8000/djangoapp/quote/?sell_currency=EUR&buy_currency=CAD&sell_amount=10
- http://forexer.lvh.me:8000/djangoapp/available-currencies/


Trade App [req2,req3]
---------------------

There are two pages available, one for listing the other for creating trades:
- http://forexer.lvh.me:8000/djangoapp/
- http://forexer.lvh.me:8000/djangoapp/create/

I've added a ModelAdmin for it for quick viewing and searching.
The shabby styling is the best I could do with my limited css knowledge.
It works as described in the requirements document however it does not use the REST endpoints.
To extend the app to behave as a SPA, the *trade_form.html* and *trade_list.html* templates can be
used by replacing the django template language bits with event handler like in *actions.js*. One
retrieval function that does uses GET method for the paginated Trades, and another POST for the
creation of new trades


Rates Package [req4]
--------------------

The mechanism for determining the interchange rates is determined relative to the EUR. The free
plan from *forex.io* does not support conversion between two non EUR currencies.
To avoid reaching the limit of 1000 calls/month, I found out that I can use the daily refference
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml rates from the ECB's site and convert
it to *fixer.io* format. From what I could tell fixer.io is using ECB data anyway.
I concieved this as a stand-alone package as it does not have any coupling with django/webframeworks.

The key points are the *MarketOperation* and the *Rates* class.


Distribution [req5]
-------------------
Distribution of the forex app is done via a docker container.

docker build -f dockerfiles/Dockerfile-prod -t acme_corp/forexer:1 .
docker push acme_corp/forexer:1

Following the publication to a registry (Amazon Elastic Container, dockerhub, etc...) one can do other
orchestrations.

Alternatively, one could provisining/deployment using ansible, chef, fabric
