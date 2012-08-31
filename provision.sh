apt-get update
## Need easy_install, pip
apt-get install -y python-setuptools
## Need this for a reason unknown to me
apt-get install -y libpq-dev python-dev
## git pip to git goods!
easy_install pip
# libevent
apt-get install -y libevent-dev
## ruby support
apt-get install -y ruby-full
## get git for pip via git
apt-get install git-core
## Curl
apt-get install curl
## Ruby & RVM
curl -L https://get.rvm.io | bash -s stable --ruby
## Make RVM work
source /home/vagrant/.rvm/scripts/rvm
## Foreman
gem install foreman --no-ri --no-rdoc
## PEP8
apt-get install -y pep8
## pyflakes
apt-get install -y pyflakes
## cmake
apt-get install -y cmake
## make ~/site default
echo "cd ~/site/" >> ~/.bashrc
echo "

Provisioning Complete. CTRL+C if this shows for more than a few seconds...

"
