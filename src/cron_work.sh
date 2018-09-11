#!/bin/sh
export LANG="zh_CN.UTF-8"

exec_dir=/root/RssToKindle/RssToKindle/src
#output_dir=$exec_dir/temp
#output_file=$output_dir/daily.mobi
output_dir=$exec_dir/temp_html
output_file=$output_dir/daily.html
target_dir=/var/www/news/

cd $exec_dir
python RSSToKindle.py

if [ -e $output_file ] 
then
    date_str=`date +%Y%m%d`
    mv $output_file $target_dir/daily_$date_str.html
fi
