Name:           redis
Version:        redis_version
Release:        0
Summary:        Redis.IO
Group:          Applications/Databases
License:        GPL
URL:            https://redis.io/
Vendor:         Redis.IO
Source:         https://download.redis.io/releases/%{name}-%{version}.tar.gz
Prefix:         %{_prefix}
BuildRoot:      %{_tmppath}/%{name}-root

%description
Redis.IO custom RPM package

%prep
%setup -q -n %{name}-%{version}

%build
make
make test

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make PREFIX=${RPM_BUILD_ROOT}/usr/local install
install -d -m 755 ${RPM_BUILD_ROOT}/usr/bin
install -d -m 755 ${RPM_BUILD_ROOT}/etc/init.d
install -m 755 %{_sourcedir}/redis-sentinel-shutdown ${RPM_BUILD_ROOT}/usr/bin/redis-sentinel-shutdown
install -m 755 %{_sourcedir}/redis-sentinel ${RPM_BUILD_ROOT}/etc/init.d/redis-sentinel

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/local/bin/redis-benchmark
/usr/local/bin/redis-check-aof
/usr/local/bin/redis-cli
/usr/local/bin/redis-sentinel
/usr/local/bin/redis-server
/etc/init.d/redis-sentinel
/usr/bin/redis-sentinel-shutdown
/usr/local/bin/redis-check-rdb

%post
mkdir /etc/redis /var/lib/redis
ln -s /usr/local/bin/redis-benchmark /usr/bin/redis-benchmark
ln -s /usr/local/bin/redis-check-aof /usr/bin/redis-check-aof
ln -s /usr/local/bin/redis-check-dump /usr/bin/redis-check-dump
ln -s /usr/local/bin/redis-cli /usr/bin/redis-cli
ln -s /usr/local/bin/redis-sentinel /usr/bin/redis-sentinel
ln -s /usr/local/bin/redis-server /usr/bin/redis-server
firewall-cmd --zone=public --add-port=26379/tcp --permanent
firewall-cmd --zone=public --add-port=26379/udp --permanent
chkconfig --add redis-sentinel
chkconfig redis-sentinel on
mkdir /var/lib/redis/sentinel_26379
