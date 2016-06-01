# This is a Adsnative demo generator tool
import urllib2
import webbrowser
import fileinput
import subprocess
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
if not 'website' in form:
	print "Content-Type: text/html" 
    print                              
    print'<h2>Please go back and enter a valid site\'s address.</h2>'
else:
    domain = form.getvalue("website")


http_domain = str('http://'+ domain)
domain_slash = str(http_domain+'/')
html = urllib2.urlopen(http_domain).read()


file = open('temp.html', 'w')
file.write(str(html))
file.close()

href_domain = str('href=\"'+http_domain)
href_domain_slash = str(href_domain+'/')

script_string = "<!--ADSNATIVE--><script type=\"text/javascript\"src =\"http://static.adsnative.com/static/js/render.v1.js\"></script><!--ADSNATIVE--></body>"

content_html = domain.strip('.com')
content_html = str(content_html+'.html')

f = open(content_html, 'w')
for line in fileinput.input('temp.html'):
	line = line.replace('href="/', href_domain_slash)
	line = line.replace('src="/', str('src="'+domain_slash))
	line = line.replace('</body>', str(script_string))
	f.write(str(line))

commit_message = 'auto adding '+content_html
subprocess.call('cd /Users/tarek/Repository/picatcha.github.io/preview', shell=True)
subprocess.call('git init', shell=True)
subprocess.call('git add '+content_html, shell=True)
subprocess.call('git commit -m \"'+commit_message, shell=True)
subprocess.call('git push picatcha master', shell=True)

#print("Contents written to file successfully.")
webbrowser.open(str('file:///Users/tarek/Repository/personal_workspace/'+content_html))