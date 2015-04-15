%define debug_package %{nil}

Name:		mono-addins
Version:	0.6.2
Release:	12%{?dist}
Summary:	Addins for mono
Group:		Development/Languages
License:	MIT
URL:		http://www.mono-project.com/Main_Page
Source0:	http://origin-download.mono-project.com/sources/mono-addins/mono-addins-%{version}.tar.bz2
Patch0:		mono-addins-0.6.2-libdir.patch
Patch1:		automake_1.11.2_pkglibdir_workaround.patch

BuildRequires:	mono-devel >= 2.4, gtk-sharp2-devel, autoconf, automake
BuildRequires:	pkgconfig
# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc %{power64} ia64 %{arm} sparcv9 alpha s390x
Provides: mono(Mono.Addins) = 0.2.0.0
Provides: mono(Mono.Addins) = 0.3.0.0
Provides: mono(Mono.Addins) = 0.4.0.0
Provides: mono(Mono.Addins) = 0.5.0.0
Provides: mono(Mono.Addins.Gui) = 0.2.0.0
Provides: mono(Mono.Addins.Gui) = 0.3.0.0
Provides: mono(Mono.Addins.Gui) = 0.4.0.0
Provides: mono(Mono.Addins.Gui) = 0.5.0.0
Provides: mono(Mono.Addins.Setup) = 0.2.0.0
Provides: mono(Mono.Addins.Setup) = 0.3.0.0
Provides: mono(Mono.Addins.Setup) = 0.4.0.0
Provides: mono(Mono.Addins.Setup) = 0.5.0.0
Provides: mono(Mono.Addins.CecilReflector) = 0.2.0.0
Provides: mono(Mono.Addins.CecilReflector) = 0.3.0.0
Provides: mono(Mono.Addins.CecilReflector) = 0.4.0.0
Provides: mono(Mono.Addins.CecilReflector) = 0.5.0.0

%description
Mono.Addins is a generic framework for creating extensible applications,
and for creating libraries which extend those applications.

%package devel
Summary: Development files for mono-addins
Group: Development/Languages
Requires: %{name} = %{version}-%{release} pkgconfig
Provides: mono(Mono.Addins.MSBuild) = 0.2.0.0
Provides: mono(Mono.Addins.MSBuild) = 0.3.0.0
Provides: mono(Mono.Addins.MSBuild) = 0.4.0.0
Provides: mono(Mono.Addins.MSBuild) = 0.5.0.0

%description devel
Mono.Addins is a generic framework for creating extensible applications,
and for creating libraries which extend those applications.
This package contains MSBuild tasks file and target, which allows
using add-in references directly in a build file (still experimental).

%prep
%setup -q 
%patch0 -p1 -b .libdir
%patch1 -p1 -b .pkglibdir

%build
sed -i "s#AC_PATH_PROG(MCS, gmcs, no)#AC_PATH_PROG(MCS, mcs, no)#g" configure.ac
autoreconf -f -i
%configure --enable-gui
find . -name "Makefile*" -print -exec sed -i 's#ASSEMBLY_COMPILER_COMMAND = gmcs#ASSEMBLY_COMPILER_COMMAND = mcs#g; s#-r:Microsoft.Build.Utilities #-r:Microsoft.Build.Utilities.v4.0 #g' {} \;
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files 
%defattr(-,root,root,-)
%doc README NEWS AUTHORS ChangeLog
%{_bindir}/mautil
%dir %{_prefix}/lib/mono/mono-addins
%{_prefix}/lib/mono/mono-addins/Mono.Addins.CecilReflector.dll
%{_prefix}/lib/mono/mono-addins/Mono.Addins.Gui.dll
%{_prefix}/lib/mono/mono-addins/Mono.Addins.Setup.dll
%{_prefix}/lib/mono/mono-addins/Mono.Addins.dll
%{_prefix}/lib/mono/mono-addins/mautil.exe
%{_prefix}/lib/mono/gac/Mono.Addins.Gui
%{_prefix}/lib/mono/gac/Mono.Addins.Setup
%{_prefix}/lib/mono/gac/Mono.Addins
%{_prefix}/lib/mono/gac/Mono.Addins.CecilReflector
%{_prefix}/lib/mono/gac/policy.0.2.Mono.Addins.Gui
%{_prefix}/lib/mono/gac/policy.0.2.Mono.Addins.Setup
%{_prefix}/lib/mono/gac/policy.0.2.Mono.Addins
%{_prefix}/lib/mono/gac/policy.0.2.Mono.Addins.CecilReflector
%{_prefix}/lib/mono/gac/policy.0.3.Mono.Addins.Gui
%{_prefix}/lib/mono/gac/policy.0.3.Mono.Addins.Setup
%{_prefix}/lib/mono/gac/policy.0.3.Mono.Addins
%{_prefix}/lib/mono/gac/policy.0.3.Mono.Addins.CecilReflector
%{_prefix}/lib/mono/gac/policy.0.4.Mono.Addins.CecilReflector
%{_prefix}/lib/mono/gac/policy.0.4.Mono.Addins.Gui
%{_prefix}/lib/mono/gac/policy.0.4.Mono.Addins.Setup
%{_prefix}/lib/mono/gac/policy.0.4.Mono.Addins
%{_prefix}/lib/mono/gac/policy.0.5.Mono.Addins.CecilReflector
%{_prefix}/lib/mono/gac/policy.0.5.Mono.Addins.Gui
%{_prefix}/lib/mono/gac/policy.0.5.Mono.Addins.Setup
%{_prefix}/lib/mono/gac/policy.0.5.Mono.Addins
%{_mandir}/man1/mautil.1.gz

%files devel
%defattr (-,root,root,-)
%{_prefix}/lib/mono/gac/policy.0.2.Mono.Addins.MSBuild
%{_prefix}/lib/mono/gac/policy.0.3.Mono.Addins.MSBuild
%{_prefix}/lib/mono/gac/policy.0.4.Mono.Addins.MSBuild
%{_prefix}/lib/mono/gac/policy.0.5.Mono.Addins.MSBuild
%{_prefix}/lib/mono/mono-addins/Mono.Addins.MSBuild.dll
%{_prefix}/lib/mono/gac/Mono.Addins.MSBuild
%{_prefix}/lib/mono/xbuild
%{_libdir}/pkgconfig/mono-addins*

%changelog
* Wed Apr 15 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 0.6.2-12
- build for Mono 4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 0.6.2-9
- Changing ppc64 arch to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.2-5
- Add patch to fix issues with pkglibdir

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 0.6.2-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sun Sep 11 2011 Christian Krause <chkr@fedoraproject.org> - 0.6.2-2
- Fix paths for x86_64

* Sun Sep 04 2011 Christian Krause <chkr@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 release
- Manually add some Provides to reflect the compatible API versions
  as defined by the policy files

* Mon Mar 28 2011 Christian Krause <chkr@fedoraproject.org> - 0.5-5
- Use official 0.5 release linked from http://ftp.novell.com/pub/mono/archive/2.6.7/sources/
- Move MSBuild parts into -devel package so that the main package does not
  depend on mono-devel (BZ 671917)
- Minor spec file cleanup

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Dan Horák <dan[at]danny.cz> - 0.5-3
- updated the supported arch list

* Fri Oct 29 2010 Christian Krause <chkr@fedoraproject.org> - 0.5-2
- Rebuild again to create correct requires/provides capabilities

* Sat Oct 09 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.5-1.1
- Rebuild

* Mon May 31 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.5-1
- Update to 5.0 release
- Alter URL

* Fri Apr 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-5.20091702svn127062.1
- Exclude ppc

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5.20091702svn127062
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-4.20091702svn127062
- update from svn

* Tue Feb 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-4.20091002svn126354
- large update from svn
- now uses a tarball
- add mautil manual

* Thu Jan 29 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-4.20081215svn105642
- update to 2.4 svn build
- remove mautil manuals

* Thu Dec 11 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-3
- Rebuild
- Correct licence to MIT
- Replaced patch with sed

* Tue Nov 25 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-2
- Fix archs

* Fri Nov 07 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.4-1
- new release
- removed scan fix patch

* Mon Jul 14 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.3.1-2.2
- rebuild

* Thu May 01 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.3.1-2.1
- rebuild

* Tue Apr 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.3.1-2
- added BR pkgconfig

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.3.1-1
- bump (should fix the monodevelop problems)

* Tue Apr 15 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.3-5
- Add patch from Debian to make sure addins don't disappear in f-spot (#442343)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3-4
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 <paul@all-the-johnsons.co.uk> 0.3-3
- removed debug package
- spec file fixes
- additional BRs for autoreconf
- excludearch ppc64 added

* Thu Jan 03 2008 <paul@all-the-johnsons.co.uk> 0.3-2
- enabled gui
- spec file fixes

* Wed Dec 19 2007 <paul@all-the-johnsons.co.uk> 0.3-1
- Initial import for FE
