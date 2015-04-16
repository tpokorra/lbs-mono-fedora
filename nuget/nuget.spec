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

%define tarballversion 2.8.3+md58+dhx1

Name:           nuget
Version:        2.8.3
Release:        1
Summary:        Package manager for NuGet repositories
License:        MIT
Group:          Development/Libraries/Other
Url:            http://nuget.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        nuget_%{tarballversion}.orig.tar.bz2
Source1:	nuget-core.pc
Source2:	nuget.sh
Source3:	build-minimal.sh
Patch0:		fix_xdt_hintpath
BuildRequires:  mono-devel mono-winfx
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

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

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

%changelog
* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-0
- copy from Xamarin nuget spec
