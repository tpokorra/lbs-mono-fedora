Name:		mysql-connector-net
Version:	6.9.6
Release:	1%{?dist}
Summary:	Mono ADO.NET driver for MySQL

Group:		Development/Languages
License:	GPLv2
URL:		http://dev.mysql.com/downloads/connector/net/
Source0:	http://cdn.mysql.com/Downloads/Connector-Net/%{name}-%{version}-src.zip
Patch0:		mysq-connector-net-mono.patch
BuildRequires:	mono-devel dos2unix
Requires:	mono-data

%description
Connector/Net is a fully-managed ADO.NET driver for MySQL.

%prep
%setup -q -c
dos2unix Source/MySql.Data/MySql.Data.csproj
%patch0 -p1

%build
#xbuild MySQLClient-mono-fedora.sln

xbuild /property:Configuration=Debug Source/MySql.Data/MySql.Data.csproj

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/

#Fix file name not match to assemblies names
#mv v4/mysql.data.dll v4/MySql.Data.dll
#mv v4/mysql.data.entity.dll v4/MySql.Data.Entity.dll
#mv v4/mysql.web.dll v4/MySql.Web.dll

#gacutil -i v4/MySql.Data.dll -f -package mysql-connector-net -root %{buildroot}/%{_prefix}/lib
#gacutil -i v4/MySql.Data.Entity.dll -f -package mysql-connector-net -root %{buildroot}/%{_prefix}/lib
#gacutil -i v4/MySql.Web.dll -f -package mysql-connector-net -root %{buildroot}/%{_prefix}/lib

%files
%doc CHANGES COPYING README
#%{_prefix}/lib/mono/gac/*
#%{_prefix}/lib/mono/mysql-connector-net/*

%changelog
* Thu Nov 21 2013 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.9.6-1
- Initial packaging
