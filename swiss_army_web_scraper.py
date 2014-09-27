import requests
import lxml.html
import os

"""
Big idea - Write a generalized web scraper


web scraper functions:

1) download links
2) download images
3) download files
4) download tables

Concerns:
Big-Oh Notation
"""

def get_links(url,base_url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.text)
    links = html.xpath("//a/@href")
    for ind,val in enumerate(links):
        if not "http" in val:
            links[ind] = base_url + val
    return links

def get_images(url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.text)
    images = html.xpath("//img/@src")
    if not os.path.exists("images"):
        os.mkdir("images")
    os.chdir("images")
    for image in images:
        name = image.split("/")[-1]
        with open(name,"wb") as f:
            r = requests.get(image)
            f.write(r.content)
    os.chdir("../")

def get_tables(url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.text)
    tables = html.xpath("//table")
    if not os.path.exists("csv"):
        os.mkdir("csv")
    os.chdir("csv")
    #name is the number of the table on html page
    for name,table in enumerate(tables):
        head = table.xpath("/thead")
        if head != []:
            head_data = head.xpath("//tr//th")
            c_head_data = [i.text_content() for i in head_data]
        foot = table.xpath("/tfoot")
        if foot != []:
            foot_data = foot.xpath("//tr//td")
            c_foot_data = [i.text_content() for i in foot_data]
        body = table.xpath("/tbody")
        if body != []:
            body_data = body.xpath("//tr//td")
            c_body_data = [i.text_content() for i body_data]
        with open("table"+str(name)+".csv","w") as f:
            for i in c_head_data:
                f.write(i+" ")
            f.write("\n")
            for i in c_foot_data:
                f.write(i+" ")
            f.write("\n")
            for i in c_body_data:
                f.write(i+"\n")
    os.chdir("../")
