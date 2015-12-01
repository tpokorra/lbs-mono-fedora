%define gitrevision f1f3d1e2d33ef87a261faccfa9ad612edd696a64
Name:           dotnet
Version:        1.0.0
Release:        1%{?dist}
Summary:        .NET Core is a general purpose managed framework

Group:          Development/Languages
License:        MIT
URL:            https://dotnet.github.io/
#Source0:        https://github.com/dotnet/core/archive/v%{version}-rc1.tar.gz
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
#%setup -q -n coreclr-%{version}-rc1
%setup -q -n coreclr-%{gitrevision}

%build

./build.sh

%install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir /usr/share/doc/dotnet
%doc /usr/share/doc/dotnet/copyright
%{_bindir}/dotnet-repl
%{_bindir}/dotnet-repl-csi
%{_bindir}/dotnet-publish
%{_bindir}/dotnet-compile-csc
%{_bindir}/dotnet-compile
%{_bindir}/dotnet
%{_bindir}/dotnet-init
%{_bindir}/dotnet-restore
%{_bindir}/dotnet-compile-native
%dir /usr/share/dotnet
/usr/share/dotnet/*


%changelog
* Tue Dec 01 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 1.0.0-1
- initial package for .NET Core RC1
