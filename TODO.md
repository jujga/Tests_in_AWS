1. Do 2 reports - cumulative and in the context in each build. Append auto build cleaning (store only N builds). да. получается у тебя должно быть в каждой сборке по сути тот же накопительный, но какопление заканчивается этой конкретной сборкой. и в каждой следующей сборке берется предыдущий отчет и к нему добавляются данные от текущей сборки.....или еще есть отдельный докер контейнер для менеджмента тест-репортов от аллюра - это более правильно , но намного реже используется, т к геморно настраивать )
2. Move Jenkins to a container - Done
    docker volume create jenkins
    docker run --name jenkins -ti     -v jenkins:/var/jenkins_home  --mount type=bind,source=D:\jenkins_backup,target=/app -p 127.0.0.1:8083:8080     jenkins/jenkins:lts
3. Move Jenkins and test env to a cloud
4. Auto running build after merge into master
5. Instruction for Auto deploy all project - Done manual instruction

