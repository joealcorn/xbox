.PHONY: requests six release

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

release:
	python setup.py register
	python setup.py sdist bdist_wheel
	twine upload dist/*
