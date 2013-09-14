# TODO
# - elasticsearch
# - htaccess
%define		php_min_version 5.3.0
Summary:	PHP and Git based pastebin
Name:		phorkie
Version:	0.3.1
Release:	0.7
License:	AGPL v3
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/phorkie/%{name}-%{version}.tar.bz2
# Source0-md5:	46b93c9270ea7950cea9ac8c58641378
Patch0:		geshi-path.patch
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://sourceforge.net/projects/phorkie/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	git-core
Requires:	php(core) >= %{php_min_version}
Requires:	php-geshi
Requires:	php-markdown
Requires:	php-pear-Date_HumanDiff
Requires:	php-pear-OpenID
Requires:	php-pear-Pager
Requires:	php-pear-Services_Libravatar
Requires:	php-pear-VersionControl_Git
Requires:	php-twig-Twig
Requires:	php-zz-MIME_Type_PlainDetect
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Self-hosted pastebin software written in PHP. Pastes are editable, may
have multiple files and are stored in git repositories.

%prep
%setup -q
%patch0 -p1

mv data/config.php.dist config.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a data scripts src www $RPM_BUILD_ROOT%{_appdir}
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/data

cp -p config.php $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.rst NEWS.rst ChangeLog
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
