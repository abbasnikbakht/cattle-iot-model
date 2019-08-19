#!/usr/bin/env bash


processes=( "python monitor.py" "python file_processor.py" "python datalogger.py")

start() {
    source /home/pi/datalogger/catenv/bin/activate
    echo virtualenv is now active.
    echo running the scripts
    for i in "${processes[@]}"
        do
           if pgrep -f "$i" &>/dev/null; then
                echo "$i already running. please stop it first"
           else
                $i &
        fi
        done

}

start_data_logger(){
    if pgrep -f "python datalogger.py" &>/dev/null; then
        echo "datalogger already running. please stop it first"
   else
        python datalogger.py &
    fi
}

stop() {

    for i in "${processes[@]}"
        do
           if pgrep -f "$i" &>/dev/null; then
                echo "Stopping "$i""
                kill $(pgrep -f "$i")
           else
                echo "$i not running"


        fi
        done

}

case "$1" in
    'start')
            start
            ;;

    'start_datalogger')
            start_data_logger
            ;;

    'stop')
            stop
            ;;
    'restart')
            stop ; echo "Sleeping..."; sleep 1 ;
            start
            ;;
    *)
            echo
            echo "Usage: $0 { start | start_datalogger | stop | restart  }"
            echo
            exit 1
            ;;
esac

exit 0
