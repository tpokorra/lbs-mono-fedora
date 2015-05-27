%if 0%{?el6}
%global mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:           nuget
Version:        2.8.3
Release:        1
Summary:        Package manager for NuGet repositories
License:        MIT
Group:          Development/Libraries
Url:            http://nuget.org/

%global tarballversion %{version}+md58+dhx1
Source0:        http://download.mono-project.com/sources/%{name}/%{name}-%{tarballversion}.tar.bz2
Source1:        nuget-core.pc
Source2:        nuget.sh
Patch0:         nuget-fix_xdt_hintpath
BuildRequires:  mono-devel mono-winfx

ExclusiveArch:  %{mono_arches}

%description
NuGet is the package manager for the Microsoft
development platform including .NET. The NuGet client
tools provide the ability to produce and consume
packages. The NuGet Gallery is the central package
repository used by all package authors and consumers.

%prep
%setup -qn nuget-git
%patch0 -p1

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
%{?exp_env}
%{?env_options}

xbuild xdt/XmlTransform/Microsoft.Web.XmlTransform.csproj
xbuild src/Core/Core.csproj /p:Configuration="Mono Release"
xbuild src/CommandLine/CommandLine.csproj /p:Configuration="Mono Release"

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
%_prefix/lib/nuget
%_datadir/pkgconfig/nuget-core.pc
%_bindir/*

%changelog
* Wed May 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.8.3-2
- Use xbuild option to build with mono 4
- Use global insted define

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-0
- copy from Xamarin nuget spec
