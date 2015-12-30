#!/usr/bin/env bash


echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "\033[32m                  脚本支持                    \033[0m"
echo "\033[32m              1.查看远程服务状态               \033[0m"
echo "\033[32m              2.停止远程服务                   \033[0m"
echo "\033[32m              3.启动远程服务                   \033[0m"
echo "\033[32m              4.部署远程服务                   \033[0m"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~       执行方式        ~~~~~~~~~~~~~~~~~~~~~"
echo "\033[32m carrefour_mobile.sh (app|weixin)_status     \033[0m"
echo "\033[32m carrefour_mobile.sh app                     \033[0m"
echo "\033[32m carrefour_mobile.sh weixin                  \033[0m"
echo "\033[32m carrefour_mobile.sh (app|weixin)_start      \033[0m"
echo "\033[32m carrefour_mobile.sh (app|weixin)_stop       \033[0m"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

source_files="/software/mobile_war/cybershop-mobile-0.0.1-SNAPSHOT.war"
dest_files="/software/cybershop-mobile-0.0.1-SNAPSHOT.war"
app_addr_list="10.151.254.3 10.151.254.11"
weixin_addr_list="10.151.254.14 10.151.254.15"

send_app_files () {
    for ip in ${app_addr_list}
            do
                scp ${source_files} ${ip}:${dest_files}
                if [ $? -eq 0 ]; then
                    echo "Send War TO APP:$ip successful"
                fi
            done
}
send_weixin_files () {
    for ip in ${weixin_addr_list}
            do
                scp ${source_files} ${ip}:${dest_files}
                if [ $? -eq 0 ]; then
                    echo "Send War TO weixin:$ip successful"
                fi
            done
}
deploy_app () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_app.py -c mobile -d deploy"
            if [ $? -eq 0 ]; then
                echo "deploy  APP:$ip successful"
            fi
        done
}
deploy_weixin () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_wechat.py -c mobile -d deploy"
            if [ $? -eq 0 ]; then
                echo "deploy  APP:$ip successful"
            fi
        done
}
app_status () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_app.py -c mobile -d status"
            if [ $? -eq 0 ]; then
                echo "Get   APP:$ip Status successful"
            fi
        done

}
weixin_status () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_wechat.py -c mobile -d status"
            if [ $? -eq 0 ]; then
                echo "GET   weixin:$ip Status successful"
            fi
        done

}
app_start () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_app.py -c mobile -d start"
            if [ $? -eq 0 ]; then
                echo "Get  APP:$ip successful"
            fi
        done

}
weixin_start () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_wechat.py -c mobile -d start"
            if [ $? -eq 0 ]; then
                echo "Get  weixin:$ip successful"
            fi
        done

}
app_stop () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_app.py -c mobile -d stop"
            if [ $? -eq 0 ]; then
                echo "deploy  APP:$ip successful"
            fi
        done

}
weixin_stop () {
    for ip in ${app_addr_list}
        do
            ssh ${ip} "/software/script/carrefour_wechat.py -c mobile -d stop"
            if [ $? -eq 0 ]; then
                echo "deploy  weixin:$ip successful"
            fi
        done

}
main(){
    case $1 in
        app)
            send_app_files;
            deploy_app;
            ;;
        weixin)
            send_weixin_files;
            deploy_weixin;
            ;;
        app_status)
            app_status;
            ;;
        app_start)
            app_start;
            ;;
        app_stop)
            app_stop;
            ;;
        weixin_status)
            weixin_status;
            ;;
        weixin_start)
            weixin_start;
            ;;
        weixin_stop)
            weixin_stop;
            ;;
        *)
            echo "Usage:$0(app|weixin|app_status|app_start|app_stop|weixin_status|weixin_start|weixin_stop)"
            exit 1
            ;;
    esac
}
main $1