# SGD Visualization

[![Build Status](https://travis-ci.org/yeastgenome/sgd_visualization.svg)](https://travis-ci.org/yeastgenome/sgd_visualization)

This is a set of react components used for genomic data visualization by [SGD](http://yeastgenome.org).  The word "set" isn't technically correct, because currently there is only one component, the protein viewer.  In the future, more components will be added.

## See Examples

Clone the repo, make sure [grunt](http://gruntjs.com) is installed.

Install dependencies

	$ npm install

Run example server

    $ grunt

Go to http://localhost:3000/protein_viewer

Look at examples/protein_viewer/index.html to see how the protein viewer is configured.

## Run Tests

Install [mocha](http://mochajs.org/) and then run

    $ mocha
