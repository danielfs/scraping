build:
	@docker build --quiet -t crawly .
run:
	@docker run crawly
debug:
	@docker run -e DEBUG=true crawly
test:
	@docker run crawly python test.py

