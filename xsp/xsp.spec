%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:		xsp
Version:	2.10.2
Release:	9%{?dist}
License:	MIT
URL:		http://www.mono-project.com/Main_Page
Source0:	http://ftp.novell.com/pub/mono/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:	mono-web-devel, mono-data, mono-devel >= 2.10, pkgconfig, autoconf automake mono-data-sqlite mono-nunit-devel
BuildRequires:	mono-data-oracle monodoc-devel
Requires:	mono-core >= 2.10
Summary:	A small web server that hosts ASP.NET
Group:		System Environment/Daemons
# Mono only available on these:
ExclusiveArch: %{mono_arches}
Obsoletes:	mono-4.0-xsp < 2.10

%define debug_package %{nil}

%description

XSP is a standalone web server written in C# that can be used to run ASP.NET
applications as well as a set of pages, controls and web services that you can
use to experience ASP.NET.

%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} pkgconfig
Summary: Development files for xsp

%description devel
Development files for xsp

%package tests
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Summary: xsp test files

%description tests
Files for testing the xsp server

%prep
%setup -q
autoreconf -I build/m4/shamrock -I build/m4/shave
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
sed -i "s#mono/2.0#mono/4.5#g" configure
sed -i "s#Mono 2.0#Mono 4.5#g" configure
sed -i "s#mono/4.0#mono/4.5#g" configure
sed -i "s#Mono 4.0#Mono 4.5#g" configure

%build
%configure --libdir=%{_prefix}/lib
make

%install
make DESTDIR=%{buildroot} install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%files
%defattr(-, root, root,-)
%doc NEWS README COPYING
%{_bindir}/asp*
%{_bindir}/dbsessmgr*
%{_bindir}/mod-mono*
%{_bindir}/xsp*
%{_bindir}/fastcgi-mono-server*
%{_prefix}/lib/xsp
%{_prefix}/lib/mono/gac/Mono.WebServer*/
%{_prefix}/lib/mono/gac/fastcgi-mono-server2
%{_prefix}/lib/mono/gac/mod-mono-server*/
%{_prefix}/lib/mono/gac/xsp*/
%{_prefix}/lib/mono/2.0/*.dll
%{_prefix}/lib/mono/2.0/*.exe
%{_prefix}/lib/monodoc/sources/Mono.WebServer.*
%{_prefix}/lib/monodoc/sources/Mono.FastCGI.*
%{_prefix}/lib/mono/4.0/Mono.WebServer2.dll
%{_prefix}/lib/mono/4.0/fastcgi-mono-server4.exe
%{_prefix}/lib/mono/4.0/mod-mono-server4.exe
%{_prefix}/lib/mono/4.0/xsp4.exe
%{_prefix}/lib/mono/gac/fastcgi-mono-server4
%{_mandir}/man1/asp*
%{_mandir}/man1/dbsessmgr*
%{_mandir}/man1/mod-mono-server*
%{_mandir}/man1/xsp*
%{_mandir}/man1/fastcgi-mono-server*

%files devel
%defattr(-, root, root,-)
%{_libdir}/pkgconfig/xsp*

%files tests
%defattr(-, root, root,-)
%{_prefix}/lib/xsp/2.0
%{_prefix}/lib/xsp/test

%changelog
* Wed Apr 29 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.10.2-9
- Build with mono 4
- Declare mono_arches for EPEL6

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Christian Krause <chkr@fedoraproject.org> - 2.10.2-2
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Wed Apr 27 2011 Christian Krause <chkr@fedoraproject.org> - 2.10.2-1
- Update to 2.10.2

* Wed Mar 30 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-1
- Update to 2.10
- Minor spec file cleanups
- Moved mono-4.0 parts into main package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Dan Horák <dan[at]danny.cz> - 2.8.1-2
- updated the supported arch list

* Tue Dec 07 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8.1-1
- Bump to bugfix 2.8.1 release

* Sat Oct 09 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1
- Bump to 2.8
- Remove 1.0 targets
- Add xsp-4.0 subpackage

* Wed Jul 14 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.5-1
- Bump to 2.6.7 pre-release
- Alter BR to require mono-2.6.7

* Mon Jun 21 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.4-2
- Spec file fixes

* Tue Apr 27 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.4-1
- Bump to 2.6.4 release
- Spec file fixes

* Fri Mar 19 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.3-1
- Bump to 2.6.3 release

* Tue Dec 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-2
- Bump to release version

* Sat Oct 03 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-1
- Bump to 2.6 preview 1

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-1
- Update to 2.4.2 preview
- Enable ppc64

* Mon Apr 13 2009 Jesse Keating <jkeating@redhat.com> - 2.4-8
- Re-enable ppc
- Fix release numbering

* Mon Apr 06 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-7.1
- Remove ppc build

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-7
- Full 2.4 release

* Wed Mar 18 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-6.RC3
- bump to RC3

* Thu Mar 12 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-5.RC2
- bump to RC2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4.RC1
- bump to RC1

* Thu Feb 05 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.pre2.20090502svn124651
- update from svn
- rename to pre2
- fix svn version number for package

* Fri Jan 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-1.20099124svn124360
- update from svn to use 2.4 branch
- altered BRs and Rs to use mono-2.4

* Fri Jan 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-7.RC2.20090901svn122761
- rename to RC2
- update from svn

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-6.RC1.20081224svn122055
- x86_64 libdir fix

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-5.RC1.20081224svn122055
- Added additional BRs

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20081224svn122055
- Bump to RC1 branched svn
- Minor specfile changes

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre3.20081217svn121604
- bump to 2.2 preview 3
- move to svn for bug fixes

* Sat Dec 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2.pre2
- bump to 2.2 preview 2
- use sed instead of patches

* Tue Nov 25 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.pre1
- bump to 2.2 preview 1

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-4
- bump to RC 4

* Mon Sep 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-3
- bump to RC 3

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- bump to 2.0 RC 1

* Sun Aug 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- bump to 2.0 preview 1
- spec file fixes

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9.1-1
- bump

* Thu Feb 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-2
- fix for problem with the test makefile

* Thu Feb 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump

* Thu Dec 20 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1.2
- remove arch ppc64
- add br mono-data-sqlite

* Thu Nov 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1
- bump
- spec file fixes
- added new tests subpackage

* Sun Nov 11 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.5-1
- bump

* Sun Apr 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.4-1
- bump

* Sun Mar 25 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-2
- fix for un-owned directories

* Thu Feb 15 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-1
- bump

* Thu Nov 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-1
- bump

* Sat Oct 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.18-1
- bump

* Thu Aug 31 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-1
- bump to new version
- added patches for architecture independance
- added devel package

* Tue Jul 11 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.16-1
- bump to new version

* Tue Jul 4 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-7
- brought into line with the new packaging regs for mono apps

* Mon Jun 19 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-6
- removed the libdir hack
- removed the overzealous AC_CANONICAL from config.in

* Sun Jun 18 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-5
- Added back the libdir hack

* Thu Jun 15 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-4
- Removed libhack
- Made noarch
- Removed debug package
- Altered configure to keep it happy

* Wed Jun 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-3
- Added BR pkgconfig

* Tue Jun 06 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.15-2
- fixes for (clean) mock builds

* Sun May 14 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.13-4
- minor alteration to the spec file

* Mon May 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.13-3
- Fixes to the spec file
- Added clean

* Mon Apr 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.13-1
- Initial import for FE
- Heavily amended spec file (based on the Novell original)

