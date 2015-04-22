Name:		mysql-connector-net
Version:	6.9.6
Release:	1%{?dist}
Summary:	Mono ADO.NET driver for MySQL

Group:		Development/Languages
License:	GPLv2
URL:		http://dev.mysql.com/downloads/connector/net/
Source0:	http://cdn.mysql.com/Downloads/Connector-Net/%{name}-%{version}-src.zip
Source1:	mysql-connector-net.pc
Patch0:		mysql-connector-net-mono.patch
BuildRequires:	mono-devel dos2unix
Requires:	mono-data

%description
Connector/Net is a fully-managed ADO.NET driver for MySQL.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
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
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_prefix}/lib/mono/gac/
%{__mkdir_p} %{buildroot}/%{_prefix}/lib/mono/mysql-connector-net/
%{__mkdir_p} %{buildroot}/%{_libdir}/pkgconfig

install -p -m0644 %SOURCE1 %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 Source/MySql.Data/bin/v4.5/Debug/MySql.Data.dll %{buildroot}%{_prefix}/lib/mono/mysql-connector-net/

gacutil -i %{buildroot}%{_prefix}/lib/mono/mysql-connector-net/MySql.Data.dll -f -package mysql-connector-net -root %{buildroot}/%{_prefix}/lib

%files
%doc CHANGES COPYING README
%{_prefix}/lib/mono/gac/*
%{_prefix}/lib/mono/mysql-connector-net/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Nov 21 2013 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.9.6-1
- Initial packaging
