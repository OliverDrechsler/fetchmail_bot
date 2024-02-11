#/bin/bash
#/ Description: These script list all installed python modules their version and license

usage() {
    grep '^#/' "$0" | cut -c4-
    exit 0
}
expr "$*" : ".*--help" > /dev/null && usage



set -eu pipefail
IFS=$'\n\t'

echo "Python Modulename;Version Nr.;License Type" >requirements_license.txt
for i in `cat requirements.txt|awk -F'=' '{print $1}'`
do
    IFS=''
    ausgabe=$(pip show $i)
    name=$i
    version=$(grep 'Version:' <<< "$ausgabe"|grep -v "Metadata"|awk -F':' '{print $2}')
    license=$(grep -i 'License:' <<< "$ausgabe"|awk -F':' '{print $2}')
    IFS=$'\n\t'
    echo $name";"$version";"$license >>requirements_license.txt
done

echo "" >>requirements_license.txt
echo "" >>requirements_license.txt
echo "" >>requirements_license.txt
echo "" >>requirements_license.txt

echo "Libirary license report"  >>requirements_license.txt
for i in `cat requirements.txt|awk -F'=' '{print $1}'`
do
    pip show $i >>requirements_license.txt
    echo "" >>requirements_license.txt
    echo "" >>requirements_license.txt
done
