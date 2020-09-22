import webbrowser

def Open(x):
	new=2
	url=x
	webbrowser.open(url,new=new)

x=str(input("Enter the link: "))

Open(x)