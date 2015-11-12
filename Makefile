.PHONY: clean bower templates watch all

all: templates
	pserve development.ini --reload

bower:
	bower update

templates: bower
	bundle exec compass compile

watch: bower
	bundle exec compass watch

clean:
	echo "bite me"

