import requests
from bs4 import BeautifulSoup
import pandas as pd

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

print(type(mydataset))

myvar = pd.DataFrame(mydataset)

print(myvar)

print(type(myvar))

baseURL = 'https://github.com/'  # Github domain

# get user input
while True:
    url = input("Enter Github user name: ")

    url = baseURL + url  # generate full url
    print(url, end='\n\n')

    # Send a GET request to the full/generated url (i.e. user's github landing page)
    response = requests.get(url)

    # check for server response
    if response.status_code == requests.codes.ok:
        break
    else:
        print('No response from ' + url)

# process server response
html_doc = response.text  # extract html contents
soup = BeautifulSoup(html_doc, 'html.parser')  # use BeautifulSoup to parse html

# variable to hold repo url
repoURL = ''

# find repo page url
for tag in soup.find_all('a', {'data-tab-item': 'repositories'}):
    repoURL = tag.get('href')

# construct repositories url (remove trailing '/' on base URL to avoid double slash)
url = baseURL.removesuffix('/') + repoURL

print('Repositories url link: ', url, end='\n\n')  # put link in console

# Send a GET request to repositories url
response = requests.get(url)

html_doc = response.text  # extract html contents
soup = BeautifulSoup(html_doc, 'html.parser')  # use BeautifulSoup to parse html

numRepos = 0  # variable to count number of repositories

columnHeadings = ['Repo', 'URL']
summaryTable = pd.DataFrame(columns=columnHeadings)

# find all public repositories, print names and url's
for tag in soup.find_all('a', {'itemprop': 'name codeRepository'}):
    print(tag.string.lstrip(), baseURL.removesuffix('/') + tag.get('href'))
    # save repository information in data frame summary table
    summaryTable.loc[numRepos] = tag.string.lstrip(), baseURL.removesuffix('/') + tag.get('href')
    numRepos += 1  # count number of repositories found

print(f'\nNumber of repositories found = {numRepos}\n')

print(summaryTable)

print(type(summaryTable))

summaryTable.to_csv('capturedData.csv', index=False)
