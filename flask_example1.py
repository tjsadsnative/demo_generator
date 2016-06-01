from flask import Flask, request, render_template
import urllib2
import fileinput
import subprocess
import webbrowser

siteName = 'cleverbot.com'


def getPubPage():
    global siteName
    http_domain = str('http://' + siteName)
    domain_slash = str(http_domain + '/')
    html = urllib2.urlopen(http_domain).read()

    file = open('temp.html', 'w')
    file.write(str(html))
    file.close()

    href_domain = str('href=\"' + http_domain)
    href_domain_slash = str(href_domain + '/')

    script_string = "<!--ADSNATIVE--><script type=\"text/javascript\"src =\"http://static.adsnative.com/static/js/render.v1.js\"></script><!--ADSNATIVE--></body>"

    global content_html

    if siteName.endswith('.com') or siteName.endswith('.org') or siteName.endswith('.net'):
        siteName = siteName[:-4]
    content_html = str(siteName + '.html')
    f = open(content_html, 'w')
    for line in fileinput.input('temp.html'):
        line = line.replace('href="/', href_domain_slash)
        line = line.replace('src="/', str('src="' + domain_slash))
        line = line.replace('</body>', str(script_string))
        f.write(str(line))


def upload2Github():
    commit_message = 'auto adding ' + content_html
    subprocess.call('cd /Users/tarek/Repository/picatcha.github.io/preview', shell=True)
    subprocess.call('git add ' + content_html, shell=True)
    subprocess.call('git commit -m \"' + commit_message, shell=True)
    subprocess.call('git push origin master', shell=True)

    # print("Contents written to file successfully.")
    webbrowser.open(str('file:///Users/tarek/Repository/personal_workspace/' + content_html))


def generatePreviewPage():
    getPubPage()
    upload2Github()


app = Flask(__name__)

@app.route("/generateDemo/")
@app.route("/generateDemo")
def form():
    return render_template("generateDemo.html")


# route below needs template changes
@app.route("/generateDemo/<siteName>")
def siteName(siteName=None):
    generatePreviewPage()
    return render_template("scrape_completed.html", siteName=siteName)
    upload2Github()


#    return render_template("website.html", domain=domain)

@app.route("/")
def index():
    return "Method used is %s" % request.method


@app.route("/veggie", methods=['GET', 'POST'])
def veggie():
    if request.method == "POST":
        return "You are using POST"
    else:
        return "You are probably using GET"


if __name__ == '__main__':
    app.run(debug=True)
