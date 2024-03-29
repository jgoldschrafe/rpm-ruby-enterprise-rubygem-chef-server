%define ruby_dist ruby-enterprise
%define ruby_dist_dash %{ruby_dist}-
%define _prefix /opt/ruby-enterprise
%define _gem %{_prefix}/bin/gem
%define _ruby %{_prefix}/bin/ruby

# Generated from chef-server-0.10.0.rc.1.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(%{_ruby} -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{_ruby} -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-server
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A meta-gem to install all server components of the Chef configuration management system
Name: %{?ruby_dist_dash}rubygem-%{gemname}
Version: 0.10.4
Release: 1%{?buildstamp}%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/chef
Source0: http://rubygems.org/downloads/%{gemname}-%{version}.gem
Source1: chef-server.init
Source2: chef-server.sysconfig
Source3: chef-server.logrotate
Source4: config.rb
Source5: setup-chef-server.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{?ruby_dist_dash}rubygems
Requires: %{?ruby_dist_dash}rubygem(chef-server-api) = %{version}
Requires: %{?ruby_dist_dash}rubygem(chef-server-webui) = %{version}
Requires: %{?ruby_dist_dash}rubygem(chef-expander) = %{version}
Requires: %{?ruby_dist_dash}rubygem(chef-solr) = %{version}
Requires: rabbitmq-server
Requires: java-1.6.0-openjdk-devel
Requires: java-1.6.0-openjdk
Requires: couchdb
Requires: zlib-devel
Requires: libxml2-devel
Requires: ntp

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

BuildRequires: rubygems
BuildArch: noarch
Provides: %{?ruby_dist_dash}rubygem(%{gemname}) = %{version}

%description
A meta-gem to install all server components of the Chef configuration
management system


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/chef/{ca,cache,sandboxes,checksums,nodes,roles,cookbooks,site-cookbooks}
mkdir -p %{buildroot}/var/chef/openid/{store,cstore}
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/chef
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/srv/chef/support
mkdir -p %{buildroot}/var/run/chef
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sbindir}

%{_gem} install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/chef-server
chmod +x %{buildroot}/etc/rc.d/init.d/chef-server

cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/chef-server

cp %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/chef/server.rb
cp %{SOURCE5} %{buildroot}%{_sbindir}/
chmod +x %{buildroot}%{_sbindir}/setup-chef-server.sh


%clean
rm -rf %{buildroot}

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add chef-server

if [ -z "`/usr/bin/id chef 2> /dev/null`" ]; then
	%{_sbindir}/adduser chef >/dev/null 2>&1 
fi
chown -R chef %{_sysconfdir}/chef >/dev/null 2>&1
chown -R chef /var/chef >/dev/null 2>&1

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service chef-server stop >/dev/null 2>&1
    /sbin/chkconfig --del chef-server
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-server restart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, -)
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/sysconfig/chef-server
%config(noreplace) %{_sysconfdir}/chef/server.rb
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-server
%{_sysconfdir}/rc.d/init.d/chef-server
%{_sbindir}/setup-chef-server.sh
/var/chef


%changelog
* Mon Oct  3 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.10.4-1.hhg
- Rebuild for Ruby Enterprise Edition

* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.4-1
- preparing for 0.10.4

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-4
- updated

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-3
- rubygem-chef-server.spec

* Mon Jul 04 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-2
- depend on 0.10.2 chef gems

* Mon Jul 04 2011 Sergio Rubio <srubio@abiquo.com> - 0.10.2-1
- upstream update

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-2
- create missing dir and fix permissions

* Tue May 03 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-1
- upstream update

* Mon May 02 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.2-1
- upstream update

* Fri Apr 29 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-3
- fixes in setup-chef-server.sh

* Fri Apr 29 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-2
- add init script
- create default dirs
- add logrotate and server.rb configs
- create chef user

* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-1
- Initial package
