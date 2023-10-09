# QA.GURU: Дипломный проект

Реализация набора автотестов (UI, API) для сайта <a href="https://themoviedb.com">themoviedb.com</a>.

> The Movie Database (TMDB) - популярная база данных фильмов и телепередач. Все данные в ней добавляются участниками сообщества, начиная с 2008 года. Более 400 тыс. разработчиков и компаний используют ее для создания сайтов и приложений. Ежедневно она обрабатывает более 3 млрд запросов.

### Используемые технологии
<p  align="center">
  <code><img width="5%" title="Pycharm" src="images/logo/pycharm.png"></code>
  <code><img width="5%" title="Python" src="images/logo/python.png"></code>
  <code><img width="5%" title="Pytest" src="images/logo/pytest.png"></code>
  <code><img width="5%" title="Selene" src="images/logo/selene.png"></code>
  <code><img width="5%" title="Selenium" src="images/logo/selenium.png"></code>
  <code><img width="5%" title="GitHub" src="images/logo/github.png"></code>
  <code><img width="5%" title="Jenkins" src="images/logo/jenkins.png"></code>
  <code><img width="5%" title="Selenoid" src="images/logo/selenoid.png"></code>
  <code><img width="5%" title="Allure Report" src="images/logo/allure_report.png"></code>
  <code><img width="5%" title="Telegram" src="images/logo/tg.png"></code>
</p>

Весь проект выполнен на языке Python, а также дополнительно:

- для UI-тестов применялись: Selene
- для API-тестов применялись: Requests, JSONSchema

Запуск тестов осуществляется с помощью:

- Jenkins
- Selenoid

Отчёты и уведомления о результатах формируются с помощью:

- Allure
- allure-notifications



# Покрытая тестами функциональность

<a href="https://github.com/ilyatara/themoviedb-tests/tree/master/tests/ui">UI</a>
- авторизация пользователя
- поиск фильмов и людей
- добавление фильма в **Понравившиеся**

<a href="https://github.com/ilyatara/themoviedb-tests/tree/master/tests/api">API</a>

- получение и изменение списка оцененных пользователем фильмов
- получение списка фильмов с наибольшим рейтингом

# <a href="https://jenkins.autotests.cloud/job/ilyatara-diploma_ui_api/">Сборка Jenkins для запуска тестов</a>

<img src="readme_images/jenkins_main_page.jpg" alt=""/>



# Запуск тестов

## Удалённый запуск

Запуск тестов на удалённой машине запускается с помощьюосуществляется с помощью скрипта:

UI-тесты:
```
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
context=selenoid browser=${BROWSER} browser_version=${BROWSER_VERSION} browser_size=${BROWSER_SIZE} selene_timeout=${SELENE_TIMEOUT} pytest tests/ui
```

API-тесты:
```
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
context=selenoid api_timeout=${API_TIMEOUT} pytest tests/api
```

Все параметры запуска, кроме "context", являются необязательными. (Если они не переданы, используются значения по умолчанию из файла project.py.)

В Jenkins параметры запуска передаются на странице "Собрать с параметрами":

<img src="readme_images/jenkins_parametrized_build.jpg" alt=""/>


## Локальный запуск

Локальный запуск всех тестов с дефолтными значениями конфигурационных переменных:
```
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
pytest .
```

При локальном запуске задавать переменную "context" необязательно, т.к. её значение "local" является дефолтным. Если переменная "context" имеет другое значение, её необходимо переопределить: <code>context=local pytest .</code>.

Подробнее о синтаксе выбора директории/файлов/тестов для запуска см. <a href="https://docs.pytest.org/en/7.1.x/how-to/usage.html">документацию PyTest</a>.



## Отчёты о прохождении тестов в Allure

#### Если тест запускался локально:
Введите в терминале команду 
```
allure serve
``` 
#### Если тест запускался в Jenkins
Передите по ссылке "Allure Report" на странице сборки:
<img src="readme_images/jenkins_build_page.jpg" alt=""/>


### Пример отображения тестов

При запуске UI-тестов в разделе "Tear down - setup browser" прикрепляется скриншот и исходный код страницы, а также логи браузера.

Если тест запускался через Selenoid, также будет прикреплено видео его прохождения/

<img src="readme_images/allure_attachments.jpg" alt=""/>

https://github.com/ilyatara/themoviedb-tests/assets/135700131/446e5ee3-b705-4d03-888a-fba6d6b4d7b4





# Подготовка к запуску

## Добавление конфигурационных файлов в Jenkins

Для запуска тестов необходимо создать в корневой директории проекта файл .env с настройками, которые с помощью библиотеки python-dotenv будут сохранены в переменные окружения. Пример заполнения файла можно посмотреть в файле .env.example.

Для запуска тестов нужно зарегистрироваться на сайте https://www.themoviedb.org/ и указать логин и пароль в переменных TMDB_LOGIN и TMDB_PASSWORD.
Также для получения авторизационного токена доступа к API необходимо создать приложение на странице https://www.themoviedb.org/settings/api. После создания приложения на ней в разделе API Read Access Token начнёт отображаться токен. Его нужно сохранить как значение настройки TMDB_READ_ACCESS_TOKEN.
Параметр TMDB_ACCOUNT_ID заполнять не обязательно. Если он останется пустым, id аккаунта будет получено через API и сохранено в конфигурационном классе Config проекта в файле project.py.

Для удалённого запуска UI-тестов в Selenoid в настройках с соответствующим префиксом нужно сохранить логин, пароль от сервиса и его базовый url.

Для добавления .env файла в Jenkins необходимо выбрать "Добавить файл сборки" - "Create/Update Text File" с параметрами "Create at Workspace" и "Overwrite file" и поместить его выше скрипта запуска тестов:

<img src="readme_images/jenkins_config_env_file.jpg" alt=""/>

Для получения отчётов о прохождении тестов в Telegram нужно аналогичным образом добавить файл notifications/telegram.json. Образец его заполнения можно находится в файле notifications/telegram.json.example. В нём необходимо заполнить поля "token" и "chat". Подробнее о заполнении этого файла см. <a href="https://github.com/qa-guru/allure-notifications">документацию проекта allure-notifications</a>.

## Формирование Allure-отчёта и получение уведомления в Telegram

Для выполнения этих шагов в разделе "Послесборочные операции" "Allure Report" и "Post build task":

<img src="readme_images/jenkins_config_post_build_actions.jpg" alt=""/>

Скрипт для отправки уведомлений в Telegram:

```
java "-DconfigFile=notifications/telegram.json" -jar notifications/allure-notifications-4.5.0.jar
```



# Уведомление о завершении тестового прогона в Telegram

Для получения результатов о тестировании используется телеграм-бот, при этом в отчёте отображаются параметры запуска тестового комплекта, время прохождения тестов, а также ссылка на allure-отчёт.

### Пример отчёта о выполнении UI и API тестов:

<img src="readme_images/telegram_notification.jpg" alt=""/>
