FROM nginx
# COPY sermons.html /usr/share/nginx/html/sermons.html
COPY index.html /usr/share/nginx/html/index.html
COPY default.conf /etc/nginx/conf.d/default.conf
RUN mkdir /usr/share/nginx/html/images
RUN chmod a+w /usr/share/nginx/html/images
COPY ./images/cropped-IMG_1811.jpg /usr/share/nginx/html/images/cropped-IMG_1811.jpg

