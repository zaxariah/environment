Summary: Configuration of various linux development and environment tools
Name: zx-system
Version: %{date}
Release: %{time}
License: BSD
Group: Development/Tools
Requires: zx-system-yum
Requires: zx-system-build
Requires: zx-system-server
BuildRoot: /var/tmp/%{name}-rpmroot
BuildArch: noarch

%define src ../../src

%description

%build

# Lighttpd
mkdir -p $RPM_BUILD_ROOT/etc/lighttpd/conf.d

%install
rm -rf $RPM_BUILD_ROOT

# Yum Client Configuration

mkdir -p $RPM_BUILD_ROOT/srv/yum

mkdir -p $RPM_BUILD_ROOT/etc/yum.repos.d
cp %{src}/yum/zx.repo $RPM_BUILD_ROOT/etc/yum.repos.d

## Packages

%package yum
Summary: Yum client environment configuration
Group: Development/Tools
Requires: createrepo
%description yum

%package build
Summary: Build Tools and Environment
Group: Development/Tools
Requires: subversion >= 1.6.12-0.1.el5.rf
Requires: git >= 1.7.1-2.el5.rf 
Requires: git-svn >= 1.7.1-2.el5.rf
Requires: rpm-build
%description build

%package server
Summary: Server services and tools
Group: Development/Tools
Requires: mysql >= 5.0.77-4.el5_5.3
Requires: mysql-server >= 5.0.77-4.el5_5.3
Requires: lighttpd >= 1.4.26-2.el5
Requires: lighttpd-fastcgi >= 1.4.26-2.el5
%description server

## Pre

%pre yum
rm -f /etc/yum.repos.d/*

## Post

%post yum
createrepo /srv/yum
# Cannot do 'makecache' while yum installing
# yum makecache || true # ignore errors

%post server

# lighttpd
chkconfig lighttpd on
/etc/init.d/lighttpd start
/newservers/openPortInFirewall 80
rm -f /etc/lighttpd/lighttpd.conf
ln -s /etc/lighttpd/lighttpd-zx.conf /etc/lighttpd/lighttpd.conf

# mysql
chkconfig mysqld on
/etc/init.d/mysqld start


## Files

%files

%files yum
/etc/yum.repos.d/*
/srv/yum

%files build

%files server