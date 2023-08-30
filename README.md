import '@github/clipboard-copy-element'
<script type="module" src="./node_modules/@github/clipboard-copy-element/dist/index.js">
### Системные требования

Для работы скрипта необходимо установить следующие компоненты:
1.  Python версии 3.11  и старше.
2.  Библиотеки, указанные во вложеном файле requirements.txt. Можно установить с помощью команды: <clipboard-copy for="blob-path" class="btn btn-sm BtnGroup-item">Copy path</clipboard-copy><div id="blob-path">src/index.js</div>`pip install -r requirements.txt` из папки проекта.
3.  Config файл должен нахдится в той же директории что и main.py.

### Запуск и результат
Для запуска необходимо выполнить скрипт main.py.

После завершения отработки будет создана папка `downloads`, в которой будет сохранен выгруженый файл. Также будет создан файл log.log, содержащий в себе логи исполнения скрипта.

Скриншот с результатом появится в корневой директории под именем: `result.png`

