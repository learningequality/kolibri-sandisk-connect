# With tips from: http://randomsplat.com/id5-cross-compiling-python-for-embedded-linux.html

mkdir -p pybuild
cd pybuild

# download setuptools 
wget https://pypi.python.org/packages/source/s/setuptools/setuptools-18.4.tar.gz#md5=214c6c43bd7035e870c1beab402c48e7
tar xvf setuptools-18.4.tar.gz

# download arm-fsl toolchain
git clone git@github.com:embeddedarm/linux-2.6.35.3-imx28.git

# set path variables
export PATH=$PATH:`pwd`/linux-2.6.35.3-imx28/cross-toolchain/arm-fsl-linux-gnueabi/bin/
export BASE_PYTHON_COMPILATION_PATH=`pwd`

# sqlite3 headers
wget http://backports.debian.org/debian-backports/pool/main/s/sqlite3/libsqlite3-dev_3.7.13-1~bpo60+1_armel.deb
ar vx libsqlite3-dev_3.7.13-1~bpo60+1_armel.deb
tar xzf data.tar.gz
mv usr/* .

# zlib
wget http://www.gzip.org/zlib/zlib-1.1.4.tar.gz
tar xvf zlib-1.1.4.tar.gz
cd zlib-1.1.4
CC=arm-fsl-linux-gnueabi-gcc \
LDSHARED="arm-fsl-linux-gnueabi-gcc -shared -Wl,-soname,libz.so.1" \
./configure --shared --prefix=$BASE_PYTHON_COMPILATION_PATH
make
make install
cd ..

# openssl
wget https://www.openssl.org/source/openssl-1.0.1i.tar.gz
tar xvf openssl-1.0.1i.tar.gz
cd openssl-1.0.1i
./Configure dist --prefix=$BASE_PYTHON_COMPILATION_PATH
make CC="arm-fsl-linux-gnueabi-gcc" AR="arm-fsl-linux-gnueabi-ar r" RANLIB="arm-fsl-linux-gnueabi-ranlib"
make install
cd ..

# python dependencies
wget https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
tar -xvzf Python-2.7.3.tgz
cd Python-2.7.3

# build for the host system
./configure
make python Parser/pgen
mv python hostpython
mv Parser/pgen Parser/hostpgen
make distclean

# patch it up
wget http://randomsplat.com/wp-content/uploads/2012/10/Python-2.7.3-xcompile.patch
patch -p1 < Python-2.7.3-xcompile.patch

# configure
CC=arm-fsl-linux-gnueabi-gcc \
CXX=arm-fsl-linux-gnueabi-g++ \
AR=arm-fsl-linux-gnueabi-ar \
RANLIB=arm-fsl-linux-gnueabi-ranlib \
PYTHON_XCOMPILE_DEPENDENCIES_PREFIX=$BASE_PYTHON_COMPILATION_PATH \
./configure --host=arm-linux --build=i686-pc-linux-gnu --prefix=$BASE_PYTHON_COMPILATION_PATH/tmp

# build
make clean
make HOSTPYTHON=./hostpython \
PYTHON_XCOMPILE_DEPENDENCIES_PREFIX=$BASE_PYTHON_COMPILATION_PATH \
HOSTPGEN=./Parser/hostpgen \
BLDSHARED="arm-fsl-linux-gnueabi-gcc -shared" \
HOSTARCH=arm-linux \
BUILDARCH=x86_64-linux-gnu \
CROSS_COMPILE=arm-fsl-linux-gnueabi- \
CROSS_COMPILE_TARGET=yes | tee make.log 2>&1

# "install"
make install HOSTPYTHON=./hostpython \
BLDSHARED="arm-fsl-linux-gnueabi-gcc -shared" \
HOSTARCH=arm-linux \
BUILDARCH=x86_64-linux-gnu \
CROSS_COMPILE=arm-fsl-linux-gnueabi- \
CROSS_COMPILE_TARGET=yes prefix=$BASE_PYTHON_COMPILATION_PATH/Python-2.7.3/_install | tee install.log 2>&1

# create a target directory for a minimal version of the installation
cd $BASE_PYTHON_COMPILATION_PATH/Python-2.7.3/
rm -r _install_minimal
mkdir -p _install_minimal/bin
mkdir -p _install_minimal/usr/lib/python2.7
mkdir -p _install_minimal/usr/include

# copy in the python binary file
cd $BASE_PYTHON_COMPILATION_PATH/Python-2.7.3/
cp _install/bin/python2.7 _install_minimal/bin/python

# bundle up the lib files into a zip file, after removing unneeded bits
cd $BASE_PYTHON_COMPILATION_PATH/Python-2.7.3/_install/lib/
rm -r python2.7-minimal
cp -r python2.7 python2.7-minimal
cd python2.7-minimal
rm -r site-packages config lib-dynload
rm *.doc *.txt
zip -r -y python27.zip .

# copy in the python library files
cd $BASE_PYTHON_COMPILATION_PATH/Python-2.7.3
cp _install/lib/python2.7-minimal/python27.zip _install_minimal/usr/lib/
cp -r _install/lib/python2.7/config _install_minimal/usr/lib/python2.7/
cp -r _install/lib/python2.7/lib-dynload _install_minimal/usr/lib/python2.7/
cp -r _install/lib/python2.7/site-packages _install_minimal/usr/lib/python2.7/
cp -r _install/include/python2.7 _install_minimal/usr/include/
cd _install_minimal
rm ../../python.zip
zip -r ../../python.zip .
cd ../../..

echo "Compilation complete (hopefully successfully). Now, connect to the Sandisk device's wifi hotspot,"
echo "and then run the local ./upload_python.sh script."

