import requests
from bs4 import BeautifulSoup
import pandas as pd

baseURL = 'https://github.com/'  # Github domain
columnHeadings = ['Repo', 'URL', 'Language', 'Description']  # define data frame column headings

# get user input
while True:
    userName = input("Enter Github user name: ")

    url = baseURL + userName  # generate full url
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
repositoryURL = ''

numRepos = 0  # variable to count number of repositories (also used as data frame index)

# find repo page url
for tag in soup.find_all('a', {'data-tab-item': 'repositories'}):
    repositoryURL = tag.get('href')

# construct repositories url (remove trailing '/' on base URL to avoid double slash)
url = baseURL.removesuffix('/') + repositoryURL

print('Repositories url link: ', url, end='\n\n')  # put link in console

# instantiate a Pandas object
summaryTable = pd.DataFrame(columns=columnHeadings)

while True:
    # Send a new GET request to repositories url
    response = requests.get(url)

    html_doc = response.text  # extract html contents
    soup = BeautifulSoup(html_doc, 'html.parser')  # use BeautifulSoup to parse html

    # find all user repositories and extract summary details (name, url, language, description)
    for tag in soup.find_all('li', {'itemprop': "owns"}):
        repoName = tag.find('a')
        repoName = repoName.string.lstrip()
        repoURL = tag.find('a', {'itemprop': 'name codeRepository'})
        repoURL = baseURL.removesuffix('/') + repoURL.get('href')
        repoLanguage = tag.find('span', {'itemprop': 'programmingLanguage'})
        repoLanguage = repoLanguage.string.lstrip()
        repoDescription = tag.find('p', {'itemprop': 'description'})
        if repoDescription is not None:
            repoDescription = repoDescription.string.lstrip()
            repoDescription = repoDescription.rstrip()

        # output to console
        print(repoName, repoURL, repoLanguage, repoDescription)

        # populate data frame
        summaryTable.at[numRepos, 'Repo'] = repoName
        summaryTable.at[numRepos, 'URL'] = repoURL
        summaryTable.at[numRepos, 'Language'] = repoLanguage
        summaryTable.at[numRepos, 'Description'] = repoDescription
        numRepos += 1  # count number of repositories found

    # check for another page of repositories
    nextPage = soup.find('a', class_='next_page')

    if nextPage:
        # construct url for next page and continue in while loop
        url = baseURL.removesuffix('/') + nextPage.get('href')
    else:
        break

print(f'\nNumber of repositories found = {numRepos}\n')

print(summaryTable)

# export captured data to .csv file
summaryTable.to_csv(userName + '.csv', index=False)

print('\nWrote data to file: capturedData.csv.')
