%global debug_package %{nil}
%global gittag bb29539d178a601253ad7e8720d854bb1fe50ea7

Name:           nunit-console
Version:        3.5
Release:        1%{?dist}
Summary:        NUnit Console runner and test engine
License:        MIT with advertising
Group:          Development/Libraries
Url:            http://www.nunit.org/
Source0:        https://github.com/nunit/nunit-console/archive/%{gittag}.tar.gz
Patch0:         nunit-console-net-4.5.patch
BuildRequires:  mono-devel
BuildRequires:  nunit-devel >= 3.5
ExclusiveArch:  %{mono_arches}

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%prep
%setup -qn nunit-console-%{gittag}

%patch0 -p1
find . -name "*.csproj" -print -exec sed -i 's#<TargetFrameworkVersion>.*</TargetFrameworkVersion>#<TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g; s#NET_2_0#NET_4_5#g; s#net-2.0#net-4.5#g' {} \;

sed -i 's#namespace System.Runtime.CompilerServices#namespace System.Runtime.CompilerServicesOff#g' src/NUnitEngine/nunit.engine/XmlHelper.cs
sed -i 's#namespace System.Runtime.CompilerServices#namespace System.Runtime.CompilerServicesOff#g' src/NUnitConsole/nunit3-console/SafeAttributeAccess.cs
sed -i 's#<TreatWarningsAsErrors>true</TreatWarningsAsErrors>#<TreatWarningsAsErrors>false</TreatWarningsAsErrors>#g' src/NUnitEngine/nunit.engine/nunit.engine.csproj
sed -i 's#<ProjectType>Local</ProjectType>##g' src/NUnitEngine/mock-assembly/mock-assembly.csproj

%build

# Remove prebuilt binaries
find . -name "*.dll" -print -delete
find . -name "*.exe" -print -delete

%{?exp_env}
%{?env_options}

xbuild /property:Configuration=Release NUnitConsole.sln

rm -f %{_builddir}/%{?buildsubdir}/bin/Release/nunit.framework.dll

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_monodir}/nunit
find %{_builddir}/%{?buildsubdir}/bin -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
find %{_builddir}/%{?buildsubdir}/bin -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
for i in mock-assembly.dll nunit.engine.dll nunit.engine.api.dll; do
    gacutil -i %{buildroot}%{_monodir}/nunit/$i -package nunit -root %{buildroot}%{_monodir}/../
done

%files
%{_monogacdir}/nunit*
%{_monogacdir}/mock-assembly/*
%{_monodir}/nunit/*

%changelog
* Sat Oct 08 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.5-1
- initial package
