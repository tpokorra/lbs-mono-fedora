#
# spec file for package nuget
#
# Copyright (c) 2014 Xamarin, Inc (http://www.xamarin.com)
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           nuget
Version:        2.8.3+md58+dhx1
Release:        0
Summary:        Package manager for NuGet repositories
License:        MIT
Group:          Development/Libraries/Other
Url:            http://nuget.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        nuget_%{version}.orig.tar.bz2
Source1:	nuget-core.pc
Source2:	nuget.sh
Source3:	build-minimal.sh
Patch0:		fix_xdt_hintpath
BuildRequires:  mono-devel
BuildArch:      noarch

%description
NuGet is the package manager for the Microsoft
development platform including .NET. The NuGet client
tools provide the ability to produce and consume
packages. The NuGet Gallery is the central package
repository used by all package authors and consumers.

%prep
%setup -n nuget-git
%patch0 -p1

%build
%{?exp_env}
%{?env_options}
%{SOURCE3}

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_prefix}/lib/nuget
%{__mkdir_p} %{buildroot}%{_datadir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_datadir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE2}`
sed -i -e 's/cli/mono/' %{buildroot}%{_bindir}/*
%{__install} -m0755 src/CommandLine/bin/Release/NuGet.Core.dll %{buildroot}%{_prefix}/lib/nuget/
%{__install} -m0755 xdt/XmlTransform/bin/Debug/Microsoft.Web.XmlTransform.dll %{buildroot}%{_prefix}/lib/nuget/
%{__install} -m0755 src/CommandLine/bin/Release/NuGet.exe %{buildroot}%{_prefix}/lib/nuget/

%files
%defattr(-,root,root)
%_prefix/lib/nuget
%_datadir/pkgconfig/nuget-core.pc
%_bindir/*
