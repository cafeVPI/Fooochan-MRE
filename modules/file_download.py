from modules.path import modelfile_path, lorafile_path
import json, requests
import subprocess

def dl_command(url, dir, name):
    subprocess.run(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {url} -d {dir} -o {name}".split())

def download_urls(urltext, model_id):
    result = ""
    paths = [modelfile_path, lorafile_path]
    num = 0
    urls = urltext.split('\n')
    if not urltext == "":
        maxn = len(urls)
        for url in urls:
            file_name = url.split('/')[-1]
            if file_name == "":
                continue
            if file_name.split('.')[-1] == file_name:
                response = requests.get(f"https://civitai.com/api/v1/model-versions/{file_name}")
                res = response.json()
                file_name = res['files'][0]['name']
            dl_command(url, paths[model_id], file_name)
            num += 1
            result = result + f"\n{file_name}"
    num = 0
    return result

def download_model_lora(t0,t1):
    result = ""
    i = 0
    ts = [t0,t1]
    for t in ts:
        res = download_urls(t, i)
        result = result + "\n" + res
        i += 1
    return result
