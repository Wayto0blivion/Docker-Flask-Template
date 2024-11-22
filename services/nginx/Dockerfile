FROM nginx:latest
LABEL authors="Zuicie"

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]