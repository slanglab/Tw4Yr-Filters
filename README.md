# Tw4Years-Filters

Code to accompany: Masis, Eggleston, Green, Jones, Armstrong, and O'Connor. "Large-scale Twitter data reveals systematic geographic and social variation in African American English." Currently under peer-review. 2023.

Contact: [Chloe Eggleston](https://chloes.computer/), Tessa Masis (tmasis@cs.umass.edu), Brendan O'Connor (brenocon@cs.umass.edu)

This software was used to filter an archive of Gardenhose messages to create the "Twitter4Years" dataset described as follows.

See also: https://github.com/slanglab/aae-twitter


# Description (copied from paper draft)

The Twitter4Years dataset is a corpus of approximately 227M tweets authored from May 2011 through April 2015 that are geolocated with latitude/longitude coordinates in the U.S., and with various metadata filters to help focus on "everyday" people (attempting to exclude, for example, celebrities and automated accounts). Messages’ locations have also been augmented with geographical shapefile lookups to TIGER/Line blockgroups distributed by the U.S. Census, and thus integrable with demographic information from Census data products at any level of its geographical hierarchy (blockgroups, tracts, counties, etc).

This dataset was constructed by filtering an archive of Twitter Gardenhose messages that were collected in realtime during the period 2011-2015; we call this the "initial archive." During this period, Twitter called the service "Gardenhose", a version of Twitter’s Sample Stream API whose documentation stated gave access to a 10\% sample of all publicly posted tweets.\footnote{Gardenhose may be technically similar to a later service called "Decahose"; see also discussion of limitations of sample stream randomness in \citet{morstatter2013sample, kergl2014endogenesis, pfeffer2018tampering}.} We used no query filters when obtaining data from the API.

A subset of this initial archive was used to create the 56M tweet corpus described in \citet{blodgett16}, which consisted of US geolocated tweets authored in the year 2013.
%(the paper’s website names this dataset “TwitterAAE corpus”, though only a subset of it was judged to contain AAE; see paper for details.) 
Other selections of this initial archive have been analyzed in earlier work as well, such as \citet{o2010tweets, eisenstein2010latent, eisenstein2014diffusion}. 

We now discuss the filtering and analysis to create Twitter4Years, which was performed in service of this work, derived from the initial archive. The collection decisions in this work follow broadly similar motivations as \citet{blodgett16}, with a number of differences and intended improvements. (It contains 92.8\% of messages in \citet{blodgett16}’s corpus.) From the initial archive, we filtered to messages fulfilling these criteria:

- Geotagged using latitude/longitude coordinates (often called “GPS coordinates”).
- Author had less than 5,000 followers when the tweet was authored.
- Message is not a retweet and its text does not contain any of the following words (case insensitive matching): `rt`, `follow`, `mention`.
- Message text has less than three hashtags.
- Message was authored from May 2011 through April 2015, a 48 month period.  We chose a multiple of 12 months as the duration in order to eliminate anomalous effects from annually occurring holidays or other cultural events. The specific range was chosen as one with a high prevalence of geotagged tweets within the initial archive. Outside this time range, users less frequently posted their location (perhaps due to software and user interface changes).
- The tweet’s authoring platform (Twitter client, the \emph{source} field in the API's tweet object) was limited to one of approximately two dozen typically used by everyday people, as opposed to automated marketing and other uses that sometimes publish to a particular location. The list was manually selected by examining the 125 most frequent authoring platforms, which make up approximately 99\% of the dataset. Our whitelist includes, for example, popular clients from the time that were used to access Twitter from the Web, iPhone, Blackberry, and Android, and excludes cross-posts from other social media platforms like Instagram and FourSquare, as well as social media hiring platforms like CareerArc.

This results in 227,253,198 messages (including duplicates); 226,631,796 deduplicated messages; and 7,414,332 unique authors.


# Whitelist description

The file `whitelist` contains the sources (Twitter client IDs) that are included.  The following describes these sources, with descriptions of each platform and their line number(s) in the `whitelist` file:

1. Official Client/Browser (1-15)
    - The official Twitter client, devices include iPhone, Android, Blackberry, Windows Phone, Nokia n40, Windows, iPad, Android Tablets, and Browsers 
2. TweetCaster (16,21,27)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20140221205743/https://tweetcaster.com/) [Google Play Store Archive](https://web.archive.org/web/20150314023306/https://play.google.com/store/apps/details?id=com.handmark.tweetcaster)
3. UberSocial (17,24,25,34,44,55)
    - A third party Twitter client. Includes versions for Blackberry, iOS, Android, as well as stand-alone skins for various media platforms (Sherlock Holmes, Tower Heist). [Website Archive](https://web.archive.org/web/20180201210152/https://www.ubersocial.com/)
4. Tweetbot (18,20,36,39)
    - A third party Twitter client. [Wikipedia](https://en.wikipedia.org/wiki/Tweetbot)
5. TweetDeck (19)
    - A third party Twitter client. Acquired by Twitter in 2011. [Wikipedia](https://en.wikipedia.org/wiki/TweetDeck)
6. NightfoxDuo (22,53)
    - A Japanese game that uses Twitter for a free-form social networking component. [Description](https://www.semanticscholar.org/paper/Detecting-Location-Spoofing-in-Social-Media%3A-of-an-Zhao/f9e30dbaec03da02d7610a6d063244bc664022ea/figure/1)
7. Echofon (23,50)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220302165541/https://echofon.com/)
8. Plume (26,30,37)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220307165409/https://myplume.com/)
9. Endomondo (28)
    - A fitness platform that allows users to update their exercise status to Twitter. [Wikipedia](https://en.wikipedia.org/wiki/Endomondo)
    - *Note:* Upon further review, this source does not strictly fit criteria for entry and should have been excluded. However, it only makes up 0.008% of the dataset, so we do not anticipate downstream analysis would be affected by this error.
10. UberTwitter (29,35)
    - Former version of UberSocial before rebranding. [Rebranding coverage](https://www.networkworld.com/article/2200143/twitter-whacks-ubertwitter-company-so-hard-it-s-changing-app-s-name-to-ubersocial.html), [additional coverage](https://everything-pr.com/uber-twitter/)
11. Gravity (31,38)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220522043832/http://mobileways.de/products/gravity/gravity/)
12. Tweetlogix (32)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220310000104/https://onloft.com/tweetlogix)
13. Hootsuite (33,46)
    - A social media management platform that allows for managing socia media accounts across platforms. [Wikipedia](https://en.wikipedia.org/wiki/Hootsuite)
14. Twittelator (40)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220308150101/https://stone.com/Twittelator/)
15. Twitbird (41,52)
    - A third party Twitter client. [News Coverage](https://www.americanexpress.com/en-us/business/trends-and-insights/articles/twitbird-a-twitter-client-for-the-best-of-us-1/), [additional coverage](https://methodshop.com/twitbird-pro/)
16. Twidroyd (42,43)
    - A third party Twitter client, eventually acquired by UberMedia and rebranded as UberSocial for Android. [Website Archive](https://web.archive.org/web/20220409053038/https://twidroid.com/)
17. A.plus (45)
    - A third party Twitter client for Desktop, eventually integrated into UberSocial as a theme. [Website Archive](https://web.archive.org/web/20110902011658/http://www.aplus-app.com:80/).
18. Seesmic (47)
    - A social media management platform, acquired by HootSuite in 2012. [Wikipedia](https://en.wikipedia.org/wiki/Seesmic)
19. twicca (48)
    - A third party Twitter client. [Play Store Archive](https://web.archive.org/web/20220208151759/https://play.google.com/store/apps/details?id=jp.r246.twicca&hl=en_US&gl=US)
20. Fenix (49)
    - A third party Twitter client. [Website Archive](https://web.archive.org/web/20220312112445/https://mvilla.it/fenix)
21. Tweetie (51)
    - A third party Twitter client. Acquired by Twitter in 2010. [Wikipedia](https://en.wikipedia.org/wiki/Tweetie)
22. Tweedle (54)
    - A third party Twitter client. [News Coverage](https://lifehacker.com/tweedle-makes-twitter-simple-stable-and-beautiful-for-1477800832)
​

# Usage

The pipeline is run in this order.  These notes describe data file locations on our internal server during development.

```
Filter 1: Geographical coordinates
	Script: geo.sh (originally at /home/ceggleston/geo.sh)
	Source Directory: /data/tweets/all
	Output Directory: /home/ceggleston/extracted

Filter 2: USA Located
	Script: usaify.py (originally at /home/ceggleston/usaify/usaify.py)
	Source Directory: /home/ceggleston/extracted
	Output Directory: /home/ceggleston/usa_extracted

Filter 3: Source Whitelist + RT/Follow/Mention + Followers Count + Hashtags Count
	Script: filters.py (originally at /home/ceggleston/samples/filters.py)
	Source Directory: /home/ceggleston/usa_extracted
	Output Directory: /home/ceggleston/dataset/tweets

Script 4: Attaching GEOIDs to each tweet for use in ACS data
	Script: gen_geoids.py (originally at /home/ceggleston/dataset/gen_geoids.py)
	Source Directory: /home/ceggleston/dataset/tweets
	Output Directory: /home/ceggleston/dataset/geoids
```
