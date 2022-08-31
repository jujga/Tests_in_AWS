ENV preparing:
1. Deploy Jenkins:
   - run `docker volume create common-volume` in the command line
   - run `docker volume create jenkins_settings_home`
   - unzip `pipeline/FULL-2022-08-31_11-39.ZIP` locally to the `<your_back_up_dir>`
   - run `docker run -d --name jenkins9 -p 8089:8080 -p 50089:50000 -u root -v /opt/maven/apache-maven-3.2.5:/usr/local/maven -v /var/run/docker.sock:/var/run/docker.sock  -v /usr/bin/docker:/usr/bin/docker --mount type=bind,source=D:\\jenkins_backup,target=/home -v common-volume:/var/jenkins_home/workspace/with_docker_compose  -v jenkins_settings_home:/var/jenkins_home jenkins/jenkins:lts`
     where `<your_back_up_dir>` is locally dir `jenk_settings_back_up.zip` unzipped is
   - run Jenkins http://localhost:8089/
   - run `docker exec -it jenkins9 bash`
   - view and copy password using command `cat var/jenkins_home/secrets/initialAdminPassword`
   - paste get password into Jenkins and submit
   - refuse of installing plugins
   - install plugin `thinbackup`
   - tune plugin `thinbackup` for `<your_back_up_dir>` (specify mounted `/home`)
   - using plugin `thinbackup` restore  Jenkins's settings from back up
   - restart Jenkins
   - after backing up username=`admin`, password=`123`
   
2. Running tests:
   - run `with_docker_compose` build

For information regarding autotests, see the readme in the /tests/README.md
