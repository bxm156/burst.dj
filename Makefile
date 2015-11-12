.PHONY: clean templates watch all

all: templates
	pserve development.ini --reload

templates:
	bundle exec compass compile

watch:
	bundle exec compass watch

clean:
	echo "bite me"

