# pardner-site

## About

This site is a prototype for a service that researchers could host to collect
personal data donations, using OAuth and service APIs to get user consent to
pull personal data directly from the services where the data is hosted.  For
the kinds of personal data available from APIs, this presents an opportunity
to streamline the experience of donating data.   A participant may be recruited
to join a research study because they use a specific service, but they may also
be recruited by a clinic, a professor, or any other kind of outreach based on
the study's profile for participants.  Once recruited and visiting the study's
data donation Web page, only a few clicks are needed for the user to log in
privately to the data platform and consent for the data to be transferred. The
process could take less time than the average online research questionnaire and
share only the information that the user consented to.

As a proof-of-concept, the implementation currently has some limitations that
could be overcome with more investment.

* Data is not anonymized on receipt (though it could be depending on the
research purpose)
* There's no data deletion request implemented yet (though that could be done
by email instead)
* Data is pulled one-time, though access tokens may allow repeat access

So far, this prototype has only implemented data requests for services that
have OAuth/HTTP APIs and low barriers to 3rd party API access.  If the site
was hosted by an actual research organization able to apply to services for
3rd party API access, many kinds of data could be available including:

* Messages, social media posts and comments, block lists and follow lists,
from social media and forum sites like Tumblr, Instagram, Tiktok, Reddit
and more
* Personal Internet usage history such as search history, AI conversations
media views, music/podcast listens, ad impressions
* Heart rate or blood-glucose or other health monitor data
* Exercise or food tracking apps like Strava

We're starting to talk about the future of this kind of approach.  There's
definite benefit to multiple researchers banding together - they can share
the expense of securing the Web site and database, and transforming the kind
of data they need into what the research studies require. Also it might just
be a matter of an extra checkbox to ask for user consent to allow multiple
studies access to the data they're donating.  A research institution 
specializing in a particular kind of personal data (e.g. online safety data,
or health tracking data) has an opportunity to really benefit multiple
research efforts with the same data donation site and pool of participants.

Contact the [Data Transfer Initiative](https://dtinit.org/contact-us) and
let us know your thoughts or interest!

## Setup
To run locally, first install dependencies with pip:

```bash
python -m pip install -r requirements.txt
```

Then, initialize the local database:

```bash
python manage.py migrate
```

Finally, start the local development server:

```bash
python manage.py runserver
```

## Administration
To access the admin site, create a superuser account:

```bash
python manage.py createsuperuser
```

Then visit /admin and log in with your credentials.
