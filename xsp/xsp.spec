%if 0%{?el6}
# see https://fedorahosted.org/fpc/ticket/395, it was added to el7
%global mono_arches %{ix86} x86_64 sparc sparcv9 ia64 %{arm} alpha s390x ppc ppc64 ppc64le
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

Name:			xsp
Version:	4.2
Release:	1%{?dist}
License:	MIT
URL:			http://www.mono-project.com/Main_Page
Summary:	A small web server that hosts ASP.NET
Group:		System Environment/Daemons

Source0:	http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	mono-web-devel, mono-data, mono-devel, mono-data-sqlite, nunit-devel
BuildRequires:	mono-data-oracle monodoc-devel
BuildRequires:	autoconf automake libtool
Requires:	mono-core
# Mono only available on these:
ExclusiveArch: %mono_arches

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

sed -i "s#dmcs#mcs#g" configure

%build
%configure --libdir=%{_prefix}/lib
make

%install
make DESTDIR=%{buildroot} install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

%files
%doc NEWS README COPYING
%{_bindir}/asp*
%{_bindir}/dbsessmgr*
%{_bindir}/mod-mono*
%{_bindir}/mono-fpm
%{_bindir}/shim
%{_bindir}/xsp*
%{_bindir}/fastcgi-mono-server*
%{_prefix}/lib/xsp
%{_monogacdir}/Mono.WebServer*/
%{_monogacdir}/fastcgi-mono-server4
%{_monogacdir}/mod-mono-server*/
%{_monogacdir}/mono-fpm
%{_monogacdir}/xsp*/
%{_prefix}/lib/monodoc/sources/Mono.WebServer.*
%{_prefix}/lib/monodoc/sources/Mono.FastCGI.*
%{_monodir}/4.?/Mono.WebServer2.dll
%{_monodir}/4.?/fastcgi-mono-server4.exe
%{_monodir}/4.?/mod-mono-server4.exe
%{_monodir}/4.?/mono-fpm.exe
%{_monodir}/4.?/xsp4.exe
%{_prefix}/lib/libfpm_helper.so.0*
%{_mandir}/man1/asp*
%{_mandir}/man1/dbsessmgr*
%{_mandir}/man1/mod-mono-server*
%{_mandir}/man1/xsp*
%{_mandir}/man1/fastcgi-mono-server*

%files devel
%{_libdir}/pkgconfig/xsp*
%{_prefix}/lib/libfpm_helper.so

%files tests
%{_prefix}/lib/xsp/test

%changelog
* Fri Jan 29 2016 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 4.2-1
- Updated to 4.2
- Use mono macros
- Use mcs instead dmcs

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.8-1
- Update to 3.8
- Rebuild (mono4)

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
