Name:           msbuild-bin
Version:        14.1.0
Release:        1%{?dist}
Summary:        The Microsoft Build Engine is a platform for building applications.

License:        MIT
URL:            https://dotnet.myget.org/feed/dotnet-buildtools/package/nuget/Microsoft.Build.Mono.Debug
Source0:        https://dotnet.myget.org/F/dotnet-buildtools/api/v2/package/Microsoft.Build.Mono.Debug/14.1.0.0-prerelease 

BuildRequires:  unzip

%description
This package contains just the binary files for bootstrapping MSBuild.

%prep

%build

cd %{build} && unzip %{SOURCE0} 

%install

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/tools
cp -R lib/* %{buildroot}%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# TODO license or copyright
%{_libdir}/*

%changelog
* Thu Aug 18 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 14.1.0-1
- initial package for msbuild
