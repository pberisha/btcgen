#Requirenemts 

apt-get install libgmp3-dev gawk bison

wget -4c https://ftp.gnu.org/gnu/glibc/glibc-2.29.tar.gz
tar -zxvf glibc-2.29.tar.gz
cd glibc-2.29
mkdir build_dir
cd build_dir
sudo ../configure --prefix=/opt/glibc
sudo make
sudo make install


sudo mv /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6.backup
sudo cp ~/glibc-2.29/build_dir/math/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6