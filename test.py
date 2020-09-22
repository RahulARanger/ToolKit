import webbrowser

new=2

print("1.Youtube\n2.Twitter\n3.Linkedin\n")

n=int(input("Enter the number: "))

if(n==1):
	url="http://www.youtube.com"
elif(n==2):
	url="http://www.twitter.com"
else:
	url="http://www.linkedin.com"

webbrowser.open(url,new=new)