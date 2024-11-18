import requests
from bs4 import BeautifulSoup
import pprint

# Fetch the content of Hacker News page 1
res = requests.get('https://news.ycombinator.com/')  # Get page 1 content
# Fetch the content of Hacker News page 2
res2 = requests.get('https://news.ycombinator.com/?p=2')  # Get page 2 content

# Parse the HTML content of page 1
soup = BeautifulSoup(res.text, 'html.parser')   # Parse page 1
# Parse the HTML content of page 2
soup2 = BeautifulSoup(res2.text, 'html.parser')  # Parse page 2

# Extract all links from the 'titleline' class on page 1
links = soup.select('.titleline > a')  # Grab all elements in 'titleline' class (page 1)
# Extract all vote subtext information from page 1
subtext = soup.select('.subtext')  # Grab all elements in 'subtext' class (page 1)

# Extract all links from the 'titleline' class on page 2
links2 = soup2.select('.titleline > a')  # Grab all elements in 'titleline' class (page 2)
# Extract all vote subtext information from page 2
subtext2 = soup2.select('.subtext')  # Grab all elements in 'subtext' class (page 2)

# Combine links and subtext from both pages
links_combined = links + links2  # Combine links from pages 1 and 2
subtext_combined = subtext + subtext2  # Combine subtext from pages 1 and 2

# Function to sort the stories by votes in descending order
def sort_stories_by_votes(hnlist):
    # Sorts the list of dictionaries by the 'votes' key in descending order
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Function to create a custom list of stories with titles, links, and votes
def create_custom_hacker_news(links, subtext):
    hn = []  # Initialize an empty list to hold the filtered stories
    for idx, item in enumerate(links):
        # Get the title of the story
        title = links[idx].getText()
        # Get the link to the story
        href = links[idx].get('href', None)
        # Find the vote count element in the subtext
        vote = subtext[idx].select('.score')
        if len(vote):  # Check if the story has a vote count
            # Extract the vote count and convert it to an integer
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:  # Filter stories with more than 99 votes
                hn.append({'title': title, 'link': href, 'votes': points})  # Add story to the list
    # Return the list of stories sorted by votes
    return sort_stories_by_votes(hn)

# Pretty print the final list of popular stories
pprint.pprint(create_custom_hacker_news(links_combined, subtext_combined))
