## the routine to download a pdf
# takes in the beautiful soup object and download path
# finds all links
# finds the link with .pdf
# downloads it
import urllib2
import os


def download(soup, download_path, file_name, jrnl):
    #print 'doing this'
    ## Download pdf routine

    save_to = download_path+'/'+jrnl
    # check for the existence of a directory which is the name of the journal
    if not os.path.isdir(save_to):
        os.mkdir(save_to)

    for tag in soup.find_all('a', href=True): 
        # find <a> tags with href in it 

        # now take all of those links and split them to find which link has .pdf in it
        linkname = os.path.basename(tag['href'])
        linksplit = os.path.splitext(linkname)

        ## if the link is a pdf then download it
        if linksplit[1] == '.pdf':
            ## open the url
            try:
                current = urllib2.urlopen(tag['href'])
                print "[****--] Downloading: ", file_name
                # download the document
                with open(save_to + '/' + file_name, 'wb') as f:
                    f.write(current.read())
            except urllib2.HTTPError as e:
                if e.code ==404:
                    print 'Paper 404, could not be downloaded.'
                    return 'no paper'
                else:
                    return 'no paper'
    return

#download(soup, download_path, jrnl, doJ)