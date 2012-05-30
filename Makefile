# restapp Makefile
#
.PHONY: build pkg sdist egg install uninstall deploy-apache test env check clean doc ftest bench

# use TAG=a for alpha, b for beta, rc for release candidate
ifdef TAG
	PKGTAG := egg_info --tag-build=$(TAG) --tag-date
else
    PKGTAG :=
endif

build:
	python setup.py $(PKGTAG) build

pkg: sdist egg

sdist:
	python setup.py $(PKGTAG) sdist

egg:
	-python2.6 setup.py $(PKGTAG) bdist_egg
	-python2.7 setup.py $(PKGTAG) bdist_egg

install:
	python setup.py $(PKGTAG) install

uninstall:
	-rm -rf /usr/local/lib/python2.6/dist-packages/restapp-*
	-rm -f /usr/local/bin/restapp

deploy-apache:
	fab pack deploy

test:
	nosetests -v

ftest:
	$(MAKE) -C ftests

bench:
	$(MAKE) -C ftests bench

env:
	pip install -s -E env -r deps.txt
	@echo "Remember to run:\n source env/bin/activate"

check:
	pyflakes restapp

doc:
	$(MAKE) -C doc html

clean:
	find . "(" -name "*~" -or  -name ".#*" -or  -name "#*#" -or -name "*.pyc" ")" -print0 | xargs -0 rm -f
	rm -rf ./build ./dist ./MANIFEST ./restapp.egg-info
