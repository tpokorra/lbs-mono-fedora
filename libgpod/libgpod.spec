%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# python-gpod should not advertise _gpod.so in its Provides
%define __provides_exclude_from %{python_sitearch}/.*\.so$
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
%ifarch %{mono_arches}
%global with_mono 1
%else
%global with_mono 0
%endif
%if 0%{?rhel}
%global with_mono 0
%endif

Summary: Library to access the contents of an iPod
Name: libgpod
Version: 0.8.3
Release: 9%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtkpod.org/libgpod.html
Source0: http://downloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2

# upstreamable patch: reduce pkgconfig-related overlinking
Patch0:  libgpod-0.8.2-pkgconfig_overlinking.patch
Patch1:  libgpod-fixswig.patch

BuildRequires: automake libtool
BuildRequires: docbook-style-xsl
BuildRequires: glib2-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libimobiledevice-devel
BuildRequires: libplist-devel
BuildRequires: libusbx-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt
%if %{with_mono}
BuildRequires: mono-devel
BuildRequires: gtk-sharp2-devel
%endif
BuildRequires: pygobject2-devel
BuildRequires: python-devel
BuildRequires: python-mutagen
BuildRequires: sg3_utils-devel
BuildRequires: sqlite-devel
BuildRequires: swig
Requires: systemd

%description
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.


%package devel
Summary: Development files for the libgpod library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the files required to develop programs that will use
libgpod.


%package doc
Summary: API documentation for the libgpod library
Group: Documentation
License: GFDL
%if 0%{?fedora}
BuildArch: noarch
%endif
Requires: %{name} = %{version}-%{release}

%description doc
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

This package contains the API documentation.


%package -n python-gpod
Summary: Python module to access iPod content
Group: Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python-mutagen

%description -n python-gpod
A python module to access iPod content.  This module provides bindings to the
libgpod library.


%if %{with_mono}
%package sharp
Summary: C#/.NET library to access iPod content
Group: Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}

%description sharp
C#/.NET library to access iPod content.  Provides bindings to the libgpod
library.


%package sharp-devel
Summary: Development files for libgpod-sharp
Group: Development/Languages
Requires: %{name}-sharp%{?_isa} = %{version}-%{release}

%description sharp-devel
C#/.NET library to access iPod content.  Provides bindings to the libgpod
library.

This package contains the files required to develop programs that will use
libgpod-sharp.
%endif


%prep
%setup -q

%patch0 -p1 -b .pkgconfig_overlinking
%patch1 -p1 -b .swig

#Fix for Mono 4
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac

#autoreconf -f

# remove execute perms on the python examples as they'll be installed in %%doc
chmod -x bindings/python/examples/*.py


%build
%configure --without-hal --enable-udev --with-temp-mount-dir=/run/%{name}
make %{?_smp_mflags} V=1


%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

mkdir -p %{buildroot}/%{_libdir}/libgpod

# remove Makefiles from the python examples dir
rm -rf bindings/python/examples/Makefile*

%if %{with_mono}
# remove execute perms from some libgpod-sharp files
chmod -x %{buildroot}/%{_libdir}/%{name}/*.dll.config
%else
# remove unwanted file
rm -f %{buildroot}/%{_libdir}/pkgconfig/%{name}-sharp.pc
%endif

# Setup tmpfiles.d config
mkdir -p %{buildroot}%{_tmpfilesdir}
echo "D /var/run/%{name} 0644 root root -" > \
    %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

# remove static libs and libtool archives
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README*
%{_bindir}/*
%{_libdir}/*.so.*
%dir /run/%{name}/
%{_tmpfilesdir}/%{name}.conf
/lib/udev/iphone-set-info
/lib/udev/ipod-set-info
/lib/udev/rules.d/*.rules
%dir %{_libdir}/libgpod/

%files devel
%{_includedir}/gpod-1.0/
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_libdir}/*.so


%files doc
%{_datadir}/gtk-doc


%files -n python-gpod
%doc COPYING bindings/python/README bindings/python/examples
%{python_sitearch}/gpod


%if %{with_mono}
%files sharp
%{_libdir}/%{name}/%{name}-sharp*


%files sharp-devel
%{_libdir}/pkgconfig/%{name}-sharp.pc
%endif

%changelog
* Tue Apr 28 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.8.3-9
- Fix for build with mono 4
- Declare mono_arches for EPEL6

* Wed Feb 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-8
- Rebuild (libimobiledevice)
- Use %%license
- Fix use of temp files (rhbz#840183)

* Sun Nov 16 2014 Dan Horák <dan[at]danny.cz> - 0.8.3-7
- switch to mono_arches

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-6
- Rebuild for libimobiledevice 1.1.7

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 0.8.3-3
- Changing ppc64 arch to power64 macro

* Mon May  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-2
- Rebuild for libimobiledevice 1.1.6

* Wed Sep 04 2013 Christophe Fergeau <cfergeau@redhat.com> 0.8.3-1
- Update to libgpod 0.8.3, this is a bugfix release which should fix
  rhbz#921831 rhbz#925750 rhbz#951167

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-9
- Rebuild for new libimobiledevice

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.2-7
- libgpod.pc Requires: libimobiledevice-1.0 ... overlinking (#818594)
- tighten subpkg deps (via %%_isa)
- omit -devel deps that (should) get autodetected already

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Bastien Nocera <bnocera@redhat.com> 0.8.2-5
- Remove bogus gtk2-devel dep in devel sub-package

* Wed Apr 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8.2-4
- Rebuild for new libimobiledevice and usbmuxd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.8.2-2
- Rebuild to break bogus libpng dep

* Wed Jul 27 2011 Christophe Fergeau <cfergeau@redhat.com>
- Remove duplicated call to autoreconf
- Small BuildRequires cleanups

* Mon Jul 25 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2
- Drop upstreamed patches
- Prevent python-gpod from advertising _gpod.so in its Provides

* Mon Jul 18 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-12
- libgpod-0.8.0-10.fc16 grew a mono-core dependency (#722976)

* Mon Jul 18 2011 Dan Horák <dan@danny.cz> - 0.8.0-11
- rebuilt for sg3_utils 1.31

* Thu Jul 14 2011 Bastien Nocera <bnocera@redhat.com> 0.8.0-10
- Add hashDB support

* Wed May 25 2011 Todd Zullinger <tmz@pobox.com> - 0.8.0-9
- Fix tmpfiles.d user/group for /var/run/libgpod (#707787)

* Mon May 23 2011 Todd Zullinger <tmz@pobox.com> - 0.8.0-8
- Support tmpfiles.d for Fedora >= 15 (#707066)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Dan Horák <dan[at]danny.cz> - 0.8.0-6
- conditionalize mono support

* Sat Jan 08 2011 Christian Krause <chkr@fedoraproject.org> - 0.8.0-5
- Change patch to fix 32 bit issues in the mono bindings
  (Itdb_Track data structure contained wrong values on x86 systems)

* Sun Dec 26 2010 Bastien Nocera <bnocera@redhat.com> 0.8.0-4
- Rebuild for new libimobiledevice

* Thu Oct 28 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 0.8.0-3
- Rebuild against new gtk-sharp2 and mono-2.8

* Wed Oct 20 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.8.0-2
- Add patch to fix 32 bit issues in the mono bindings

* Tue Oct 12 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.8.0-1
- Update to 0.8.0

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.7.95-1
- Update to 0.7.95
- Drop upstreamed patches

* Sat Sep 04 2010 Todd Zullinger <tmz@pobox.com> - 0.7.94-1
- Update to 0.7.94
- Add mono subpackage (#630181)

* Mon Aug 23 2010 Todd Zullinger <tmz@pobox.com> - 0.7.93-4
- Own %%{_datadir}/gtk-doc rather than require gtk-doc (#604388)

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.93-3
- persuade configure to work with swig 2.0.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.93-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Todd Zullinger <tmz@pobox.com> - 0.7.93-1
- Update to 0.7.93
- Drop upstreamed mount-dir location patch
- Fix temp mount dir configure option typo
- Drop duplicate libimobiledevice-devel BR
- Remove pointless %%{__$command} macros

* Tue Apr 13 2010 Dan Horák <dan@danny.cz> - 0.7.91-3
- rebuilt for sg3_utils 1.29

* Mon Mar 22 2010 Rex Dieter <rdieter@fedoraproject.org> 0.7.91-2
- rebuild (libimobiledevice)

* Thu Mar 04 2010 Bastien Nocera <bnocera@redhat.com> 0.7.91-1
- Update to 0.7.91
- Use udev callout, disable HAL callouts
- Enable iPhone/iPod Touch support

* Tue Feb 09 2010 Todd Zullinger <tmz@pobox.com> - 0.7.90-1
- Update to 0.7.90
- Adjust default hal callout path (#547049)
  (Temporaily use --with-hal-callouts-dir=%%{_libexecdir}/scripts)

* Thu Dec 10 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-6
- Handle partial UTF-16 strings (#542176)

* Mon Oct 19 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-5
- Fix UTF-16 string parsing patch again

* Mon Oct 19 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-4
- Update UTF-16 string parsing patch

* Sat Oct 17 2009 Bastien Nocera <bnocera@redhat.com> 0.7.2-3
- Fix crasher when parsing UTF-16 strings with a BOM (#517642)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 05 2009 Todd Zullinger <tmz@pobox.com> - 0.7.2-1
- Update to 0.7.2
- Make doc subpackage noarch (on Fedora >= 10)
- Drop --with-hal-callouts-dir from configure, the upstream default works now

* Tue Apr 28 2009 Dan Horak <dan[at]danny.cz> - 0.7.0-3
- rebuild for sg3_utils 1.27

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Todd Zullinger <tmz@pobox.com> - 0.7.0-1
- Update to 0.7.0
- BR libxml2-devel

* Wed Jan 14 2009 Todd Zullinger <tmz@pobox.com> - 0.6.0-10
- Fix path to hal callout (this should help setup the SysInfoExtended
  file automagically)
- Use /var/run/hald as mount dir for hal callout
- Require hal
- Require main package for the -doc subpackage

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-9
- Rebuild for Python 2.6

* Thu Oct 02 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-8
- The -devel package should require gtk2-devel as well
- Add gdk-pixbuf-2.0 to the pkg-config file requirements

* Thu Aug 28 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-7
- Ensure patches apply with no fuzz

* Mon Jun 30 2008 Dan Horak <dan[at]danny.cz> - 0.6.0-6
- add patch for sg3_utils 1.26 and rebuild

* Wed May 14 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-5
- Make libgpod-devel require glib2-devel (#446442)

* Tue Feb 12 2008 Todd Zullinger <tmz@pobox.com> - 0.6.0-4
- rebuild for gcc 4.3

* Wed Dec 19 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-3
- BR docbook-style-xsl to ensure the python docs are built correctly

* Wed Dec 19 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-2
- add the NEWS file, which contains some info on getting newer iPods working
- split out API docs into a separate package
- set %%defattr for python-gpod

* Wed Nov 21 2007 Todd Zullinger <tmz@pobox.com> - 0.6.0-1
- update to 0.6.0
- apply a few upstream patches that just missed the release

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 0.5.2-2
- Rebuild for build ID

* Sat Aug 04 2007 Todd Zullinger <tmz@pobox.com> - 0.5.2-1
- update to 0.5.2
- replace %%makeinstall with %%{__make} DESTDIR=%%{buildroot} install
- build python bindings, merging python-gpod package from extras
- make %%setup quiet
- patch to fixup building of the python docs, BR libxslt
- update license tag

* Tue Jan 16 2007 Alexander Larsson <alexl@redhat.com> - 0.4.2-1
- update to 0.4.2
- Change %%description to reflect newer features
- Remove TODO file from %%doc as it's not included anymore
- Explicitly disable the python bindings, they are in the python-gpod package in
  Extras until the Core/Extras merge

* Mon Nov 20 2006 Alexander Larsson <alexl@redhat.com> - 0.4.0-2
- Add ldconfig calls in post/postun

* Mon Nov 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0
- Include docs in the -devel package
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-3.1
- rebuild

* Tue Jun 06 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-3
- Add missing BR of perl-XML-Parser

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 04 2006 John (J5) Palmieri <johnp@redhat.com> 0.3.0-2
- Modified Matthias Saou's SPEC file found on freshrpms.net
- Added to Fedora Core

* Mon Dec 19 2005 Matthias Saou <http://freshrpms.net/> 0.3.0-1
- Initial RPM release.

