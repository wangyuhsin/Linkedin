# Define constants
# Your LinkedIn email and password
EMAIL = "..."
PWORD = "..."

# LinkedIn cookies
# Check https://help.delpha.io/s/article/How-to-access-your-LinkedIn-Cookie to learn how to get your cookies
LI_AT = "AQEDASQhyy..."
JSESSIONID = "ajax:683..."

# The number of profiles to scrape
# Please set a value less than 1000
SCRAPE_NUM = 50

# The URL of LinkedIn search results page you want to scrape
# Need to filter 'Connections', 'Locations', 'Current company' on LinkedIn people search beforehand
# Make sure to decode the search URL (https://www.urldecoder.io/)
SEARCH_URL = 'https://www.linkedin.com/search/results/people/?currentCompany=["18013280","675562","29296664","17988315","9398436","11130470","807257","3991822","18542592","11869260","309694","3254263","2135371","1815218"]&geoUrn=["90000084"]&keywords=Full Stack Engineer OR AI Engineer OR ML Engineer OR Front-End Engineer OR Backend Engineer&network=["S","O"]&origin=FACETED_SEARCH&sid=zW9'

# Top 50 engineering schools
TARGET_SCHOOLS = {
    "Massachusetts Institute of Technology",
    "Stanford University",
    "University of California, Berkeley",
    "Purdue University",
    "Carnegie Mellon University",
    "Georgia Institute of Technology",
    "Caltech",
    "University of Michigan",
    "The University of Texas at Austin",
    "Texas A&M University",
    "University of Illinois Urbana-Champaign",
    "UC San Diego",
    "Cornell University",
    "The Johns Hopkins University",
    "University of Southern California",
    "UCLA",
    "Columbia University",
    "Northwestern University",
    "University of Colorado Boulder",
    "University of Maryland",
    "University of Pennsylvania",
    "Duke University",
    "Harvard University",
    "Princeton University",
    "North Carolina State University",
    "University of Washington",
    "The Ohio State University",
    "UC Santa Barbara",
    "University of Wisconsin-Madison",
    "Rice University",
    "Virginia Tech",
    "Northeastern University",
    "Penn State University",
    "Boston University",
    "University of California, Davis",
    "UC Irvine",
    "New York University",
    "University of Dayton",
    "University of Minnesota",
    "University of Virginia",
    "Arizona State University",
    "University of Delaware",
    "University of Rochester",
    "Vanderbilt University",
    "Yale University",
    "Iowa State University",
    "University of Florida",
    "University of Notre Dame",
    "University of Pittsburgh",
    "Wichita State University",
}
