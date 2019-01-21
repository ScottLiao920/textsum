from bs4 import BeautifulSoup, NavigableString, Tag
import urllib3
import os
global url_next
global file_no
file_no = 0
folder = "G:/URECA/textsum/CWD/corpus/"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def make_soup(web):
    http = urllib3.PoolManager()
    r = http.request("GET", web, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'})
    return BeautifulSoup(r.data, 'lxml')


def gettitle(soup):
    title = soup.title.get_text()
    return title


def generate_txt(name, url, date, article, count):
    try:
        name = name.replace("  ", " ").replace("\n", "").replace("\t", "")[0:100]
        new = folder + name + '.txt'
        if(os.path.exists(new)):
            print("File already exists!")
            return count
        else:
            file = open(new, 'w', errors='ignore')
            file.write(url)
            file.write('\n' + date)
            file.write('\n' + name)
            for i in article:
                text = i.get_text().replace('\xa0 ', ' ').encode('utf-8')
                text = text.decode('ascii', 'ignore')  # this is to delete all the /sa0 in unicode
                if not (text[0:8] == "Related:"):
                    file.write('\n' + text)
            file.close()
            count = count + 1
    except OSError:
        print("Illegal file name!")
    return count


url_next = "https://www.us-cert.gov/ncas/alerts"
while(url_next):
    target_list = make_soup(url_next).find_all("span", {"class": "document_title"})
    for target in target_list:
        next = "https://www.us-cert.gov" + target.a["href"]
        next_soup = make_soup(next)
        title = gettitle(next_soup).replace(" | US-CERT", "")
        temp = str(next_soup.footer.get_text())
        date = temp[23: temp.find("201") + 4]
        content = next_soup.find("div", {"id": "ncas-content"}).find_all("div", {"class": "field-item even"})
        print(generate_txt(title, next, date, content, file_no))
        file_no += 1
    url_next = make_soup(url_next).find("li", {"class": "pager-next"})
    if url_next:
        url_next = "https://www.us-cert.gov" + url_next.a["href"]
    else:
        print("All news are downloaded!")
    print(url_next)