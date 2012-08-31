apt-get update
## Need easy_install, pip
apt-get install -y python-setuptools
## Need this for a reason unknown to me
apt-get install -y libpq-dev python-dev
## git pip to git goods!
easy_install pip
# libevent
apt-get install -y libevent-dev
## get git for pip via git
apt-get install -y git-core
## Curl
apt-get install -y curl
## PEP8
apt-get install -y pep8
## pyflakes
apt-get install -y pyflakes
## cmake
apt-get install -y cmake
## RabbitMQ
apt-get install -y rabbitmq-server
## Htop
apt-get install -y htop
# Be a vagrant user
su vagrant
## Ruby & RVM
curl -L https://get.rvm.io | bash -s stable
## Make RVM work
source /etc/profile.d/rvm.sh
# Install latest ruby
/usr/local/rvm/bin/rvm install 1.9.2
# Go forth and ruby 1.9.2
rvm use 1.9.2
## Foreman
gem install foreman --no-ri --no-rdoc
## make ~/site default and use rvm 1.9.2
echo "cd ~/site/

rvm use 1.9.2" >> ~/.bashrc
echo "

Provisioning Complete. CTRL+C if this shows for more than a few seconds...

"
