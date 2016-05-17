test:
	sh run_template_min.sh

package:
	python3 setup.py bdist_wheel
	ls dist/*

build:
	python3 setup.py bdist

package_to_pypi:
	python3 setup.py sdist upload
	@echo "Go to https://pypi.python.org/pypi/bio-apricot/"

html_doc:
	cd docs && make html && cd ..

show_html_docs:
	firefox docs/build/html/index.html &

readme_txt:
	pandoc --from=markdown --to=plain README.md -o README.txt

readme_html:
	pandoc --from=markdown --to=html README.md -o README.html

readme_rst:
	grep -v "^\[!" README.md | sed -e "1d" > README.md.tmp
	pandoc --from=markdown --to=rst README.md.tmp -o README.rst
	rm README.md.tmp

readme_clean:
	rm -f README.tex README.html README.rst
	rm -f README.tex README.html README.txt

pylint:
	pylint bin/apricot apricotlib/* tests/*

new_release:
	@echo "* Create/checkout a release branch"
	@echo "  git branch release_v0.3.X"
	@echo "  git checkout release_v0.3.X"
	@echo "* Change bin/apricot"
	@echo "* Change setup.py"
	@echo "* Change docs/source/conf.py"
	@echo "* Change CHANGELOG.txt"
	@echo "* Create new docs"
	@echo "* Test package creation"
	@echo "* Test doc creation"
	@echo "* make package_to_pypi"
	@echo "* git add CHANGELOG.txt bin/apricot docs/source/conf.py setup.py"
	@echo "* Commit changes e.g. 'git commit -m \"Set version to 1.0.X\"'"
	@echo "* Tag the commit e.g. 'git tag -a v1.0.X -m \"version v1.0.X\"'"
	@echo "* Merge release into dev and master"
	@echo "* Push it to github: git push"
	@echo "* Generate a new release based on this tag at"
	@echo "  https://github.com/malvikasharan/APRICOT/releases/new"
	@echo "* Upload new docs using 'make upload_doc'"
