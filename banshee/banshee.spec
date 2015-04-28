Name:    banshee
Version: 2.6.2
Release: 9%{?dist}
Summary: Easily import, manage, and play selections from your music collection

License: MIT
URL:     http://banshee.fm/
Source0: http://ftp.gnome.org/pub/GNOME/sources/banshee/2.6/banshee-%{version}.tar.xz

# GStreamer 1.0 patches from Debian:
Patch2: Initial-port-to-GStreamer-1.0.patch
Patch3: Remove-build-time-enable-gapless-playback-option.patch
Patch4: Don-t-use-the-new-decoded-pad-signal-of-decodebin.patch
Patch5: Use-new-style-GStreamer-1.0-raw-audio-caps-in-the-WA.patch
# Backported crash fix from upstream
Patch6: Dont-try-to-mount-null-devices.patch
# Bugzilla 1167029
Patch7: banshee-2.6.2-gst1.0-handle-events-fix.patch
# Add sqlite-hints
# https://bugzilla.gnome.org/show_bug.cgi?id=740879
Patch8: banshee-2.6.2-sqlite-hints.patch

# Mono only available on these:
ExclusiveArch: %{mono_arches}

BuildRequires: mono-devel
BuildRequires: mono-zeroconf-devel >= 0.9.0-2
BuildRequires: sqlite-devel >= 3.4
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: gstreamer1-plugins-good
BuildRequires: libmtp-devel >= 0.2.0
# explicitly depend on dbus-glib-devel for
# https://bugzilla.redhat.com/show_bug.cgi?id=867133
BuildRequires: dbus-glib-devel
BuildRequires: GConf2-devel
BuildRequires: libappstream-glib

# Web Browser
BuildRequires: webkitgtk-devel

# Sharp
BuildRequires: gio-sharp-devel gtk-sharp-beans-devel
BuildRequires: gkeyfile-sharp-devel gudev-sharp-devel
BuildRequires: gtk-sharp2-devel taglib-sharp-devel
BuildRequires: gnome-sharp-devel notify-sharp-devel
%ifnarch s390 s390x
BuildRequires: libgpod-sharp-devel >= 0.8.2
%endif
BuildRequires: gdata-sharp-devel
BuildRequires: dbus-sharp-devel >= 1:0.7.0
BuildRequires: dbus-sharp-glib-devel

# Extra mono deps
BuildRequires: mono-data mono-data-sqlite mono-addins-devel

# Gnome/Glib
BuildRequires: gnome-desktop-devel

# X
BuildRequires: libXxf86vm-devel

# Misc
BuildRequires: gnome-doc-utils gettext-devel intltool perl(XML::Parser)

# Disable boo support until boo is available again for Mono 2.8
# BuildRequires: boo-devel

# Building with nunit installed causes banshee to require it at runtime
#BuildRequires: mono-nunit-devel

BuildRequires: desktop-file-utils

# Snapshots only
BuildRequires: autoconf automake libtool

Requires:      shared-mime-info
Requires:      gstreamer1-plugins-good
%ifnarch s390 s390x
Requires:      libgpod-sharp >= 0.8.2
Requires:      gvfs-afc
%endif
Requires:      gio-sharp gtk-sharp-beans
Requires:      media-player-info

Obsoletes: banshee-meego < 2.2.1-4
Obsoletes: banshee-musicbrainz < 2.6.2

%description
Banshee allows you to import CDs, sync your music collection to an iPod,
play music directly from an iPod, create playlists with songs from your
library, and create audio and MP3 CDs from subsets of your library.

%package devel
Summary:        Development files for Banshee
Requires:       %{name} = %{version}-%{release}
Obsoletes:      banshee-musicbrainz-devel < 2.6.2

%description devel
Banshee allows you to import CDs, sync your music collection to an iPod,
play music directly from an iPod, create playlists with songs from your
library, and create audio and MP3 CDs from subsets of your library.

The %{name}-devel package contains libraries and header files for
developing extensions for %{name}.

%prep
%setup -q
%patch2 -p1 -b .gst1
%patch3 -p1 -b .gapless
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1 -b .handle-events-fix
%patch8 -p1 -b .sqlite-hints

%build
# Snapshots only
NOCONFIGURE=1 ./autogen.sh

%configure  --disable-docs --enable-mtp \
%ifarch s390 s390x
            --disable-appledevice \
%endif
            --with-vendor-build-id=Fedora%{?fedora}-%{version}-%{release} \
            --disable-boo --disable-clutter --disable-meego

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/banshee.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/banshee/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/banshee/b.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/banshee/c.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/banshee/d.png 

# clean-up .a archives
find %{buildroot} \( -name '*.la' -or -name '*.a' \) -exec rm -f {} \;

# mono's .config files don't need to be executable
find $RPM_BUILD_ROOT -name '*.config' -exec chmod a-x {} \;

%find_lang %{name} --with-gnome

%check
make check V=1

desktop-file-validate %{buildroot}%{_datadir}/applications/banshee*.desktop

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc COPYING AUTHORS README NEWS
%{_bindir}/banshee
%{_bindir}/muinshee
%{_bindir}/bamz
%{_libdir}/banshee
%{_datadir}/appdata/banshee.appdata.xml
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.bansheeproject.Banshee.service
%{_datadir}/dbus-1/services/org.bansheeproject.CollectionIndexer.service
%{_datadir}/banshee/
%{_datadir}/icons/hicolor/*/apps/media-player-banshee.png
%{_datadir}/mime/packages/*

%files devel
%{_libdir}/pkgconfig/banshee-*.pc

%changelog
* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 2.6.2-9
- Use better AppData screenshots

* Wed Dec 10 2014 Tom Callaway <spot@fedoraproject.org> 2.6.2-8
- add sqlite hinting

* Tue Dec  2 2014 Tom Callaway <spot@fedoraproject.org> 2.6.2-7
- fixed version of last patch, thanks to Fabrice Bellet

* Wed Nov 26 2014 Tom Callaway <spot@fedoraproject.org> 2.6.2-6
- add fix to allow vaapisink in gst1.0 to handle GstNavigation stuff properly (bz1167029)

* Sat Aug 16 2014 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-5
- update mime scriptlets

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Eric "Sparks" Christensen <sparks@fedoraproject.org> - 2.6.2-2
- Added patch to fix BZ 1012176

* Sun Mar 09 2014 Kalev Lember <kalevlember@gmail.com> - 2.6.2-1
- Update to 2.6.2
- Fold banshee-musicbrainz into the main package
- Add two more GStreamer 1.0 patches from Debian

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Mon Apr  1 2013 Tom Callaway <spot@fedoraproject.org> - 2.6.0-4
- gstreamer 1.0 support

* Sat Mar 30 2013 Kalev Lember <kalevlember@gmail.com> - 2.6.0-3
- Initialize dbus threads (#867133)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Christian Krause <chkr@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Mon Mar 26 2012 Christian Krause <chkr@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Sun Feb 26 2012 Christian Krause <chkr@fedoraproject.org> - 2.2.1-4
- Drop MeeGo sub-package since the required mutter-meego package
  is not available anymore

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 11 2011 Dan Horák <dan[at]danny.cz> - 2.2.1-2
- fix Requires on s390(x)
- switch to a macro for the list of Mono arches

* Thu Nov 17 2011 Christian Krause <chkr@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1
- Comment out snapshot-only buildreqs
- Switch from ndesk dbus stuff to dbus-sharp
- Add requires on media-player-info
- Add patch to fix compiling with newer versions of libgpod-sharp
- Bump required version of libgpod-sharp-devel to 0.8.2
- Disable clutter due to a compile issue - according to upstream
  the clutter support is currently not functional:
  https://bugzilla.gnome.org/show_bug.cgi?id=620073

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Sun May 22 2011 Christian Krause <chkr@fedoraproject.org> - 2.0.1-2
- Require gvfs-afc for iPhone support (BZ 704313)

* Thu May 05 2011 Christian Krause <chkr@fedoraproject.org> - 2.0.1-1
- Update to stable release 2.0.1

* Wed Apr 06 2011 Christian Krause <chkr@fedoraproject.org> - 2.0.0-2
- Rebuilt against gio-sharp-0.3

* Tue Apr 05 2011 Christian Krause <chkr@fedoraproject.org> - 2.0.0-1
- Update to stable release 2.0.0

* Tue Mar 29 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.6-1
- Update to development release 1.9.6

* Thu Mar 10 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.5-1
- Update to development release 1.9.5

* Sat Feb 26 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.4-1
- Update to development release 1.9.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.3-1
- Update to development release 1.9.3

* Sat Jan 15 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.2-1
- Update to development release 1.9.2

* Wed Jan 12 2011 Dan Horák <dan[at]danny.cz> - 1.9.1-2
- updated the supported arch list

* Sat Jan 08 2011 Christian Krause <chkr@fedoraproject.org> - 1.9.1-1
- Update to development release 1.9.1
- Drop upstreamed patches
- Some spec file cleanup

* Fri Dec 31 2010 Christian Krause <chkr@fedoraproject.org> - 1.8.0-12
- Add MeeGo sub-package (BZ 660334)
- Make all of mono *.config files non-executable

* Fri Oct 29 2010 Christian Krause <chkr@fedoraproject.org> - 1.8.0-11
- Rebuilt against Mono 2.8
- Disable Boo support

* Mon Oct 25 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-10
- Add a patch to fix CVE-2010-3998

* Tue Oct 19 2010 Dan Horák <dan[at]danny.cz> - 1.8.0-9
- Update the Requires to match BR on s390(x)

* Tue Oct 19 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-8
- Added gnome-doc-utils BR

* Mon Oct 18 2010 Dan Horák <dan[at]danny.cz> - 1.8.0-7
- Fix BRs and configure options on s390(x)
- Be verbose during build

* Mon Oct 11 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-6
- Fix download URL

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-5
- Add upstream patch to fix sync screen

* Tue Oct 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-4
- Added manual requires for libgpod-sharp, gio-sharp, gtk-sharp-beans
- Remove podsleuth dependency

* Tue Oct 05 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-3
- Removed hal and ipod-sharp BR
- Removed libmtp-hal Requires
- Added gio-sharp, gtk-sharp-beans, gudev-sharp and gkeyfile-sharp BR
- Enabled apple device building on s390 s390x (hopefully this works)
- Added --disable-hal and --disable-ipod to configure

* Fri Oct 01 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-2
- Add versioned BR for libgpod

* Fri Oct 01 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-1
- Update to 1.8.0

* Fri Oct 01 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.6-1
- Update to 1.7.6
- Remove upstreamed build fix patch
- Remove upstreamed mimedb patch
- Update desktop-database patch to apply against 1.7.6
- Fix gtkwebkit dependency to enable web music stores
- Add libgpod-sharp to build requires

* Fri Oct 01 2010 Dan Horák <dan[at]danny.cz> - 1.7.4-3
- Fix BRs and configure options on s390(x) and ppc(64)

* Wed Sep 08 2010 Christian Krause <chkr@fedoraproject.org> - 1.7.4-2
- Add patch to properly comment out some make rules (BZ 631387)

* Tue Aug 17 2010 Christian Krause <chkr@fedoraproject.org> - 1.7.4-1
- Update to development release 1.7.4 (BZ 623624)
- Remove upstreamed patches
- Add patches to avoid calling update-mime-database or
  update-desktop-database during "make install"
- Cleanup scriptlets
- Add update-mime-database to %%post / %%postun

* Sat Jun 26 2010 Christian Krause <chkr@fedoraproject.org> - 1.6.1-5
- Fix status icon transparency (BZ 533308)

* Fri Jun 18 2010 Christian Krause <chkr@fedoraproject.org> - 1.6.1-4
- avoid "DllNotFoundException: libbnpx11" when switching to
  fullscreen mode

* Thu Jun 17 2010 Bastien Nocera <bnocera@redhat.com> - 1.6.1-3
- Require libmtp-hal package to get device information, to be
  removed when banshee uses udev

* Tue Jun 01 2010 Christian Krause <chkr@fedoraproject.org> - 1.6.1-2
- Add explicit Requires gstreamer-plugins-good (BZ 588063) to avoid
  that gstreamer stucks when loading files
- Rebuilt against new mono-addins

* Mon May 17 2010 Christian Krause <chkr@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1 release

* Wed Mar 31 2010 Christian Krause <chkr@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 release

* Thu Mar 25 2010 Christian Krause <chkr@fedoraproject.org> - 1.5.6-1
- Update to 1.5.6 release

* Fri Mar 12 2010 Christian Krause <chkr@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 release

* Sun Feb 28 2010 Christian Krause <chkr@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4 release
- Remove upstreamed patch (Spanish translation update)

* Thu Feb 18 2010 Karsten Hopp <karsten@redhat.com> -2.1
- disable ipod support on s390(x), enable boo support

* Thu Feb 04 2010 Christian Krause <chkr@fedoraproject.org> - 1.5.3-2
- Update Spanish translation

* Wed Feb 03 2010 Christian Krause <chkr@fedoraproject.org> - 1.5.3-1
- Update to final 1.5.3 release
- Remove upstreamed patch (last.fm integration)

* Wed Dec 16 2009 Christian Krause <chkr@fedoraproject.org> - 1.5.3-0.1.20091216git
- Update to latest snapshot to pick up DeviceKit-disks integration
  to fix iPod support (BZ 495240)
- Add a minor patch to fix the last.fm integration

* Mon Nov 23 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.2-1
- Update to final 1.5.2 release

* Wed Nov 18 2009 Christian Krause <chkr@fedoraproject.org> - 1.5.2-0.1.20091118git
- Update to latest snapshot
- Remove all *.la and *.a files during %%install

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 1.5.1-3
- ExcludeArch sparc64

* Thu Oct 22 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.1%{?patchver}-2
- Rebuild against new mono-zeroconf (bz #526132)

* Mon Oct 19 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.1-1
- Update to final 1.5.1 release

* Thu Sep 17 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.1-0.3.git20090917%{?dist}
- Update to latest snapshot
- Drop clutter10 patch (fixed upstream)

* Mon Aug 31 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.1-0.2.git20090831%{?dist}
- Build with clutter support

* Mon Aug 31 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.1-0.1.git20090831%{?dist}
- Update to latest snapshot

* Thu Aug 27 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.0-3
- Rebuild for boo update
- Remove unused dependency on nautilus-cd-burner

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Michel Salim <salimma@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Thu Apr 02 2009 David Nielsen <gnomeuser@gmail.com> - 1.4.3-3
- add patch to fix rh#492707 - Banshee use 100% when fetching cover art

* Sat Mar 07 2009 David Nielsen <dnielsen@fedoraproject.org> - 1.4.3-2
- add patch for gnomebz #536047

* Thu Mar 05 2009 David Nielsen <dnielsen@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3
- Remove upstreamed patch

* Wed Feb 25 2009 David Nielsen <dnielsen@fedoraproject.org> - 1.4.2-6
- Rebuilt for updated taglib-sharp

* Tue Feb 24 2009 David Nielsen <dnielsen@fedoraproject.org> - 1.4.2-5
- Clean out obsolete configuration arguments
- Remove unneeded build dependency
- Enable compiletime vendor identification at the request of upstream (#486285)
- Enable threaded build as per the Fedora standards

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.2-3
- Enable video mode support
- Enable unit tests if nunit-2.4 is available
- MusicBrainz subpackage no longer depends on main package

* Tue Feb 10 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.2-2
- Patch to correct timezone handling for podcasts (bz #484766)

* Fri Jan 23 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2
- Require mono-addins
- Enable menu entry on other desktops

* Thu Jan  1 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.1-4
- Manually require libmtp

* Thu Jan  1 2009 Michel Salim <salimma@fedoraproject.org> - 1.4.1-3
- Split MusicBrainz libraries into separate subpackages
- Properly tag songs ripped from CDs (bug #477669)

* Thu Dec 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.1-2
- rebuild to fix broken deps

* Thu Nov 27 2008 Michel Salim <salimma@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Mon Nov 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.0.1-1
- update to 1.4.0.1

* Mon Oct 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.1-3
- bump for new gnome-sharp

* Mon Aug 25 2008 Michel Salim <salimma@fedoraproject.org> - 1.2.1-2
- Updated requirement: use podsleuth rather than libipoddevice

* Sun Aug 24 2008 Michel Salim <salimma@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Jul 31 2008 Nigel Jones <dev@nigelj.com> - 1.2.0-2.1
- ifarching foo broke... now fixed

* Wed Jul 30 2008 Nigel Jones <dev@nigelj.com> - 1.2.0-2
- Reenable boo, I can't see why not now...

* Wed Jul 30 2008 Nigel Jones <dev@nigelj.com> - 1.2.0-1
- Update to 1.2.0 (new upstream release)
- Refer to: http://banshee-project.org/download/archives/1.2.0/ for more details

* Fri Jul 4 2008 Nigel Jones <dev@nigelj.com> - 1.0.0-2
- Bump for new gnome-sharp

* Fri Jun 6 2008 Nigel Jones <dev@nigelj.com> - 1.0.0-1
- Banshee goes GOLD!

* Wed Jun 4 2008 Nigel Jones <dev@nigelj.com> - 0.99.3-2
- Disable boo (again) - Broken dependencies and 'issues'

* Sat May 30 2008 Nigel Jones <dev@nigelj.com> - 0.99.3-1
- New Upstream Release (0.99.3) - RC 1

* Tue May 27 2008 Nigel Jones <dev@nigelj.com> - 0.99.2-3
- Rebuild for new gtk-sharp2

* Sat May 24 2008 Nigel Jones <dev@nigelj.com> - 0.99.2-2
- Rebuild & correct BR

* Fri May 23 2008 Nigel Jones <dev@nigelj.com> - 0.99.2-1
- New Upstream Release (0.99.2) - Beta 2
- Enable podcast & boo

* Sat May 5 2008 Nigel Jones <dev@nigelj.com> - 0.99.1-1.1
- Fix brainfart...  Comment out the cp for Source1 which I moved out of the way

* Sat May 5 2008 Nigel Jones <dev@nigelj.com> - 0.99.1-1
- New Upstream Release (0.99.1) - Beta 1 (Closes: Bug# 445449)
- boo doesn't work quite yet for us, this will most likely be enabled in a -2
  build (README.Fedora hence removed from sources)
- Spec file improvements per guidelines
- Put .pc files in their proper place

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.98.3-2
- adding BR: mono-addins-devel

* Sat Apr 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.98.3-1
- update to 0.98.3 (which doesn't have any prebuilt binaries in it)

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.13.3-4
- revert to using bundled boo as external has no ppc support currently

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.13.2-3
- Use external boo and ndesk-dbus
- Nicer workaround to gstreamer-plugin detection problem

* Fri Jan 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.2-2
- Add content-type support

* Mon Jan 14 2008 Christopher Aillon <caillon@redhat.com> - 0.13.2-1
- Update to 0.13.2

* Fri Aug 31 2007 Christopher Aillon <caillon@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Tue Aug  7 2007 Christopher Aillon <caillon@redhat.com> - 0.13.0-1
- Update to 0.13.0

* Sun May  6 2007 Matthias Clasen <mclasen@redhat.com> - 0.12.1-3
- Own /usr/share/banshee (#233823)

* Tue Apr 17 2007 Christopher Aillon <caillon@redhat.com> - 0.12.1-2
- Fix typo in schemas

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> - 0.12.1-1
- Update to 0.12.1

* Fri Mar 30 2007 Christopher Aillon <caillon@redhat.com> - 0.12.0-5
- Fix up schema installs

* Fri Mar 23 2007 Christopher Aillon <caillon@redhat.com> - 0.12.0-4
- Some more updates to the file list

* Tue Mar 20 2007 Christopher Aillon <caillon@redhat.com> - 0.12.0-3
- Remove %%{_datadir}/icons/hicolor/* from %%files

* Wed Mar  7 2007 Christopher Aillon <caillon@redhat.com> - 0.12.0-2
- Add gstreamer-plugins-good as a build dep for gconfaudiosink

* Wed Mar  7 2007 Christopher Aillon <caillon@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Fri Feb  2 2007 Christopher Aillon <caillon@redhat.com> - 0.11.5-1
- Update to 0.11.5

* Fri Sep  1 2006 Christopher Aillon <caillon@redhat.com> - 0.10.12-4
- Register banshee-notificationareaicon.schemas in %%post (bug 185605)
- Add dllmap for libdbus-glib so banshee works without dbus-glib-devel
  (bug 202990)

* Mon Aug 28 2006 Christopher Aillon <caillon@redhat.com> - 0.10.12-3
- Rebuild

* Sat Aug 26 2006 Christopher Aillon <caillon@redhat.com> - 0.10.12-2
- For some reason, the last build picked up dependencies on both
  mono(glib-sharp) = 2.8.0.0 and mono(glib-sharp) = 2.10.0.0
  Not sure why, but hopefully this rebuild fixes it....

* Wed Aug 23 2006 Christopher Aillon <caillon@redhat.com> - 0.10.12-1
- Update to 0.10.12
- Build against newer mono stack

* Mon Aug  7 2006 Nalin Dahyabhai <nalin@redhat.com> - 0.10.11-1
- Update to 0.10.11
- Buildrequire: dbus-sharp-devel, because configure looks for it
- Buildrequire: gettext-devel, because configure looks for its copy of msgfmt

* Fri Jun 16 2006 Jeremy Katz <katzj@redhat.com> - 0.10.10-2
- rebuild against new nautilus-cd-burner
- hack to get it to build

* Tue May  2 2006 Christopher Aillon <caillon@redhat.com> 0.10.10-1
- Update to 0.10.10

* Tue Mar 21 2006 Christopher Aillon <caillon@redhat.com> 0.10.9-1
- Update to 0.10.9

* Tue Mar 14 2006 Christopher Aillon <caillon@redhat.com> 0.10.8-1
- Update to 0.10.8

* Thu Mar  9 2006 Christopher Aillon <caillon@redhat.com> 0.10.7-2
- Add explicit Requires on libipoddevice (#184482)

* Tue Mar  7 2006 Christopher Aillon <caillon@redhat.com> 0.10.7-1
- Update to 0.10.7
- Fix build on x86-64

* Mon Mar  6 2006 Christopher Aillon <caillon@redhat.com> 0.10.6-3
- Don't build with smp_mflags, as parallel make causes the build to fail

* Sat Mar  4 2006 Christopher Aillon <caillon@redhat.com> 0.10.6-2
- Rebuild

* Tue Feb 21 2006 Christopher Aillon <caillon@redhat.com> 0.10.6-1
- Initial RPM
