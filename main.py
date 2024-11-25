import re
import os
import glob
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor


headers = {
    "DNT": "1",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "X-Sorry": "If you find this traffic annoying, please visit https://github.com/lolinekord/pyNCS/"
}

def get_html() -> None:
    """
    Stores HTML files such as song information in the local directory.
    """
    # Get the maximum page count
    res = requests.get("https://ncs.io/music", headers=headers).text
    pages = res.split("<ul class=\"pagination\">")[1].split("</ul")[0]
    max_pages: str = re.findall("\d+</a>", pages)[-1].split("</a>")[0]
    print("[+] Max pages: "+max_pages) 
    
    i = 1
    while i < int(max_pages)+1:
        res = requests.get("https://ncs.io/music?page="+str(i), headers=headers)  # Based on the number of pages retrieved, the actual content is archived to a local directory.
        with open(f"./ncs_html/{i}.html", "w", encoding="utf-8") as f:
            f.write(res.text.replace(" ", "").replace("\r", "").replace("\n", ""))
        print("[+] Saved: https://ncs.io/music?page="+str(i))
        i += 1


def get_tid(html: str) -> list[str]:
    """
    Get the tid from a locally archived HTML file.
    """
    # music list
    music_list = html.split("<h5>RecentReleases<divclass=\"grid-list\">")[1].split("</article>")[0]
    
    # get tid
    tid = re.findall(r"data-tid=\"([\da-z-]+)\"data-versions=", music_list)
    return tid
    


def download_ncs(tid: str) -> None:
    """
    Download the file based on the saved tid.
    """
    with requests.get("https://ncs.io/track/download/"+tid, headers=headers, stream=True) as res:
        filename = res.headers["content-disposition"].split("filename=\"")[1][:-1]
        print("[+] Downloading: "+filename)

        with open("./output/"+filename, "wb") as f:
            for chunk in res.iter_content(chunk_size=2048*2048):
                f.write(chunk)

    print("[+] File saved: ./output/"+filename)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A Python script to download all music files from the NCS official site.")
    parser.add_argument("--mode", type=str)
    
    args = parser.parse_args()

    if args.mode == "fetch":
        print("[+] Fetch the HTML file")
        input("[!] Pless Enter to start")

        get_html()

        input("[!] done")

    elif args.mode == "parse":
        print("[+] Extract tid")
        input("[!] Pless Enter to start")

        html_files = [p for p in glob.glob("./ncs_html/**.html", recursive=True) if os.path.isfile(p) and re.search("\d+\.html", p)]
        
        titleids = []
        for html_file in html_files:
            tidy = get_tid(open(html_file, "r", encoding="utf-8").read())
            titleids += tidy
        with open("./ncs_titles.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(titleids))
        print("[+] ncs_titles.txt saved")
        
        input("[!] done")

    elif args.mode == "download":
        print("[+] Download NCS")
        input("[!] Press Enter to start. This will take time and traffic to download all the songs.")

        tids = open("./ncs_titles.txt", "r", encoding="utf-8").read().splitlines()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            for tid in tids:
                executor.submit(download_ncs, tid)
        executor.shutdown()

        input("[!] done")

