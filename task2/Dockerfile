# Базовый образ — лёгкий nginx на Alpine (~40 MB вместо сотен у debian)
FROM nginx:alpine

# Метаданные образа (docker image inspect → Config.Labels)
LABEL maintainer="Бельский Тимофей Дмитриевич <pipa53@example.com>"
LABEL description="Lab 1, Task 2 — nginx с собственной HTML-страницей"

# Копируем нашу страницу внутрь образа, в корень сайта nginx
# (в отличие от задания 1: файл «запекается» в слой, bind mount не нужен)
COPY html/index.html /usr/share/nginx/html/index.html

# Документируем, что контейнер слушает 80 порт (сам по себе EXPOSE порты не публикует)
EXPOSE 80

# CMD наследуется из базового образа nginx:alpine — там уже прописан запуск nginx
# Явно указывать не обязательно, но для наглядности оставим комментарий
# CMD ["nginx", "-g", "daemon off;"]