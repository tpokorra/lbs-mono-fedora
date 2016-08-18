%global bootstrap 1
%global deliverydir bin/Product/Linux.x64.Release
Name:           dotnet-corefx
Version:        1.0.0
Release:        1%{?dist}
Summary:        This package contains the .NET Core foundational libraries, called CoreFX

License:        MIT
URL:            https://docs.microsoft.com/dotnet/
Source0:        https://github.com/dotnet/corefx/archive/v%{version}.tar.gz

BuildRequires:  clang
BuildRequires:  dotnet-coreclr
BuildRequires:  zlib-devel
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  cmake

%if 0%{bootstrap}
BuildRequires:  msbuild-bin
%else
BuildRequires:  msbuild
%endif

%description

The corefx repo contains the library implementation (called "CoreFX") for .NET Core. It includes System.Collections, System.IO, System.Xml, and many other components.

%prep
%setup -q -n corefx-%{version}

%build

sed -i "s#__generateversionsource=true#__generateversionsource=false#g" build.sh
sed -i "s#\\\$__scriptpath/Tools/corerun#/usr/bin/corerun --clr-path /usr/lib64#g" build.sh
sed -i "s#\\\$__scriptpath/Tools/MSBuild\.exe#/usr/lib64/MSBuild.exe#g" build.sh
sed -i 's#.*__scriptpath/init-tools.sh#echo "not calling init-tools.sh"#g' build.sh
./build.sh x64 Release clean

%install

# TODO
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# TODO license or copyright
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Thu Aug 18 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 1.0.4-1
- initial package
