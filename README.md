# Tw4Years-Filters

Code to accompany: Masis, Eggleston, Green, Jones, Armstrong, and O'Connor. "Large-scale Twitter data reveals systematic geographic and social variation in African American English." Currently under peer-review.

Contact: [Chloe Eggleston](https://chloes.computer/), Tessa Masis (tmasis@cs.umass.edu), Brendan O'Connor (brenocon@cs.umass.edu)

This software was used to filter an archive of Gardenhose messages to create the "Twitter4Years" dataset described as follows.

See also: https://github.com/slanglab/aae-twitter

# Description

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

