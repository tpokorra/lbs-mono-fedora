%global debug_package %{nil}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
%define zipversion 2.5.10.11092
Name:           nunit25
Version:        2.5.10
Release:        1%{?dist}
Summary:        Unit test framework for CLI
License:        MIT
Group:          Development/Libraries
Url:            http://www.nunit.org/
Source0:        http://launchpad.net/nunitv2/2.5/2.5.10/+download/NUnit-%{zipversion}-src.zip
Source1:        nunit25.pc
Source2:        nunit-console25.sh
BuildRequires:  mono-devel libgdiplus-devel
ExclusiveArch:  %{mono_arches}

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.
.
NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%package        devel
Summary:        Development files for NUnit
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
 
%description devel
Development files for %{name}.

%prep
%setup -qn NUnit-%{zipversion}

%build

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%{?exp_env}
%{?env_options}
xbuild /property:Configuration=Debug ./src/NUnitCore/core/nunit.core.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitCore/interfaces/nunit.core.interfaces.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitFramework/framework/nunit.framework.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitMocks/mocks/nunit.mocks.csproj
xbuild /property:Configuration=Debug ./src/ClientUtilities/util/nunit.util.dll.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console/nunit-console.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console-exe/nunit-console.exe.csproj
#xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui/nunit-gui.csproj
#xbuild /property:Configuration=Debug ./src/GuiComponents/UiKit/nunit.uikit.dll.csproj
#xbuild /property:Configuration=Debug ./src/GuiException/UiException/nunit.uiexception.dll.csproj
#xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui-exe/nunit-gui.exe.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_prefix}/lib/nunit/2.5/
%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE2}`-2.5
%{__install} -m0644 src/ConsoleRunner/nunit-console-exe/App.config %{buildroot}%{_prefix}/lib/nunit/2.5/nunit-console.exe.config
%{__install} -m0644 src/GuiRunner/nunit-gui-exe/App.config %{buildroot}%{_prefix}/lib/nunit/2.5/nunit.exe.config
find %{_builddir}/%{?buildsubdir} -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/nunit/2.5/" \;
find %{_builddir}/%{?buildsubdir} -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/nunit/2.5/" \;
for i in nunit-console-runner.dll nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.mocks.dll nunit.util.dll ; do
    gacutil -i %{buildroot}%{_prefix}/lib/nunit/2.5/$i -package nunit/2.5 -root %{buildroot}%{_prefix}/lib
    rm -f %{buildroot}%{_prefix}/lib/nunit/2.5/$i
done

%files
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/nunit*
%{_prefix}/lib/mono/nunit/2.5
%{_prefix}/lib/nunit/2.5
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/nunit25.pc

%changelog
* Mon May 04 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.5.10-1
- Inicial package for 2.5 version
