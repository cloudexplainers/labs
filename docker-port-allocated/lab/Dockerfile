# Ana's tea shop website: nginx serving one page. Built off-screen as shop:v1 and shop:v2 (VERSION).
FROM nginx:alpine
ARG VERSION
RUN printf '<h1>Ana'"'"'s tea shop</h1>\n<p>Version %s</p>\n' "$VERSION" > /usr/share/nginx/html/index.html
