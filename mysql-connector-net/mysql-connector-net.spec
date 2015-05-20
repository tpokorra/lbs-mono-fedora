%global debug_package %{nil}
%if 0%{?el6}
%global mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
%if 0%{?rhel}%{?el6}%{?el7}
# see https://fedorahosted.org/fpc/ticket/395
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

Name:           mysql-connector-net
Version:        6.9.6
Release:        3%{?dist}
Summary:        Mono ADO.NET driver for MySQL

Group:          Development/Languages
License:        GPLv2
URL:            http://dev.mysql.com/downloads/connector/net/
Source0:        http://cdn.mysql.com/Downloads/Connector-Net/%{name}-%{version}-src.zip
Source1:        mysql-connector-net.pc
Patch0:         mysql-connector-net-mono.patch

BuildRequires:  mono-devel dos2unix

Requires:       mono-data
# Mono only available on these:
ExclusiveArch: %{mono_arches}

%description
Connector/Net is a fully-managed ADO.NET driver for MySQL.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%prep
%setup -q -c
dos2unix Source/MySql.Data/MySql.Data.csproj
%patch0 -p1

%build
xbuild /property:Configuration=Debug Source/MySql.Data/MySql.Data.csproj

%install
%{__mkdir_p} %{buildroot}/%{_libdir}/pkgconfig
%{__mkdir_p} %{buildroot}/%{_monogacdir}/
%{__mkdir_p} %{buildroot}/%{_monodir}/mysql-connector-net/

install -p -m0644 %SOURCE1 %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 Source/MySql.Data/bin/v4.5/Debug/MySql.Data.dll %{buildroot}%{_monodir}/mysql-connector-net/

gacutil -i %{buildroot}%{_monodir}/mysql-connector-net/MySql.Data.dll -f -package mysql-connector-net -root %{buildroot}/%{_prefix}/lib

%files
%doc CHANGES README
%license COPYING
%{_monogacdir}/*
%{_monodir}/mysql-connector-net/*

%files devel
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon May 18 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.9.6-3
- Use global insted define

* Wed Apr 22 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.9.6-2
- Add pc file
- Fix build for mono

* Thu Nov 21 2013 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.9.6-1
- Initial packaging
