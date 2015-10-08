// packages
var gulp   = require('gulp');
var mocha = require('gulp-mocha'); 
var fs = require('fs');
var path = require('path');
var join = path.join;

// a failing test breaks the whole build chain
gulp.task('default', ['test']);

gulp.task('test', ['test-unit']);
gulp.task('test-unit', function () {
    return gulp.src('./test/**/test*.js', {read: false})
        .pipe(mocha({reporter: 'spec', ui: "qunit",
                    useColors: true}));
});


gulp.task('watch', ['test','watch-mocha']);

gulp.task('watch-mocha', function() {
   gulp.watch(['./src/**/*.js','./lib/**/*.js', './test/**/*.js'], ['test']);
});
