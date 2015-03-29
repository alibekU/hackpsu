//*********** IMPORTS *****************
var lr = require('tiny-lr'), // Минивебсервер для livereload
    gulp = require('gulp'), // Сообственно Gulp JS
    jade = require('gulp-jade'), // Плагин для Jade
    stylus = require('gulp-stylus'), // Плагин для Stylus
    nib = require('nib'); //Плагин для nib
    livereload = require('gulp-livereload'), // Livereload для Gulp
    jsmin = require('gulp-jsmin'); // Минификация JS
    rename = require('gulp-rename'); //Переименовка
    myth = require('gulp-myth'), // Плагин для Myth - http://www.myth.io/
    csso = require('gulp-csso'), // Минификация CSS
    imagemin = require('gulp-imagemin'), // Минификация изображений
    uglify = require('gulp-uglify'), // Минификация JS
    concat = require('gulp-concat'), // Склейка файлов
    connect = require('connect'), // Webserver
    server = lr();

// Собираем Stylus
gulp.task('stylus', function() {
    gulp.src('./assets/stylus/*.styl')
        .pipe(stylus({use: [nib()]})) // собираем stylus
    .on('error', console.log) // Если есть ошибки, выводим и продолжаем
    .pipe(myth()) // добавляем префиксы - http://www.myth.io/
    .pipe(gulp.dest('./public/css/')) // записываем css
    .pipe(livereload(server)); // даем команду на перезагрузку css
});

// Собираем html из Jade
gulp.task('jade', function() {
    gulp.src(['./assets/template/*.jade','!./assets/template/_*.jade'])
        .pipe(jade({
            pretty: true
        }))  // Собираем Jade только в папке ./assets/template/ исключая файлы с _*
        .on('error', console.log) // Если есть ошибки, выводим и продолжаем
    .pipe(gulp.dest('./public/')) // Записываем собранные файлы
    .pipe(livereload(server)); // даем команду на перезагрузку страницы
});

//Собираем JS
gulp.task('js', function() {
    gulp.src('./assets/js/**/*.js')
    .pipe(gulp.dest('./public/js'))
    .pipe(livereload(server)); // даем команду на перезагрузку страницы
});

// Копируем и минимизируем изображения
gulp.task('images', function() {
    gulp.src('./assets/img/**/*')
        .pipe(imagemin())
        .pipe(gulp.dest('./public/img'))
});

// Локальный сервер для разработки
gulp.task('http-server', function() {
    connect()
        .use(require('connect-livereload')())
        .use(connect.static('./public'))
        .listen('9000');
    console.log('Server listening on http://localhost:9000');
});

// Запуск сервера разработки gulp watch
gulp.task('watch', function() {
    // Предварительная сборка проекта
    gulp.run('stylus');
    gulp.run('jade');
    gulp.run('images');
    gulp.run('js');

    // Подключаем Livereload
    server.listen(35729, function(err) {
        if (err) return console.log(err);
        gulp.watch('assets/stylus/**/*.styl', ['stylus']);
        gulp.watch('assets/template/**/*.jade',['jade']);
        gulp.watch('assets/img/**/*', ['images']);
        gulp.watch('assets/js/**/*', ['js']);
    });
    gulp.run('http-server');
});