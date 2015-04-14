Name:           libgdiplus
Version:        2.10.9
Release:        3%{?dist}
Summary:        An Open Source implementation of the GDI+ API

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.mono-project.com/Main_Page
Source0:        http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.bz2
# Patch for linking against libpng 1.5 (BZ #843330)
# https://github.com/mono/libgdiplus/commit/506df13e6e1c9915c248305e47f0b67549732566
Patch0:         libgdiplus-2.10.9-libpng15.patch
# Fix build with Freetype 2.5
# https://github.com/mono/libgdiplus/commit/180c02e0f2a2016eba8520b456ca929e9dcf03db
Patch1:         libgdiplus-2.10.9-freetype25.patch
# drop -Wno-format so the default -Werror=format-security works
Patch2:         libgdiplus-2.10.9-format.patch
# https://github.com/mono/libgdiplus/commit/1fa831c7440f1985d2b730211bbf8a059c10a63b
Patch3:         libgdiplus-2.10.9-tests.patch
BuildRequires:  freetype-devel glib2-devel libjpeg-devel libtiff-devel
BuildRequires:  libpng-devel fontconfig-devel
BuildRequires:  cairo-devel giflib-devel libexif-devel
BuildRequires:  zlib-devel

%description
An Open Source implementation of the GDI+ API, it is part of the Mono 
Project

%package devel
Summary: Development files for libgdiplus
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for libgdiplus

%prep
%setup -q 
%patch0 -p1 -b .libpng15
%patch1 -p1 -b .freetype25
%patch2 -p1 -b .format
%patch3 -p1 -b .tests

%build
%configure --disable-static 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
cd %{buildroot}/%{_libdir}; ln -s libgdiplus.so.0 libgdiplus.so; cd -
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS README TODO AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Tue Apr 14 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- create symbolic link /usr/lib(64)/libgdiplus.so

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Dan Horák <dan[at]danny.cz> - 2.10.9-1
- updated to 2.10.9
- fix FTBFS (#1089734, #1037161)

* Mon Nov 25 2013 Björn Esser <bjoern.esser@gmail.com> - 2.10-11
- rebuilt for giflib-5.0.5 on rawhide
- removed BuildRequires: libungif-devel, since the package passed away
- fixed bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.10-8
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.10-7
- rebuild against new libjpeg

* Fri Jul 27 2012 Christian Krause <chkr@fedoraproject.org> - 2.10-6
- Add patch to support linking against libpng 1.5 (BZ #843330)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.10-3
- Rebuild for new libpng

* Sun Mar 27 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-2
- Update to official 2.10 release
- Move sources into lookaside cache

* Thu Feb 03 2011  Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.10-1
- Bump to 2.10 RC2

* Tue Nov 23 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8.1-1
- Bump to bug fix release

* Thu Oct 14 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-2
- Correct URL
- Revert merge-review cleanup (#226009)

* Thu Oct 07 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1.1
- Bump to full release

* Wed Sep 15 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1
- Bump to review 3 of the 2.8 release
- Remove patch for CVE-2010-1526

* Tue Aug 24 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.7-3
- Add upstream patch for CVE-2010-1526

* Sun Jul 25 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.7-2
- Cleanup spec file

* Sat Jul 10 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.7-1
- Update to 2.6.7 release candidate 1
- Add BR giflib-devel and libexif-devel

* Sun Jun 20 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.4-2
- Cleanup spec file
- Remove removal of -Werror - not applicable anymore

* Tue Apr 27 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.4-1
- Update to the 2.6.4 release
- URL and source locations fixed in spec file

* Wed Dec 16 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-2
- Update to 2.6

* Wed Sep 30 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-1
- Update to 2.6 preview 1

* Mon Jun 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4,2-2
- bump to RC1

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-1
- bump to 2.4.2 preview

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-5
- 2.4 release

* Tue Mar 17 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4.RC3
- Bump to RC3

* Tue Mar 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.RC2
- Bump to RC2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-2.RC1
- Bump to RC1 release
- Fixed source URL
- Returned from svn to official releases

* Mon Feb 02 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-1.pre1.20090202svn124838
- Update to svn
- retagged as 2.4 pre-release 1

* Sat Jan 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20090104svn122354.1
- Rebuild

* Sun Jan 04 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20090104svn122354
- Update to svn

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20081224svn122059
- Bump to RC1 branched svn

* Wed Dec 10 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre2.20081012svn118228
- Update to svn

* Fri Dec 05 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2.pre2
- Update to 2.2 preview 2

* Tue Nov 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.pre1
- Update to 2.2 preview 1

* Sat Oct 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-5
- fix the long standing symlink problem

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-4
- Bump to RC4

* Mon Sep 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-3
- Bump to RC3

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- Bump to RC1

* Sat Aug 02 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- Bump to preview 1
- Alter licence

* Thu Mar 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-4
- bump to preview 4

* Mon Feb 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump to preview 1

* Tue Dec 11 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-2
- bump to preview 4

* Thu Nov 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1
- bump to latest preview version

* Fri Oct 05 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.5-1
- bump to 1.2.5
- disabled static build
- added fontconfig-devel requirement

* Sat Apr 21 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.4-1
- bump

* Fri Jan 26 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-1
- bump

* Sat Dec 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.2-1
- bump

* Sat Nov 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-1
- bump

* Fri Nov 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2-1
- bump
- added post and postun
- put the .so file in the devel package

* Sat Sep 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-1
- bump
- added devel package
- swapped the perl script into prep (where it should be!)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jul  7 2006 Alexander Larsson <alexl@redhat.com> - 1.1.16-1
- update to 1.1.16

* Wed Jun  7 2006 Alexander Larsson <alexl@redhat.com> - 1.1.15-1
- Update to 1.1.15

* Wed Apr 26 2006 Alexander Larsson <alexl@redhat.com> - 1.1.13.6-2
- Upgrade to 1.1.13.6

* Fri Mar  3 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.4-1
- Update to 1.1.13.4

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.2-2
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.13.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.2-1
- Update to 1.1.13.2

* Fri Jan 13 2006 Alexander Larsson <alexl@redhat.com> - 1.1.13-1
- update to 1.1.13

* Wed Jan 11 2006 Alexander Larsson <alexl@redhat.com> 1.1.11-2
- Don't package debug info

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 1.1.11-1
- Update to 1.1.11

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 1.1.10-3
- Rebuild, fix gcc4 issue

* Thu Nov 17 2005 Alexander Larsson <alexl@redhat.com> 1.1.10-2
- Build on s390* also

* Thu Nov 17 2005 Alexander Larsson <alexl@redhat.com> - 1.1.10-1
- Initial version

