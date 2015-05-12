%define debug_package %{nil}

%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

Name:		mono-basic
Version:	4.0.1
Release:	1%{?dist}
Summary:	VisualBasic.NET support for mono
Group:		Development/Languages
License:	LGPLv2+
URL:		http://www.mono-project.com/Main_Page
Source0:	http://origin-download.mono-project.com/sources/mono-basic/%{name}-%{version}.tar.bz2

# Yeah, so this guy isn't self-hosting.
%ifarch !ppc
BuildRequires:	mono-basic pkgconfig
%else
BuildRequires:	pkgconfig
%endif
BuildRequires:	mono-devel >= 3.0
BuildRequires:	mono-winforms mono-data mono-web

ExclusiveArch: %{mono_arches}

%description
This package contains the Visual Basic .NET compiler and language
runtime. This allows you to compile and run VB.NET application and
assemblies.

%package devel
Summary: Development files for mono-basic
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} pkgconfig
 
%description devel
Development files for mono-basic

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --libdir=%{_prefix}/lib
make

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_libdir}/pkgconfig

cat <<EOF >%{buildroot}/%{_libdir}/pkgconfig/mono-basic.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_prefix}/lib

Name: mono-basic
Description: mono-basic - VB for mono
Version: %{version}
Libs: -r:%{_prefix}/lib/mono/4.5/Microsoft.VisualBasic.dll
EOF

%files 
%defattr(-,root,root,-)
%{_bindir}/vbnc*
%{_monodir}/4.5/vbnc*
%{_monodir}/4.5/Microsoft.VisualBasic.dll
%{_monogacdir}/Microsoft.VisualBasic
%{_monodir}/4.5/Mono.Cecil.VB*dll
%{_monogacdir}/Mono.Cecil.VB.Mdb
%{_monogacdir}/Mono.Cecil.VB.Pdb
%{_monogacdir}/Mono.Cecil.VB
%{_mandir}/man1/vbnc.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/mono-basic.pc

%changelog
* Tue May 12 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Tue May 28 2013 Dan Horák <dan[at]danny.cz> - 2.10-7
- update ExclusiveArch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Thu Jun 02 2011 Paul Whalen <paul.whalen@senecac.on.ca> - 2.10-2
- Added arm macro to ExclusiveArch

* Sun Mar 27 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-1
- Update to 2.10 release
- Update mono-basic.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Christian Krause <chkr@fedoraproject.org> - 2.8-2
- Rebuild again to create correct requires/provides capabilities

* Sun Oct 03 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1
- Bump to 2.8 preview 8

* Sun Jun 20 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.2-1
- Bump to 2.6.2 release
- Cleanup spec file

* Wed Dec 16 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-2
- Bump to 2.6 release

* Wed Sep 30 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-1
- Bump to 2.6 preview 1

* Mon Jun 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-2
- Bump to 2.4.2 RC1
- Drop R mono-winforms

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-1
- Update to 2.4.2 preview
- Enable ppc64 build

* Mon Apr 13 2009 Jesse Keating <jkeating@redhat.com> - 2.4-5
- Re-enable ppc
- Fix release numbering

* Mon Apr 06 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4.1
- Remove ppc

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4
- Full 2.4 release

* Wed Mar 18 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.RC3
- bump to RC3

* Tue Mar 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-2.RC2
- bump to RC2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-1.RC1
- bump to RC1
- fix to build against mono-2.4

* Wed Dec 31 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-9.RC1.20081231svn122295
- Hack to build under ppc. Will revert next build

* Wed Dec 31 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-8.RC1.200812131svn122295
- Large update from svn
- Retag for RC1 release

* Fri Dec 19 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-7.pre3.20081217svn121665
- Reenable ppc

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-6.pre3.20081217svn121665
- Removed ppc build (problems upstream with mono-2.2)

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-5.pre3.20081217svn121665
- Another fix for x86_64

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.pre3.20081217svn121665
- Fix for x86_64

* Wed Dec 17 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre3.20081217svn121665
- Update

* Tue Dec 16 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre3.20081216svn121582
- Bump to preview 3 svn (as per Novell release schedule)

* Mon Dec 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre2.20081215svn121506
- Update 2.2 preview 2 to svn build
- Modify patch
- Added in manual file

* Fri Dec 05 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2.pre2
- Update to 2.2 preview 2

* Tue Nov 25 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.1.pre1
- rebuild

* Thu Nov 20 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.pre1
- bump to 2.2 preview 1

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-4
- bump to RC4

* Mon Sep 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-3
- bump to RC3
- alter excludearch to exclusivearch
- alter version number in pc file

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- bump to 2.0 RC 1

* Sun Aug 10 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- bump to 2.0 preview 1

* Tue Apr 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-4
- spec file changelog fix
- added BR pkgconfig

* Mon Apr 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-3
- added devel subpackage
- removed debug package

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.9-2
- get rid of bootstrap binary bits

* Thu Feb 21 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump

* Tue Jan 08 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-4
- add excludearch ppc64
- alter license to LGPLv2+

* Thu Jan 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-3
- minor spec file fixes

* Thu Dec 20 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-2
- bump
- fix for vbnc

* Sun Apr 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.4-1
- bump

* Sat Feb 17 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-1
- Initial import for FE
