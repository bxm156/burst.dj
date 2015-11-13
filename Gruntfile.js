
module.exports = function (grunt) {
  'use strict';

  // Project configuration.
  grunt.initConfig({
      pkg: grunt.file.readJSON('package.json'),
      meta: {
          version: '0.0.1',
          banner: '/*!\n* <%= pkg.name %> - v<%= meta.version %>\n' +
              '* http://pylonsproject.org/\n' +
              '* Copyright (c) <%= grunt.template.today("yyyy") %> ' +
              'Pylons Project\n*/\n\n'
      },
      bower: {
          'default': {
              dest: 'burstdj/static',
              options: {
                  expand: true,
                  packageSpecific: {
                      'foundation': {
                          files: [
                            "js/foundation/foundation.reveal.js"
                          ]
                      }
                  }
              }
          }
      },
      copy: {
          'js': {
              files: [
                {expand: true, src: ['js/**'], dest: 'burstdj/static'},
            ],
          }
      },
      sass: {
          'default': {
              options: {
                  style: 'expanded',
                  loadPath: ['bower_components/foundation/scss']
              },
              files: [{
                  expand: true,
                  cwd: 'scss',
                  src: ['*.scss'],
                  dest: 'burstdj/static/css',
                  ext: '.css'
              }]
          }
      }
  });

  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-bower');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task.
  grunt.registerTask('default', [
    'sass:default',
    'bower:default',
    'copy:js',
  ]);
};
