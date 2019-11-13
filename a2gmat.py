import os
import requests
import json
import re
import shutil
import urllib

from pprint import pprint
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve


DOMAIN = 'https://a2gmat.teachable.com/'


def not_exist_create_folder(path):
    if not os.path.isdir(path):
        print(path)
        os.mkdir(path)
    return

def download(url, path):
    try:
        urlretrieve(url=url, filename=path)
        sleep(2)
    except urllib.error.HTTPError as e:
        print('urllib.error.HTTPError', e)
        input('paused')

def main():
    browser = webdriver.Chrome(os.popen('which chromedriver').read().strip())

    # login
    login_url = 'https://sso.teachable.com/secure/135194/users/sign_in?flow_school_id=135194'
    browser.get(login_url)
    elem = browser.find_element_by_id('user_email')
    elem.send_keys(ACCOUNT)
    elem = browser.find_element_by_id('user_password')
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.RETURN)

    # target-homepage
    target = 'https://a2gmat.teachable.com/courses/597007/lectures/10709076'
    browser.get(target)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    for sidebar in soup.find_all('div', 'col-sm-12 course-section'):
        title = sidebar.find('div', 'section-title').text.strip()
        print('')
        print('*' * 100)

        if title in ['錄音檔下載區']:
            continue

        # lv1
        title.replace('/', '-')
        folderLv1 = os.path.join(A2GMAT, title)
        not_exist_create_folder(folderLv1)

        for sub in sidebar.find_all('li'):
            sub = sub.find('a', 'item')
            sub_url = DOMAIN + sub.get('href')
            sub_title = ' '.join(sub.text.split()).replace('/', '-')

            # lv2 --create folder
            folderLv2 = os.path.join(folderLv1, sub_title)
            not_exist_create_folder(folderLv2)

            browser.get(sub_url)
            sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')

            # write description
            description = soup.find('div', 'lecture-text-container')
            if description:
                with open(os.path.join(folderLv2, 'description.txt'), 'w+') as f:
                    f.write(str(description.text).strip())

            # save mp3, pdf file
            for sub_content in soup.find_all('a', 'download'):
                print(sub_content)
                fileName = sub_content.get('data-x-origin-download-name')
                print(fileName)
                filePath = os.path.join(folderLv2, fileName)
                fileUrl = sub_content.get('href')
                download(fileUrl, filePath)

            # save mov file
            for sub_content in soup.find_all('script', 'w-json-ld'):
                sub_content = json.loads(sub_content.text)
                fileName = sub_content['name']
                wistiaUrl = sub_content['embedUrl']

                # lv3
                browser.get(wistiaUrl)
                sleep(1)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                fileUrl = None
                backup = None
                for wistia_content in soup.find_all('script'):
                    if '.bin' in wistia_content.text:
                        wistia_content = wistia_content.text.strip()
                        wistia_content = wistia_content.split('W.iframeInit(')[1]
                        wistia_content = wistia_content.split(', {}')[0]
                        wistia_content = json.loads(wistia_content)
                        for c in wistia_content['assets']:
                            if c['display_name'] == 'Original file':
                                fileUrl = c['url']
                                backup = c
                if fileUrl:
                    print('- * -' * 5)
                    print('wistiaUrl', wistiaUrl)
                    print('fileName', fileName)
                    print('fileUrl', fileUrl)
                    movPath = os.path.join(folderLv2, fileName)
                    download(fileUrl, movPath)
                else:
                    pprint(soup.find_all('script'))
                    input('paused')

    browser.close()
    return


if __name__ == '__main__':
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
    A2GMAT = os.path.join(SCRIPT_FOLDER, 'a2gmat')
    if os.path.isdir(A2GMAT):
        shutil.rmtree(A2GMAT)
    os.mkdir(A2GMAT)

    ACCOUNT = '*'
    PASSWORD = '*'
    main()
