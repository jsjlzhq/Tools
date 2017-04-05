#!/bin/bash
generateStartScript()
{
    cd $exeName
    outputFile=$1.sh

    echo "#!/bin/bash" >$outputFile
    echo "appName=$1" >>$outputFile
    cat >>$outputFile <<"thisDocument"
thisDir="$(cd `dirname "$0"` && pwd )"
cd "$thisDir"/bin
export LD_LIBRARY_PATH=.:../lib
nohup "$thisDir"/bin/$appName & 
thisDocument
    chmod +x $outputFile
}

prepareDirectories()
{
    if [ ! -e lib ]; then
        mkdir lib
    fi
    rm -f lib/*

    if [ ! -e bin ]; then
        mkdir bin
    fi
    rm -f bin/*
}

#-------------- main --------------------------
if [ $# -lt 2 ]; then
    echo usage: $0 exe pathToSetting
    exit
fi

notFound=`ldd "$1"|grep -i "not found"`
if [ -n "$notFound" ]; then
    echo "Failed to find library. Please set LD_LIBRARY_PATH"
    echo $notFound
    exit 1
fi

settingFile=$2

prepareDirectories
cp "$settingFile" bin

ldd "$1" | awk 'NF == 4 {print $3}; NF == 2 {print $1}' |grep -Ev "^/lib64|^/usr" |xargs -i cp {} lib
mv $1 bin

exeName=`basename $1`

mkdir $exeName
mv lib $exeName
mv bin $exeName

generateStartScript $exeName

echo done
echo Notes:
echo libs under /lib64, and /usr/ and their child directories are not copied
echo you should copy these libs manually 


