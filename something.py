#!/usr/bin/env python3
from pathlib import Path
import time
import os
import markdown
import re
import tarfile

# Files, which should not be indexed in either of the lists
forbiddenFiles = ["index.md", "contact.md"]
address = "http://nichtkursiv.link"
rssFeedLocation = "output/feed.xml";
inputDirPath = "input";
outputDirPath = "output";
headerPath = "templates/header.html";
headerIndexPath = "templates/header_index.html"
footerIndexPath = "templates/footer_index.html"
footerPath = "templates/footer.html";
currentTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
def getFileContent(filename):
  try:
    with open(filename, "r", encoding="utf-8") as file:
      return file.read()
  except FileNotFoundException:
    print(f"ERROR: File {file} not found")  
    return ""
def mdSuffix2HTMLSuffix(filename):
  editedFilename = os.path.splitext(filename)[0]+".html"
  return editedFilename
def getTitleFromMDFile(filename):
  try:
    with open(filename, "r", encoding="utf-8") as file:
      return re.sub(r"(# )", "", file.readline()).replace("\n", "")
  except FileNotFoundException:
    print(f"ERROR: File {file} not found")
    return ""
def generateRSS():
  with open(f"{outputDirPath}/rss.xml", "w", encoding="utf-8") as file:
    # I am aware that using this function in bulk is unelegant or
    # unpythonic or whatever, but it seems to be the easiest solution to
    # the formatting issues in the previous code.
    file.write(f"<?xml version='1.0' encoding='UTF-8' ?> \n");
    file.write(f"<rss version='2.0'> \n")
    file.write(f"<channel> \n")
    file.write(f"<title>{getTitleFromMDFile(inputDirPath + '/index.md')}</title> \n")
    file.write(f"<description>Nothing to see here</description> \n")
    file.write(f"<link>{address}/rss.xml</link> \n")
    file.write(f"<lastBuildDate>{currentTime}</lastBuildDate> \n")
    file.write(f"<pubDate>{currentTime}</pubDate> \n")
    file.write(f"<generator>something.py</generator> \n")
    file.write(f"<ttl>1800</ttl> \n")
    for fileIter in os.listdir(inputDirPath):
      filePath = os.path.join(inputDirPath, fileIter)
      filePathBase = os.path.basename(filePath)
      if os.path.isfile(filePath) and filePath not in forbiddenFiles:
        file.write(f"<item> \n")
        file.write(f"<title>{getTitleFromMDFile(filePath)}</title> \n")
        file.write(f"<description>Another post on {address}</description>\n")
        file.write(f"<link>{address}/{mdSuffix2HTMLSuffix(filePathBase)}</link>\n")
        file.write(f"<guid isPermaLink='false'> \n")
        file.write(f"{address}/{mdSuffix2HTMLSuffix(filePathBase)}\n")
        file.write(f"</guid> \n")
        file.write(f"<pubDate>{currentTime}</pubDate> \n")
        file.write(f"</item> \n")
        print(f"RSS: Added {filePathBase} to the feed.")
    file.write("</channel> \n")
    file.write("</rss>") 
    print("RSS: Finished generating the RSS Feed")
def generateAtom():
  with open(f"{outputDirPath}/atom.xml", "w", encoding="utf-8") as file:
    file.write(f"<?xml version='1.0' encoding='utf-8'?> \n")
    file.write(f"<feed xmlns='http://www.w3.org/2005/Atom'> \n")
    file.write(f"<title>{getTitleFromMDFile(inputDirPath + '/index.md')}</title>")
    file.write(f"<link href='{address}/atom.xml' rel='self'/> \n")
    file.write(f"<updated>{currentTime}</updated> \n")
    file.write(f"<author> \n")
    file.write(f"<name>{address}</name> \n")
    file.write(f"</author> \n")
    file.write(f"<id>{address}</id> \n")
    for fileIter in os.listdir(inputDirPath):
      filePath = os.path.join(inputDirPath, fileIter)
      filePathBase = os.path.basename(filePath)
      if os.path.isfile(filePath) and filePath not in forbiddenFiles:
        file.write(f"<entry>\n")
        file.write(f"<title>{getTitleFromMDFile(filePath)}</title>\n")
        file.write(f"<content type='html'>Another post on{address}</content>\n")
        file.write(f"<link href='{address}/{mdSuffix2HTMLSuffix(filePathBase)}'>") 
        file.write(f"</link>\n")
        file.write(f"<id>{address}/{mdSuffix2HTMLSuffix(filePathBase)}</id>\n")
        file.write(f"<updated>{currentTime}</updated>\n")
        file.write(f"<published>{currentTime}</published>\n")
        file.write(f"</entry>\n")
        print(f"Atom: Added {filePathBase} to the feed.")
    file.write(f"</feed>")
    print("Atom: Finished generating the Atom feed")
def generateHTML():
  for fileIter in os.listdir(inputDirPath):
    filePath = os.path.join(inputDirPath, fileIter)
    if os.path.isfile(filePath) and filePath not in forbiddenFiles:
      # This code below is for generating the HTML files
      header = (getFileContent(headerPath).replace("TITLEHERE",
        os.path.basename(fileIter)
      ))
      main = markdown.markdown(getFileContent(filePath))
      footer = getFileContent(footerPath)
      htmlFile = mdSuffix2HTMLSuffix(fileIter)
      with open(os.path.join(outputDirPath, htmlFile), 
                "w", encoding="utf-8") as file:
        file.write(header + main + footer)
        print(f"HTML: Generated the page for {str(htmlFile)}")
  print("HTML: Finished generating HTML files")
def generateIndex():
  header = getFileContent(headerIndexPath).replace("TITLEHERE", address)
  index = markdown.markdown(getFileContent(f"{inputDirPath}/index.md"))
  footer = (getFileContent(footerIndexPath).replace("LASTGENDATE", 
    currentTime
  )) 
  with open(os.path.join(outputDirPath, "index.html"), 
    "w", encoding="utf-8") as file:
      file.write(header)
      file.write(index)
      file.write("<ul>\n")
      for fileIter in os.listdir(inputDirPath):
        if fileIter not in forbiddenFiles:
          link2File = mdSuffix2HTMLSuffix(fileIter)
          linkName = Path(os.path.basename(fileIter)).with_suffix('')
          file.write(f"<li><a href='{link2File}'>{linkName}</a></li>\n")
          print(f"Index: Added {linkName} to the list on the index page")
      file.write("</ul>\n")
      file.write(footer)
      print("Index: Finished listing links on the index page")
def generateTarGZ():
  with tarfile.open(f"{outputDirPath}/website_repo.tar.gz", "w:gz") as tar:
    for file in os.listdir("."):
      print(f"ARCHIVE: Added {file} to the .tar.gz archive")
      tar.add(file)
  print("ARCHIVE: Finished generating the .tar.gz archive")
if __name__ == "__main__":
  generateHTML()
  generateIndex()
  generateRSS()
  generateAtom()
  generateTarGZ()
