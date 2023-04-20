# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joslopez <joslopez@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/19 19:12:23 by joslopez          #+#    #+#              #
#    Updated: 2023/04/19 19:17:12 by joslopez         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib.request
import shutil

def download_image(url, path):
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)

def download_images(url, depth, base_path, allowed_extensions):
    
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    if parsed_url.scheme == 'file':
        web = 0
        try:
            with urllib.request.urlopen(url) as response:
                f = response.read()
        except:
            exit()        
        soup = BeautifulSoup(f, 'html.parser')
    else:
        web = 1
        try:
            response = requests.get(url)
        except:
            exit()
        soup = BeautifulSoup(response.content, 'html.parser')
    img = soup.find_all('img')
    print(f"Total {len(img)} Image(s) Found for this branch!")
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if not img_url:
            continue
        _, ext = os.path.splitext(img_url)
        if ext.lower() not in allowed_extensions:
            continue
        if web == 0:
                image_name = os.path.basename(img_url)
                url = url.replace("file://", "")
                img_url = img_url.replace("file://", "")
                item_path = os.path.join(os.path.dirname(url), img_url)
                try:
                    dest_path = os.path.join(base_path, image_name)
                    if not os.path.exists(dest_path):
                        try:
                            shutil.copy2(item_path, dest_path)
                        except:
                            print(f"Error in {item_path}")
                except:
                    pass
        else:
            img_path = os.path.join(base_path, os.path.basename(img_url))
            download_image(img_url, img_path)
        
    if depth > 0:
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            href = urljoin(base_url, href)
            if href.startswith(base_url):
                download_images(href, depth - 1, base_path, allowed_extensions)
    

def main():
    parser = argparse.ArgumentParser(description='Spider program to extract images from a website')
    if parser.add_argument('-r', action='store_true', help='recursively download images'):
        parser.add_argument('-l', nargs="?", const = 5, type=int, help='maximum recursion depth')
    parser.add_argument('-p', default='./data/', nargs="?", const='./data/', help='download path')
    parser.add_argument('url', nargs="?", help='URL to extract images from')
    args = parser.parse_args()
    
    if str.startswith(args.p, "http") or str.startswith(args.p, "file://"):
        args.url = args.p
        args.p = "./data/"
        
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    if not os.path.exists(args.p):
        os.makedirs(args.p)

    if args.url and args.l and args.p:
        download_images(args.url, args.l, args.p, allowed_extensions)
    elif args.url and args.p and not args.l:
        download_images(args.url, 0, args.p, allowed_extensions)

    if args.r:
        print(f'Downloading recursively with depth {args.l}')
    else:
        print('Downloading non-recursively')

if __name__ == '__main__':
    main()
