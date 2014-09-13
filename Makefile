.PHONY: requests publish html

requests:
	rm -fr xbox/vendor/requests
	git clone https://github.com/kennethreitz/requests.git
	mv requests/requests xbox/vendor
	rm -fr requests
