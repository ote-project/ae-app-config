FROM eclipse-temurin:21
RUN apt update \
  && apt install -y build-essential git curl gsfonts imagemagick libmagickwand-dev nodejs redis-server libssl-dev libcurl4-openssl-dev libxml2-dev libxslt1-dev default-libmysqlclient-dev mysql-server sudo

COPY ./jruby/bin /opt/jruby/bin
COPY ./jruby/lib/jni /opt/jruby/lib/jni
COPY ./jruby/lib/ruby /opt/jruby/lib/ruby
COPY ./jruby/lib/jruby.jar /opt/jruby/lib/

RUN update-alternatives --install /usr/local/bin/ruby ruby /opt/jruby/bin/jruby 1
COPY ./diaspora /opt/diaspora
ENV PATH /opt/jruby/bin:$PATH
RUN /opt/diaspora/bin/set_up_dse_db

WORKDIR /opt/diaspora
ENTRYPOINT ["bin/run_dse_in_docker"]

