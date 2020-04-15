const gulp = require('gulp');
const connect = require('gulp-connect');
const htmlmin = require('gulp-htmlmin');
const ngAnnotate = require('gulp-ng-annotate');
const replace = require('gulp-replace');
const uglify = require('gulp-uglify-es').default;
const useref = require('gulp-useref');

gulp.task('dev', () =>
  connect.server({
    host: '0.0.0.0',
    port: 8080,
    root: ['.', 'src']
  })
);

gulp.task('useref', () =>
  gulp.src('src/index.html')
    .pipe(useref())
    .pipe(gulp.dest('dist'))
);

gulp.task('js', () =>
  gulp.src('dist/main.min.js')
    .pipe(ngAnnotate())
    .pipe(uglify())
    .pipe(replace('http://localhost:8081', `${process.env.API_HOST}`))
    .pipe(gulp.dest('dist'))
);

gulp.task('html', () =>
  gulp.src('src/app/**/*.html')
    .pipe(htmlmin({ collapseWhitespace: true }))
    .pipe(gulp.dest('dist/app'))
);

gulp.task('fonts', () =>
  gulp.src('node_modules/font-awesome/fonts/*')
    .pipe(gulp.dest('dist/fonts'))
);

gulp.task('assets', () =>
  gulp.src(['src/favicon.ico'])
    .pipe(gulp.dest('dist'))
);

gulp.task('build', gulp.series('useref', 'js', 'html', 'fonts', 'assets'));

gulp.task('default', gulp.series('dev'));
