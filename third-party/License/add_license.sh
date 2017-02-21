#!/bin/bash
# Copyright justin.chigang@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

TMP_FILE=tmp.file
LICENSE_TOKEN="http://www.apache.org/licenses/LICENSE-2.0"

function get_first_author()
{
    author=$(git log --reverse --pretty=format:"%ae" $1 | head -1)
    substring=$(git log --reverse --pretty=format:"%ae" $1 | head -1 | awk -F@ '{print $2}')
    case $substring in
     huawei*)
       echo "HUAWEI TECHNOLOGIES CO.,LTD"
          ;;
     orange*)
       echo "Orange"
          ;;
     zte*)
       echo "ZTE Corporation"
          ;;
     *)
       echo "$author"
          ;;
     esac
}

function get_latest_year()
{
    git log --pretty=format:"%ad" $1 | head -1 | awk '{print $5}'
}

function gen_c_license()
{
cat << EOF >$1
/******************************************************************************* 
 * Copyright (c) $2 $3 and others. 
 *
 * All rights reserved. This program and the accompanying materials 
 * are made available under the terms of the Apache License, Version 2.0 
 * which accompanies this distribution, and is available at 
 * http://www.apache.org/licenses/LICENSE-2.0 
 *******************************************************************************/ 

EOF
}

function gen_xml_license()
{
cat << EOF >$1
<!--
 Copyright (c) $2 $3 and others.

 All rights reserved. This program and the accompanying materials
 are made available under the terms of the Apache License, Version 2.0
 which accompanies this distribution, and is available at
 http://www.apache.org/licenses/LICENSE-2.0
-->

EOF
}

function gen_bash_license()
{
cat << EOF >$1
##############################################################################
# Copyright (c) $2 $3 and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

EOF
}

function add_c_license()
{
    C_LICENSE="c_license_header.tmp"
    author=`get_first_author "$1"`
    year=`get_latest_year "$1"`
    gen_c_license $C_LICENSE $year "$author"
    cat $C_LICENSE $1 > $TMP_FILE
    rm -f $C_LICENSE
    mv $TMP_FILE $1
}

function add_xml_license()
{
    XML_LICENSE="xml_license_header.tmp"
    author=`get_first_author "$1"`
    year=`get_latest_year "$1"`
    gen_xml_license $XML_LICENSE $year "$author"
    cat $XML_LICENSE $1 > $TMP_FILE
    rm -f $XML_LICENSE
    mv $TMP_FILE $1
}

function add_bash_license()
{
    BASH_LICENSE="bash_license_header.tmp"
    author=`get_first_author "$1"`
    year=`get_latest_year "$1"`
    gen_bash_license $BASH_LICENSE $year "$author"
    cat $1 | head -1 | grep "#!" > /dev/null
    if [ $? -eq 0 ]; then
        #insert 2
        sed -i "1 r $BASH_LICENSE" $1
    else
        #sed -i "1 R $BASH_LICENSE" $1
        cat $BASH_LICENSE $1 > $TMP_FILE
        mv $TMP_FILE $1
    fi
    rm -f $BASH_LICENSE
}

if [[ -z "$1" ]] || [[ ! -d "$1" ]]; then  
    echo "The directory is empty or not exist!"  
    echo "It will use the current directory."  
    nowdir=$(pwd)  
else  
    nowdir=$(cd $1; pwd)  
fi  
echo "$nowdir"  

n=0

function Searchfile()  
{  
    cd $1  
    
    dirlist=$(ls)  
    for dirname in $dirlist
    do  
        if [[ -d "$dirname" ]];then
            n=$((n+4))
            cd $dirname
            for i in $( seq 0 $n );do echo -n ' ';done;echo "$dirname ..."  
            Searchfile $(pwd)  
            cd ..  
            n=$((n-4))
        fi;

        filename=$dirname
        if [[ -f "$filename" ]]; then
            for i in $( seq 0 $n );do echo -n ' ';done;echo " |--$filename"
            grep -rn $LICENSE_TOKEN $filename >/dev/null
            if [ $? -eq 1 ]; then
                if [ "${filename##*.}" = "c" -o "${filename##*.}" = "cpp" -o "${filename##*.}" = "java" ]; then
                    add_c_license $filename 
                    for i in $( seq 0 $n );do echo -n ' ';done;echo " |--add license for $filename... "
                elif [ "${filename##*.}" = "py" -o "${filename##*.}" = "yml" -o "${filename##*.}" = "yaml" -o "${filename##*.}" = "sh" ]; then
                    add_bash_license $filename 
                    for i in $( seq 0 $n );do echo -n ' ';done;echo " |--add license for $filename... "
                elif [ "${filename##*.}" = "xml" ]; then
                    add_xml_license $filename
                    for i in $( seq 0 $n );do echo -n ' ';done;echo " |--add license for $filename... "
                fi;
            fi;
        fi;
    done;  
}  
  
Searchfile $nowdir 

# Revert changes of skipped files, e.g. __init__.py

git checkout \*\*/__init__.py
