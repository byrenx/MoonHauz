#!/bin/bash

dir_resolve()
{
    cd "$1" 2>/dev/null || return $?    # cd to desired directory; if fail, quell any error messages but return exit status
    echo "`pwd -P`" # output full, link-resolved path
}

dir=$( cd "$( dirname "$0" )" && pwd )
packages="`dir_resolve \"$dir/../../packages\"`"

echo $packages

echo ' --> Cleaning'

rm -rf "$packages/pytz" 2>/dev/null
rm $packages/gdata.zip $packages/atom.zip $packages/google-api* $packages/wtforms.zip $packages/utils.zip $packages/protopigeon.zip 2>/dev/null

echo ' --> Starting Packaging'

echo ' --> Packaging pytz'
cd /tmp
rm -rf pytz-appengine 2>/dev/null
git clone https://github.com/brianmhunt/pytz-appengine.git
cd pytz-appengine
python build.py all
cp -r pytz $packages

echo ' --> Packaging gdata'
cd /tmp
rm -rf gdata gdata.zip 2>/dev/null
hg      clone https://code.google.com/p/gdata-python-client gdata
cd gdata/src
zip ../../gdata.zip -rq *
cd ../../
cp gdata.zip $packages


echo ' --> Getting api-client'
cd $packages
rm google-api-python-client-gae-1.2.zip 2>/dev/null
wget https://google-api-python-client.googlecode.com/files/google-api-python-client-gae-1.2.zip


echo ' --> Packaging wtforms & wtforms-json'
cd /tmp
rm -rf wtforms.zip wtforms wtforms-json six 2>/dev/null

git clone https://github.com/wtforms/wtforms.git
cd wtforms
zip ../wtforms.zip -rq wtforms AUTHORS.txt LICENSE.txt
cd ../

git clone https://github.com/kvesteri/wtforms-json.git wtforms-json
cd wtforms-json
zip -r ../wtforms.zip wtforms_json LICENSE
cd ../

hg clone https://bitbucket.org/gutworth/six six
cd six
zip -r ../wtforms.zip six.py
cd ../

cp wtforms.zip $packages


echo ' --> Packaging protopigeon'
cd /tmp
rm -rf protopigeon.zip protopigeon 2>/dev/null

git clone git@bitbucket.org:jonparrott/protopigeon.git protopigeon
cd protopigeon
zip ../protopigeon.zip -rq protopigeon license.txt
cd ../
cp protopigeon.zip $packages
