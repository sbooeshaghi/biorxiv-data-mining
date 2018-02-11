## the routine to download a pdf
# takes in the beautiful soup object and download path
# finds all links
# finds the link with .pdf
# downloads it
import urllib2
import os


# for the scraper I am using, I modified this slightly to include jrnl and doJ 
# for creating new_file_name

def download(soup, download_path, jrnl, doJ):
    print 'doing this'
    ## Download pdf routine
    for tag in soup.find_all('a', href=True): 
        # find <a> tags with href in it 

        # now take all of those links and split them to find which link has .pdf in it
        linkname = os.path.basename(tag['href'])
        linksplit = os.path.splitext(linkname)

        ## if the link is a pdf then download it
        if linksplit[1] == '.pdf':
            ## open the url
            current = urllib2.urlopen(tag['href'])
            new_file_name = jrnl + str(doJ[jrnl]) + '.pdf'
            print "[****--] Downloading: ", new_file_name
            # download the document
            with open(download_path + '/' + new_file_name, 'wb') as f:
                f.write(current.read())
    pass

download(soup, download_path, jrnl, doJ)