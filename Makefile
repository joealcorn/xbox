.PHONY: requests six

requests:
	rm -fr xbox/vendor/requests
	git clone https://github.com/kennethreitz/requests.git
	mv requests/requests xbox/vendor
	rm -fr requests

six:
	rm -rf xbox/vendor/six
	hg clone ssh://hg@bitbucket.org/gutworth/six
	mv six/six.py xbox/vendor
	rm -fr six
