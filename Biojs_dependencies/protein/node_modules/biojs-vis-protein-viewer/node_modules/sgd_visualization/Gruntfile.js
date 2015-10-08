"use strict";
var EXAMPLE_PATH = "examples/";
var SRC_PATH = "src/sgd_visualization.jsx";

module.exports = function(grunt) {    
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),

        browserify: {
            dev: {
                dest: EXAMPLE_PATH + "assets/bundled_sgd_visualization.js",
                src: "src/bundled.jsx",
                options: {
                    browserifyOptions: {
                        debug: true
                    }
                }
            }
        },

        connect: {
            server: {
                options: {
                    port: 3000,
                    base: EXAMPLE_PATH
                }
            }
        },

        watch: {
            options: {
                livereload: true
            },
            jsx: {
                files: ["src/**/*.jsx", "src/**/*.js", (EXAMPLE_PATH + "**/*.html")],
                tasks: ["browserify:dev"]
            }
        },
    });

    // load vendor tasks
    grunt.loadNpmTasks("grunt-browserify");
    grunt.loadNpmTasks("grunt-contrib-connect");
    grunt.loadNpmTasks("grunt-contrib-watch");
    
    // define custom tasks
    grunt.registerTask("default", ["browserify:dev", "connect","watch"]);
};
