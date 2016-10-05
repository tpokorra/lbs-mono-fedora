%global debug_package %{nil}

%if 0%{?el6}
# see https://fedorahosted.org/fpc/ticket/395, it was added to el7
%global mono_arches %{ix86} x86_64 sparc sparcv9 ia64 %{arm} alpha s390x ppc ppc64 ppc64le
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

Name:           nunit
Version:        3.5
Release:        1%{?dist}
Summary:        Unit test framework for CLI
%if 0%{?el6}
License:        MIT
%else
License:        MIT with advertising
%endif
Group:          Development/Libraries
Url:            http://www.nunit.org/
Source0:        https://github.com/nunit/nunit/archive/%{version}.tar.gz
Source1:        nunit.pc
Source2:        nunitlite-runner.sh
BuildRequires:  mono-devel
ExclusiveArch:  %{mono_arches}
Provides:       mono-nunit = 4.0.2-5
Obsoletes:      mono-nunit < 4.0.2-6
Obsoletes:      nunit-runner <= 2.6.4-10

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%package        devel
Summary:        Development files for NUnit
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Provides:       mono-nunit-devel = 4.0.2-5
Obsoletes:      mono-nunit-devel < 4.0.2-6

%description devel
Development files for %{name}.

%prep
%setup -qn nunit-%{version}

%build

# Remove prebuilt binaries
find . -name "*.dll" -print -delete

%{?exp_env}
%{?env_options}

xbuild /property:Configuration=Release src/NUnitFramework/framework/nunit.framework-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite/nunitlite-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite-runner/nunitlite-runner-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/mock-assembly/mock-assembly-4.5.csproj

xbuild /property:Configuration=Release src/NUnitFramework/slow-tests/slow-nunit-tests-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/testdata/nunit.testdata-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/tests/nunit.framework.tests-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite.tests/nunitlite.tests-4.5.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_monodir}/nunit
%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__mkdir_p} %{buildroot}%{_datadir}/icons/NUnit
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/nunitlite-runner
%{__install} -m0644 src/NUnitFramework/nunitlite-runner/App.config %{buildroot}%{_monodir}/nunit/nunitlite-runner.exe.config
find %{_builddir}/%{?buildsubdir}/bin -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
find %{_builddir}/%{?buildsubdir}/bin -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
for i in nunit.framework.dll nunit.framework.tests.dll nunitlite.dll nunit.testdata.dll; do
    gacutil -i %{buildroot}%{_monodir}/nunit/$i -package nunit -root %{buildroot}%{_monodir}/../
done

%files
%if ! 0%{?el6}
%license LICENSE.txt
%endif
%{_bindir}/nunitlite-runner
%{_monogacdir}/nunit*
%{_monodir}/nunit/*

%files devel
%{_libdir}/pkgconfig/nunit.pc

%changelog
* Wed Oct 05 2016 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.5-1
- Update to 3.5
- Move from nunit3-console to nunitlite-runner

* Fri Sep 02 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.4.1-2
- fix obsoletes nunit-runner

* Wed Jul 20 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.4.1-1
- upgrade to 3.4.1. nunit-gui will be in separate package (#1360389)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.4-11
- Replace nunit-runner with nunit-gui with only desktop frontend

* Sun Nov 01 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.4-10
- Split runner tool in subpackage

* Tue Aug 04 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-9
- obsoleting mono-nunit and mono-nunit-devel (bug 1247825)

* Fri Jul 17 2015 Dan Horák <dan[at]danny.cz> - 2.6.4-8
- set ExclusiveArch

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-7
- require desktop-file-utils for building and make sure we own the icons/NUnit directory

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-5
- fix Requires for devel package, and fixing other issues

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-2
- include a desktop file and install the icon

* Mon Jun 22 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-1
- upgrade to 2.6.4
- fix the license
- fix some rpmlint warnings and errors

* Thu Jun 04 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-6
- do not replace mono-nunit. fix some rpmlint warnings and errors

* Wed Jun 03 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-5
- Use mono macros
- Require isa in devel subpackage
- Use global insted define

* Tue May 19 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-4
- this package replaces mono-nunit

* Mon May 04 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.3-3
- Move to 2.6 folder for compat with other versions
- Use real source file

* Tue Apr 21 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.3-2
- Split nunit.pc into devel package
- Use upstream zip source
- Add ExclusiveArch

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-0
- copy from Xamarin NUnit spec
