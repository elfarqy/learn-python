import os
from bs4 import BeautifulSoup
import re
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import NewPost

TAG_RE = re.compile(r'<[^>]+>')

username = 'usernameHere'
password = 'passwordHere'
wp = Client('http://wp.local/xmlrpc.php', username, password)


def main():
    filePaths = []
    for root, dirs, files in os.walk("directory"):
        for file in files:
            if file.endswith(".html"):
                filePaths.append(os.path.join(root, file))
    return filePaths


def readFile():
    files = main()
    for file in files:
        soup = BeautifulSoup(open(file), "html.parser")
        contents = soup.find_all('div', {'class': 'entry'})
        currentDirectory = os.path.dirname(file)
        fileName = os.path.basename(currentDirectory)
        savePath = os.path.join('exported', "{n}.txt".format(n=fileName))
        tmpDocuments = []
        for content in contents:
            tmpDocuments.append(remove_tags(str(content)))

        with open(savePath, 'a') as the_file:
            the_file.write(" ".join(tmpDocuments))

        post = WordPressPost()
        
        post.title = str(fileName).replace('-',' ')
        post.content = " ".join(tmpDocuments)
        post.post_status = 'draft'
        
        wp.call(NewPost(post))

        # break


def remove_tags(text):
    return TAG_RE.sub('', text)


if __name__ == '__main__':
    readFile()
