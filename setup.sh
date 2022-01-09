#color codes

c_green="\033[1;32m"
c_yellow="\033[1;33m"
c_blue="\033[1;34m"
c_magenta="\033[1;35m"
c_cyan="\033[1;36m"

echo -e "$c_green [*]Setting up mpv-android"
cd ..
cd usr
cd bin
touch mpv
echo "IyEvZGF0YS9kYXRhL2NvbS50ZXJtdXgvZmlsZXMvdXNyL2Jpbi9zaA==" | base64 -d > mpv
echo "" >> mpv
echo "YW0gc3RhcnQgLS11c2VyIDAgLWEgYW5kcm9pZC5pbnRlbnQuYWN0aW9uLlZJRVcgLWQgIiQxIiAtbiBpcy54eXoubXB2Ly5NUFZBY3Rpdml0eQ==" | base64 -d >> mpv
chmod +x mpv

echo -e "$c_yellow [*]Setting up python"
pkg install clang
pkg install python3

echo -e "$c_blue [*]Installing python packages"
pip install pycryptodome
pip install pycryptodomex
pip install yarl
pip install requests
pip install termcolor
pip install beautifulsoup4
pkg instal libxslt
pkg install libxml2
CFLAGS="-O0" pip install lxml

clear
echo -e "$c_green [*]Installation Done"


