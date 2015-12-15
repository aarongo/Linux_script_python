#!/usr/bin/env bash

TOMCAT_HOME=/software/jenkins_tomcat
#Wait For StopIng Tomcat
SHUTDOWN_WAIT=20

tomcat_pid() {
    echo `ps aux | grep org.apache.catalina.startup.Bootstrap | grep -v grep | grep 'jenkins_tomcat' | awk '{ print $2 }'`
}

start() {
  pid=$(tomcat_pid)
    if [ -n "$pid" ];then
      echo "\033[32mTomcat is already running (pid: $pid)\033[0m"
    else
      # Start tomcat
      echo "\033[32mStarting tomcat\033[0m"
      ulimit -n 100000
      umask 007
      /bin/su -p -s /bin/sh root $TOMCAT_HOME/bin/startup.sh
    fi
  return 0
}

stop() {
  pid=$(tomcat_pid)
  if [ -n "$pid" ];then
    echo "\033[32m Stoping Tomcat\033[0m"
    /bin/su -p -s /bin/sh root $TOMCAT_HOME/bin/shutdown.sh
    let kwait=$SHUTDOWN_WAIT
    count=0;
    until [ `ps -p $pid | grep -c $pid` = '0' ] || [ $count -gt $kwait ]
    do
      echo -n -e "\nwaiting for processes to exit";
      sleep 1
      let count=$count+1;
    done

    if [ $count -gt $kwait ]; then
      echo -n -e "\nkilling processes which didn't stop after $SHUTDOWN_WAIT seconds"
      kill -9 $pid
    fi
  else
    echo "Tomcat is not running"
  fi

  return 0
}

case $1 in
      start)
        start
      ;;
      stop)
        stop
      ;;
      restart)
        stop
        start
      ;;
      status)
        pid=$(tomcat_pid)
        if [ -n "$pid" ]
        then
          echo "Tomcat is running with pid: $pid"
        else
          echo "Tomcat is not running"
        fi
      ;;
esac
exit 0