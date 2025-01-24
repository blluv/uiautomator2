import os
import re
import requests
import zipfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
VERSION_FILE = BASE_DIR.parent / "version.py"
APK_VERSION = None
JAR_VERSION = "0.1.5"


with open(VERSION_FILE, "r", encoding="utf8") as f:
    for line in f:
        if "apk_version" in line:
            print(line)
            APK_VERSION = re.search(r"'([^\"]+)'", line).group(1)
            break

if not APK_VERSION:
    raise ValueError("APK_VERSION could not be determined from version.py")

print(f"APK_VERSION: {APK_VERSION}")


def download(url, output_path):
    print(f">> Downloading {url} -> {output_path}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def download_apk(version, name):
    url = f"https://github.com/openatx/android-uiautomator-server/releases/download/{version}/{name}"
    download(url, name)

    
    with zipfile.ZipFile(name, "r") as z:
        z.testzip()


def download_jar():
    url = f"https://public.uiauto.devsleep.com/u2jar/{JAR_VERSION}/u2.jar"
    download(url, "u2.jar")


if __name__ == "__main__":
    os.chdir(BASE_DIR)

    download_jar()
    download_apk(APK_VERSION, "app-uiautomator.apk")

    version_data = {
        "com.github.uiautomator": APK_VERSION
    }
    with open("version.json", "w") as f:
        f.write(f"{version_data}\n")
