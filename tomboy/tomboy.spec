Name:           tomboy
Version:        1.15.4
Release:        7%{?dist}
Summary:        Note-taking application
Group:          User Interface/Desktops
License:        LGPLv2+ and GPLv2+ and MIT
# Tomboy itself is LGPLv2+
# libtomboy contains GPL+ code
# Mono.Addins is MIT
URL:            http://projects.gnome.org/tomboy/
Source0:        http://download.gnome.org/sources/%{name}/1.15/%{name}-%{version}.tar.xz

BuildRequires:  gtk2-devel
BuildRequires:  atk-devel
BuildRequires:  gtkspell-devel
BuildRequires:  gtk-sharp2-devel
BuildRequires:  dbus-sharp-devel
BuildRequires:  dbus-sharp-glib-devel

BuildRequires:  GConf2
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gnome-doc-utils
BuildRequires:  intltool
BuildRequires:  libX11-devel

Requires: gtkspell
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc %{power64} ia64 %{arm} sparcv9 alpha s390x


%description
Tomboy is a desktop note-taking application which is simple and easy to use.
It lets you organise your notes intelligently by allowing you to easily link
ideas together with Wiki style interconnects.


%package devel
Summary: Support for developing addings for tomboy
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}


%description devel
Tomboy is a desktop note-taking application. This package allows you
to develop addins that add new functionality to tomboy.


%prep
%setup -q

# Convert to utf-8
for file in ChangeLog ; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done


%build
%configure --disable-scrollkeeper --disable-static
mkdir bin
make %{?_smp_mflags}


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=%{buildroot} INSTALL="install -p"
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find %{buildroot} -name '*.la' -delete

chmod a+x %{buildroot}%{_libdir}/%{name}/*.exe
chmod a+x %{buildroot}%{_libdir}/%{name}/addins/*.dll

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.gnome.org/show_bug.cgi?id=736869
SentUpstream: 2014-09-18
-->
<application>
  <id type="desktop">tomboy.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Tomboy is a desktop note-taking application for GNU/Linux, Unix, Windows, and
      Mac OS X.
      Simple and easy to use, but with potential to help you organize the ideas and
      information you deal with every day.
    </p>
    <p>
      Have you ever felt the frustration at not being able to locate a website you
      wanted to check out, or find an email you found interesting, or remember an idea
      about the direction of the political landscape in post-industrial Australia?
      Or are you one of those desperate souls with home-made, buggy, or not-quite-perfect
      notes systems?
      Time for Tomboy.
    </p>
    <p>
      We bet you'll be surprised at how well a little application can make life less
      cluttered and run more smoothly.
    </p>
  </description>
  <url type="homepage">https://projects.gnome.org/tomboy/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/tomboy/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/tomboy.desktop

%find_lang %name --with-gnome

for i in %{buildroot}%{_datadir}/mime/*; do
  if [ ! "${i##*/}" = "packages" ]; then
    rm -rf $i
  fi
done


%post
%gconf_schema_upgrade tomboy
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :


%pre
%gconf_schema_prepare tomboy


%preun
%gconf_schema_remove tomboy


%postun
update-mime-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  update-mime-database %{_datadir}/mime &> /dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_libdir}/%{name}
%{_bindir}/tomboy
%{_libdir}/tomboy/*
%{_datadir}/dbus-1/services/org.gnome.Tomboy.service
%{_mandir}/man1/tomboy.1.gz
%{_datadir}/tomboy
%{_datadir}/icons/hicolor/*/apps/tomboy.*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/mime/packages/tomboy.xml
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/tomboy.desktop
%{_sysconfdir}/gconf/schemas/tomboy.schemas


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Apr 17 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 1.15.4-7
- Rebuild for Mono 4

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.15.4-6
- Add an AppData file for the software center

* Sat Sep 27 2014 Rex Dieter <rdieter@fedoraproject.org> 1.15.4-5
- update/optimize mimeinfo scriplets

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Brent Baude <baude@us.ibm.com> - 1.15.4-2
- Changing ppc64 arch to power64 macro 

* Sat Jan 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.15.4-1
- Update to 1.15.4.
- Fix rpmlint warning about bogus date in the changelog.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun  8 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.15.2-1
- Update to 1.15.2.

* Mon May  6 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.15.1-1
- Update to 1.15.1.

* Tue Apr  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.14.0-1
- Update to 1.14.0.

* Fri Mar 22 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.6-1
- Update to 1.13.6.

* Wed Feb 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.5-1
- Update to 1.13.5.

* Wed Jan 30 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.4-1
- Update to 1.13.4.

* Fri Dec 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.3-1
- Update to 1.13.3.

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.2-1
- Update to 1.13.2.
- Fix changelog.

* Fri Oct 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.13.1-1
- Update to 1.13.1.

* Thu Oct 18 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.12.1-1
- Update to 1.12.1.

* Wed Sep 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.12.0-1
- Update to 1.12.0.

* Sun Sep 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.7-1
- Update to 1.11.7.

* Mon Aug  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.5-1
- Update to 1.11.5.

* Wed Jul 18 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.4-1
- Update to 1.11.4.

* Tue Jun 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.3-1
- Update to 1.11.3.

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.2-1
- Update to 1.11.2.

* Mon May  7 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.1-1
- Update to 1.11.1.

* Wed Apr 18 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.1-1
- Update to 1.10.1.

* Tue Mar 27 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.0-1
- Update to 1.10.0.

* Fri Mar 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.10-1
- Update to 1.9.10.

* Tue Mar 13 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.9-1
- Update to 1.9.9.

* Thu Mar  1 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.8-2
- Use dbus-sharp and dbus-sharp-glib.

* Sat Feb 25 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.8-1
- Update to 1.9.8.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.6-1
- Update to 1.9.6.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.4-1
- Update to 1.9.4.

* Sat Dec 10 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.3-1
- Update to 1.9.3.

* Fri Nov 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.2-1
- Update to 1.9.2.

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Tue Sep 13 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.6-1
- Update to 1.7.6.
- Use xz-compressed source.

* Sat Jul  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.1-1
- Update to 1.7.1.
- Drop dependency on gconf-sharp-peditors.

* Thu Jun 16 2011 Dan Horák <dan[at]danny.cz> - 1.7.0-2
- updated the supported arch list

* Wed Jun 15 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-1
- Update to 1.7.0.
- Add BR on libX11-devel.

* Thu Jun  2 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.0-1
- Update to 1.6.0, also fixes CVE-2010-4005.
- Simply create the missing dir instead of patching Makefile.am.
- Include the .desktop file (bz 672406).
- Use pkgconfig(...)-style BRs.
- Add missing BR on GConf2.
- Re-enable the panel applet for F14 (bz 637416).
- Minor cosmetics.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.5.2-2
- Rebuild against new mono and gmime-sharp

* Mon Oct 25 2010 Ray Strode <rstrode@redhat.com> 1.5.2-1
- Update to 1.5.2
  Related: #646666

* Thu Oct  7 2010 Matthias Clasen <mclasen@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Fri Oct 01 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.4.0-2
- Merge-review cleanup (#226498)

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.2-1
- Update to 1.3.2

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Mon Jun 07 2010 Christian Krause <chkr@fedoraproject.org> - 1.2.1-2
- Rebuild against new mono-addins

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> - 1.2.1-1
- Update to 1.2.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 1.1.4-1
- Update to 1.0.4

* Fri Feb 12 2010 Caolán McNamara <caolanm@redhat.com> - 1.0.0-3
- Rebuild for dependencies

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 1.0.0-2
- exclude sparc64  no mono available

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.7-1
- Update to 0.15.7

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.6-1
- Update to 0.15.6

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.15.5-2
- Build for ppc64.

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.5-1
- Update to 0.15.5

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.4-1
- Update to 0.15.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.2-1
- Update to 0.15.2

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.1-1
- Update to 0.15.1

* Fri May 15 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.0-2
- Update to 0.15.0

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 0.14.1-1
- Update to 0.14.1
- See http://download.gnome.org/sources/tomboy/0.14/tomboy-0.14.1.news

* Sun Apr  5 2009 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Split off a silly one-file devel package (#476251)

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Tue Mar  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.13.6-2
- Applets must not register with the session manager

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 0.13.6-1
- Update to 0.13.6

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Matthias Clasen <mclasen@redhat.com> - 0.13.5-1
- Update to 0.13.5

* Sun Feb  8 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.13.4-2
- Rebuild against new mono stack to fix broken deps

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.13.4-1
- Update to 0.13.4

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 0.13.3-1
- Update to 0.13.3

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.2-3
- Update to 0.13.2

* Mon Dec  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.1-6
- Rebuild for pkg-config deps

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.1-5
- Rebuild against new gmime

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.1-4
- Update to 0.13.1

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.12.0-6
- Better URL
- Tweak %%description

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12.0-5
- add BR: gnome-desktop-sharp-devel

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12.0-4
- rebuild for new gnome-sharp

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> - 0.12.0-3
- Apply upstream patch to fix crasher when gnome-panel-devel
  isn't installed.

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 0.12.0-2
- Save some space

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11.3-2
- fix license tag

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.3-1 
- Update to 0.11.3

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.1-1 
- Update to 0.11.1

* Sun Jul  6 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.11.0-4
- rebuild for mono dependencies

* Wed Jun 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11.0-3
- Add error messages instead of empty lines. Resolves "warning CS0642: Possible mistaken empty statement" errors.

* Wed Jun 04 2008 Caolán McNamara <caolanm@redhat.com> - 0.11.0-2
- rebuild for mono dependancies

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1 
- Update to 0.11.0

* Fri Apr 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10.1-2
- add mono-addins-devel as a BuildRequires, so Tomboy doesn't carry a local copy
  of Mono.Addins

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Mon Mar  3 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.8-1
- Update to 0.9.8

* Tue Feb 26 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.7-1
- Update to 0.9.7

* Sat Feb 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.6-2
- Fix dbus BR

* Wed Feb 13 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.6-1
- Update to 0.9.6

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.5-1
- Update to 0.9.5

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.9.3-1
- Update to 0.9.3

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Tue Nov  6 2007 Ray Strode <rstrode@redhat.com> - 0.8.1-2
- Fix bug 252294 (CVE-2005-4790)

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1
- Update to 0.8.1 (bug fixes)

* Thu Sep 20 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-2
- Don't show the start here note on login

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.8-1
- Update to 0.7.8

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.6-1
- Update to 0.7.6

* Sat Aug 25 2007 Ray Strode <rstrode@redhat.com> - 0.7.4-3
- Not sure why ppc64 is excluded and it's causing a broken
  conduit dep, try adding it back to the build.
- Mono isn't available on ppc64, get rid of it again from 
  the build

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.7.4-2
- Rebuild for build ID

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4
- Update the license field

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.3-2
- Fix a default value in the GConf schema

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.7.2-2
- rebuild for toolchain bug

* Mon Jul 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Wed Feb 28 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-1
- Update to 0.5.9

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.8-1
- Update to 0.5.8

* Wed Jan 31 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.5-1
- Update to 0.5.5

* Thu Jan 11 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Wed Sep  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Wed Sep  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.0-2
- Fix an issue with the applet icon size (205379)

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Fri Aug 18 2006 Alexander Larsson <alexl@redhat.com> - 0.3.9-3
- Rebuild with new mono and gtk-sharp2

* Mon Aug 14 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.9-2.fc6
- Make the about dialog close (#202355)

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.9-1.fc6
- Update to 0.3.9
- Fix %%preun script
- Use upstream icons

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 0.3.5-7
- rebuild
- Add missing br gettext
- don't build on s390(x)

* Thu May 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 0.3.5-5
- rebuild

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.5-4
- Add missing BuildRequires

* Fri Feb 17 2006 Christopher Aillon <caillon@redhat.com> - 0.3.5-3
- Don't run tomboy in the current working directory

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 0.3.5-2
- Rebuild

* Tue Feb  7 2006 Jesse Keating <jkeating@redhat.com> - 0.3.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Christopher Aillon <caillon@redhat.com> - 0.3.5-1
- Tomboy 0.3.5

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 0.3.4-2
- Rebuild

* Mon Jan 30 2006 Alexander Larsson <alexl@redhat.com> - 0.3.4-1
- update to 0.3.4

* Fri Jan 13 2006 Alexander Larsson <alexl@redhat.com> 0.3.3-5
- Add gtkspell requirement

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 0.3.3-4
- Better icons

* Thu Dec  8 2005 Alexander Larsson <alexl@redhat.com> 0.3.3-3
- rebuild for new dbus

* Fri Nov 18 2005 Alexander Larsson <alexl@redhat.com> 0.3.3-2
- Make dlls and exes executable to pick up dependencies

* Wed Nov 16 2005 Alexander Larsson <alexl@redhat.com> - 0.3.3-1
- Initial package

