%global debug_package %{nil}
%global gittag c0526b74cf131636feb578eab5535d4ef15008aa

Name:           nunit-gui
Version:        3.5
Release:        1%{?dist}
Summary:        New Gui test runner for NUnit 3.0
License:        MIT with advertising
Group:          Development/Libraries
Url:            http://www.nunit.org/
Source0:        https://github.com/nunit/nunit-gui/archive/%{gittag}.tar.gz
# TODO: add script to /usr/bin to start nunit3-gui
Patch0:         nunit-gui-hintpath.patch
BuildRequires:  mono-devel
BuildRequires:  nunit-devel >= 3.5
BuildRequires:  nunit-console
BuildRequires:  mono-cecil-devel
ExclusiveArch:  %{mono_arches}

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%prep
%setup -qn nunit-gui-%{gittag}

%patch0 -p1
find . -name "*.csproj" -print -exec sed -i 's#<TargetFrameworkVersion>.*</TargetFrameworkVersion>#<TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g; s#NET_2_0#NET_4_5#g; s#net-2.0#net-4.5#g' {} \;

%build

# Remove prebuilt binaries
find . -name "*.dll" -print -delete
find . -name "*.exe" -print -delete

%{?exp_env}
%{?env_options}

xbuild /property:Configuration=Release src/nunit.uikit/nunit.uikit.csproj
xbuild /property:Configuration=Release src/nunit-gui/nunit-gui.csproj
rm -f %{_builddir}/%{?buildsubdir}/bin/Release/nunit.engine.dll
rm -f %{_builddir}/%{?buildsubdir}/bin/Release/nunit.engine.api.dll
rm -f %{_builddir}/%{?buildsubdir}/bin/Release/Mono.Cecil.dll

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_monodir}/nunit
find %{_builddir}/%{?buildsubdir}/bin -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
find %{_builddir}/%{?buildsubdir}/bin -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;

%files
%{_monodir}/nunit/*

%changelog
* Sat Oct 08 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.5-1
- initial package
