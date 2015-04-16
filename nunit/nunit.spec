#
# spec file for package nunit
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

Name:           NUnit
Version:        2.6.3
Release:        0
Summary:        Unit test framework for CLI
License:        MIT
Group:          Development/Libraries/Other
Url:            http://www.nunit.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        nunit_%{version}+dfsg.orig.tar.gz
Source1:	nunit.pc
Source2:	nunit-gui.sh
Source3:	nunit-console.sh
BuildRequires:  mono-devel
BuildArch:      noarch

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.
.
NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%prep
%setup

%build
%{?exp_env}
%{?env_options}
xbuild /property:Configuration=Debug ./src/NUnitCore/core/nunit.core.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitCore/interfaces/nunit.core.interfaces.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitFramework/framework/nunit.framework.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitMocks/mocks/nunit.mocks.csproj
xbuild /property:Configuration=Debug ./src/ClientUtilities/util/nunit.util.dll.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console/nunit-console.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console-exe/nunit-console.exe.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui/nunit-gui.csproj
xbuild /property:Configuration=Debug ./src/GuiComponents/UiKit/nunit.uikit.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiException/UiException/nunit.uiexception.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui-exe/nunit-gui.exe.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_prefix}/lib/nunit
%{__mkdir_p} %{buildroot}%{_datadir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_datadir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE2}`-2.6
%{__install} -m0755 %{SOURCE3} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE3}`-2.6
sed -i -e 's/cli/mono/' %{buildroot}%{_bindir}/*
%{__install} -m0644 src/ConsoleRunner/nunit-console-exe/App.config %{buildroot}%{_prefix}/lib/nunit/nunit-console.exe.config
%{__install} -m0644 src/GuiRunner/nunit-gui-exe/App.config %{buildroot}%{_prefix}/lib/nunit/nunit.exe.config
find %{_builddir}/%{?buildsubdir} -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/nunit/" \;
find %{_builddir}/%{?buildsubdir} -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/nunit/" \;
for i in nunit-console-runner.dll nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.mocks.dll nunit.util.dll ; do
	gacutil -i %{buildroot}%{_prefix}/lib/nunit/$i -package nunit -root %{buildroot}%{_prefix}/lib
	rm -f %{buildroot}%{_prefix}/lib/nunit/$i
done

%files
%defattr(-,root,root)
%_prefix/lib/mono/gac/nunit*
%_prefix/lib/mono/nunit
%_prefix/lib/nunit
%_datadir/pkgconfig/nunit.pc
%_bindir/*
