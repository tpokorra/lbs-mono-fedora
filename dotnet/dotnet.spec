%global gitrevision 03bb9a00a68efac5f1637f53ea0099a2dea47117
%global deliverydir bin/Product/Linux.x64.Debug
Name:           dotnet
Version:        1.0.0
Release:        1%{?dist}
Summary:        .NET Core is a general purpose managed framework

Group:          Development/Languages
License:        MIT
URL:            https://dotnet.github.io/
Source0:        https://github.com/dotnet/coreclr/archive/%{gitrevision}.tar.gz

BuildRequires:  which
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  llvm
BuildRequires:  clang
BuildRequires:  lldb
BuildRequires:  lldb-devel
BuildRequires:  gettext
BuildRequires:  libicu-devel
BuildRequires:  libcurl-devel
BuildRequires:  libunwind-devel
BuildRequires:  lttng-ust-devel
BuildRequires:  libuuid-devel
BuildRequires:  uuid-devel
BuildRequires:  mono-devel

%description
.NET Core is a set of runtime, library and compiler components.
You can create .NET Core apps that run on multiple OSes and CPUs.

%prep
%setup -q -n coreclr-%{gitrevision}

%build

./build.sh skipmscorlib

%install

mkdir -p %{buildroot}%{_bindir}
for f in corerun coreconsole crossgen ilasm ildasm; do cp %{deliverydir}/$f %{buildroot}%{_bindir}; done
mkdir -p %{buildroot}%{_libdir}
cp %{deliverydir}/*.so %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
cp %{deliverydir}/inc/*.h %{buildroot}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# TODO license or copyright
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Wed Jan 06 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 1.0.0-1
- initial package for .NET Core (from git master)
