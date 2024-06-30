# python_Pandas
Simple Python script using Pandas to create and build a summary table of web data gathered from github user pages (e.g. repositories, url's, etc) and write captured data to a .csv file.  

Console input requests a github user name. Response method in requests package returns web page html.

BeautifulSoup html parser is used to locate tags associated with desired user information and feed the Pandas data frame.

Repository names and clickable url's are output to the console in addition to being placed in the Pandas summary table.

Finally, captured data is written to a .csv file.