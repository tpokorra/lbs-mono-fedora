# This is master branch. Crossplatform is not supported
#%global tarballversion 14.0.25420.1-ish
# from the branch https://github.com/Microsoft/msbuild/tree/xplat
%global tarballversion 204cfd215fdc1c92322b0b22165cc8c4c3259e02
%global bootstrap 1
Name:           msbuild
Version:        14.0.25420
Release:        1%{?dist}
Summary:        The Microsoft Build Engine is a platform for building applications.

License:        MIT
URL:            https://github.com/Microsoft/msbuild
Source0:        https://github.com/Microsoft/msbuild/archive/%{tarballversion}.tar.gz

BuildRequires:  dotnet-coreclr
%if 0%{bootstrap}
BuildRequires:  msbuild-bin
%else
BuildRequires:  msbuild
%endif

%description
The Microsoft Build Engine, which is also known as MSBuild, provides an XML schema for a project file that controls how the build platform processes and builds software. Visual Studio uses MSBuild, but MSBuild does not depend on Visual Studio. By invoking msbuild.exe on your project or solution file, you can orchestrate and build products in environments where Visual Studio isn't installed.

%prep
%setup -q -n %{name}-%{tarballversion}

%build

#sed -i "s#CLR2\\\#clr2\\\#g" src/XMakeCommandLine/MSBuildTaskHost/MSBuildTaskHost.csproj
#sed -i "s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>#<TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g" dir.props
#sed -i "s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>#<TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g;s#System\.XML#System.Xml#g" src/XMakeCommandLine/MSBuildTaskHost/MSBuildTaskHost.csproj

sed -i 's#eval.*init-tools.*#echo "not running init-tools.sh"#g' cibuild.sh
sed -i 's#RUNTIME_HOST=.*#RUNTIME_HOST="/usr/bin/corerun"#g' cibuild.sh
sed -i 's#MSBUILD_EXE=.*#MSBUILD_EXE="/usr/lib64/tools/MSBuild.exe"#g' cibuild.sh

./cibuild.sh --host CoreCLR --target CoreCLR || exit -1

%install

#TODO
#mkdir -p %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{_libdir}
#mkdir -p %{buildroot}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# TODO license or copyright
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Thu Aug 18 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 1.0.4-1
- initial package for msbuild
