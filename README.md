ENV preparing:
1. Deploy Jenkins:
   - run `docker volume create common-volume` in the command line
   - unzip `jenk_settings_back_up.zip` locally
   - run `docker run -d --name jenkins8 -p 8088:8080 -p 50088:50000 -u root  -v /home/acmedcare/jenkins_home:/var/jenkins_home -v /opt/maven/apache-maven-3.2.5:/usr/local/maven -v /var/run/docker.sock:/var/run/docker.sock  -v /usr/bin/docker:/usr/bin/docker --mount type=bind,source=<your_back_up_dir>>,target=/home -v common-volume:/var/jenkins_home/workspace/with_docker_compose  jenkins/jenkins:lts`
     where `<your_back_up_dir>` is locally dir `jenk_settings_back_up.zip` unzipped is
   - run Jenkins http://localhost:8088/
   - run `docker exec -it jenkins8 bash`
   - view and copy password using command `cat var/jenkins_home/secrets/initialAdminPassword`
   - paste get password into Jenkins and submit
   - refuse of installing plugins
   - install plugin `thinbackup`
   - tune plugin `thinbackup` for `<your_back_up_dir>`
   - using plugin `thinbackup` restore  Jenkins's settings from back up
   
2. Running tests:
   - run `with_docker_compose` build

For information regarding autotests, see the readme in the /tests/README.md
