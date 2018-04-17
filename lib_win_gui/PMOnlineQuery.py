# -*- coding: cp936 -*-
from Bio import Entrez
from Bio import Medline
import urllib
from urllib2 import Request
from urllib2 import HTTPError
from urllib2 import URLError
import Tkinter as tk
import tkMessageBox
#import GUI
import time

import logging
#logging.basicConfig(fmt="%(level)s %(asctime)s %(message)s", level=logging.DEBUG)

global TERM
global max_count
global mailAd

TERM = vars()
max_count = int()
mailAd = vars()
resultContent = vars()

#content = vars()
#mailAd = 'Sample@mail.com'
#TERM = 'fever'
#max_count = 10


def queryOnline(max_count, TERM, mailAd, window, labelFb):
    global resultContent
    resultContent = " "
    # Set the maximum number of searching results
    # Set the searching key wordscontaining
    term_alert= 'Getting {0} publication(s) containing  {1}...\n' \
                'Please wait...'.format(max_count, TERM)
    print term_alert
    labelFb.config(text=term_alert, fg='#067a64')
    window.update_idletasks()
    # Output format2

    #####################Query Part######################

    Entrez.email = mailAd

    h = Entrez.esearch(db='pubmed', retmax=max_count, term=TERM)
    result = Entrez.read(h)
    # return the result
    result_alert='Total number of publications containing {0}: {1}\n' \
                 'Please wait...'.format(TERM, result['Count'])
    print result_alert
    labelFb.config(text=result_alert, fg='#067a64')
    window.update_idletasks()
    ids = result['IdList']
    h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
    resultContent = h.read()
    #    time.sleep(5)
    success_alert = "Your query result is ready to download.\nWhen you are ready, click the DOWNLOAD! button."
    #    logging.info("Start")
    labelFb.config(text=success_alert, fg='#067a64')
    #    logging.info("end")
    #    time.sleep(5)
    print success_alert
    #    time.sleep(5)
    return resultContent


def queryOnline2(max_count, TERM, mailAd, window, labelFb):
    try:
        logging.info("queryOnline start")
        print "===============> queryOnline start"
        queryOnline(max_count, TERM, mailAd, window, labelFb)
        logging.info("queryOnline finished")
    except HTTPError as e:
        print "================> %r" % e
        warningHTTP = "There is an HTTP error\n" + str(e.code)
        print(e.code)
        labelFb.config(
            text="Search is terminated.please try later.(HTTPError)", fg="red")
        window.update_idletasks()
        tkMessageBox.showinfo('Oops!', warningHTTP, parent=window)
    except URLError as e:
        print "================> %r" % e
        warningURL = "There is an URL error\n" + str(e.reason)
        print(e.reason)
        labelFb.config(
            text="Search is terminated, please try later.(URLError)", fg="red")
        window.update_idletasks()
        tkMessageBox.showinfo('Oops!', warningURL, parent=window)


if __name__ == "__main__":
    queryOnline2(max_count, TERM, mailAd, window, labelFb)
