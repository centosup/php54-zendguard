# spec file for php54-zendguard
#
# Copyright (c) 2012-2014 centosup.ispsystem.info
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php54-zendguard}
%global extname       zendguard
%global debug_package %{nil}
%global with_zts      0%{?__ztsphp:1}

Name:          php54-zendguard
Summary:       Zend Guard Loader
Version:       5.6.0
Release:       1%{?dist}
License:       Distribuable
Group:         Development/Languages

URL:           http://www.zend.com
Source0:       http://downloads.zend.com/guard/6.0.0/ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php54-devel

# ABI check
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Loader for ZendGuard Encoded Files.

%prep
%setup -q -T -c

tar xvf %{SOURCE0}

# Drop in the bit of configuration
cat > %{extname}.nts << 'EOF'
; Enable %{extname} extension module
zend_extension = %{php_extdir}/%{extname}.so
EOF

%build
# tarball provides binaries

%install
rm -rf %{buildroot}

install -D -pm 755 ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64/php-5.4.x/ZendGuardLoader.so %{buildroot}%{php_extdir}/%{extname}.so
install -D -m 644 %{extname}.nts %{buildroot}%{php_inidir}/%{extname}.ini

%check
# simple module load test
%{__php} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep 'Zend Guard'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64/*.txt

%config(noreplace) %{php_inidir}/%{extname}.ini
%{php_extdir}/%{extname}.so
