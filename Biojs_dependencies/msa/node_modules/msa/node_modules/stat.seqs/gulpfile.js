/*
 * stat.seqs
 * https://github.com/greenify/stat.seqs
 *
 * Copyright (c) 2014 greenify
 * Licensed under the MIT license.
 */


// browserify build config
var buildDir = "build";
var outputFile = "biojsstatseqs";

// packages
var gulp   = require('gulp');

// testing
var mocha = require('gulp-mocha'); 

// path tools
var fs = require('fs');
var path = require('path');
var join = path.join;
var mkdirp = require('mkdirp');
var del = require('del');

// auto config
var outputFileMin = join(buildDir,outputFile + ".min.js");
var packageConfig = require('./package.json');

// a failing test breaks the whole build chain
gulp.task('default', ['test']);


gulp.task('test', ['test-unit']);


gulp.task('test-unit', function () {

    return gulp.src('./test/**/test*.js', {read: false})
        .pipe(mocha({reporter: 'spec',
                    useColors: true}));
});


gulp.task('watch', ['test','watch-mocha']);
gulp.task('watch-mocha', function() {
   gulp.watch(['./src/**/*.js','./lib/**/*.js', './test/**/*.js'], ['test']);
});

// will remove everything in build
gulp.task('clean', function(cb) {
  del([buildDir], cb);
});

// just makes sure that the build dir exists
gulp.task('init', ['clean'], function() {
  mkdirp(buildDir, function (err) {
    if (err) console.error(err)
  });
});
