%global			debug_package %{nil}
%global			mainver 0.95.1

Name:			gnome-do
Version:		%{mainver}
Release:		4%{?dist}
Summary:		Quick launch and search

License:		GPLv3+
Group:			Applications/File
URL:			http://do.cooperteam.net/
# http://launchpad.net/do/trunk/0.95.1/+download/gnome-do-0.95.1.tar.gz
Source0:		http://launchpad.net/do/trunk/%{mainver}/+download/gnome-do-%{version}.tar.gz

BuildRequires:		mono-devel, mono-addins-devel
BuildRequires:		mono-nunit-devel
BuildRequires:		desktop-file-utils
BuildRequires:		dbus-sharp-devel
BuildRequires:		dbus-sharp-glib-devel
BuildRequires:		GConf2-devel
BuildRequires:	        gtk-sharp2-devel, notify-sharp-devel
BuildRequires:		gnome-sharp-devel, gnome-desktop-sharp-devel >= 2.26
BuildRequires:		gnome-keyring-sharp-devel
BuildRequires:		gettext
BuildRequires:		perl-XML-Parser
BuildRequires:		intltool
BuildRequires:		gtk2-devel
BuildRequires:		desktop-file-utils
BuildRequires:		gio-sharp-devel
BuildRequires:		gkeyfile-sharp-devel
BuildRequires:		autoconf automake libtool

Requires(pre):		GConf2
Requires(post):		GConf2
Requires(preun):	GConf2

Requires:		mono(NDesk.DBus.GLib) = 1.0.0.0
Requires:		gnome-keyring-sharp, gnome-desktop-sharp, findutils
Requires:		gnome-desktop, pkgconfig
Requires:               gio-sharp, gkeyfile-sharp

# Mono only available on these:
ExclusiveArch: %mono_arches

%description
GNOME Do (Do) is an intelligent launcher tool that makes performing
common tasks on your computer simple and efficient. Do not only allows
you to search for items in your desktop environment
(e.g. applications, contacts, bookmarks, files, music), it also allows
you to specify actions to perform on search results (e.g. run, open,
email, chat, play).

%package devel
Summary:		Development files for GNOME Do
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		pkgconfig

%description devel
Development files for GNOME Do

%prep
%setup -q

sed -i "s#gmcs#mcs#g" configure*
sed -i "s#gmcs#mcs#g" m4/shamrock/mono.m4

%build
NOCONFIGURE=1 autoreconf -vif
%configure
make %{?_smp_mflags}


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install	\
	--dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart	\
	--add-only-show-in=GNOME				\
	$RPM_BUILD_ROOT%{_datadir}/applications/gnome-do.desktop
desktop-file-install --delete-original	\
	--dir $RPM_BUILD_ROOT%{_datadir}/applications	\
	--remove-category Application	\
	$RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


#own this dir:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/

%find_lang %{name}

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%doc AUTHORS COPYING COPYRIGHT
%{_bindir}/gnome-do
%{_libdir}/gnome-do/
%{_datadir}/gnome-do/
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-do.desktop
%config(noreplace) %{_sysconfdir}/gconf/schemas/*
%{_datadir}/icons/hicolor/*/apps/gnome-do.*
%{_datadir}/applications/*

%files devel
%{_libdir}/pkgconfig/*

%changelog
* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.95.1-4
- Rebuild (mono4)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Juan Rodriguez <nushio@fedoraproject.rog> -0.95.1-1
- Updated RPM Url
- Updated package to version 0.95.1

* Sun May 25 2014 Brent Baude <baude@us.ibm.com> - 0.9-6
- Changing ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Theodore Lee <theo148@gmail.com> - 0.9-2
- Build with gmcs instead of dmcs

* Mon Mar 05 2012 Theodore Lee <theo148@gmail.com> - 0.9-1
- Update to latest upstream release
- Drop upstreamed xargs and about dialog patches
- Switch build dependencies from ndesk-dbus to dbus-sharp

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.8.5-8
- Rebuild for new libpng

* Thu Aug 18 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-7
- Explicitly require gnome-desktop

* Thu Aug 18 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-6
- Rebuild for rpm-4.9.1 bug

* Thu Jul 21 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-5
- Fix bindir entry in file listing

* Thu Jul 21 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-4
- Add patch for About window bug

* Sat Jul 16 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-3
- Add patch for minor ExecuteWithArguments bugs

* Fri Jul 15 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-2
- Add requires on findutils (for xargs)
- Obsolete docklets

* Tue Jun 28 2011 Theodore Lee <theo148@gmail.com> - 0.8.5-1
- Update to latest upstream release
- Use global instead of define
- Drop patches for issues that have been fixed upstream

* Sun Mar 13 2011 Theodore Lee <theo148@gmail.com> - 0.8.4-0.3.aa
- Update patch for opening weird filenames

* Fri Mar 11 2011 Theodore Lee <theo148@gmail.com> - 0.8.4-0.2.aa
- Add unreleased fixes for opening weird filenames and the email action
- Updated to latest upstream release, which has dropped Docky
- Remove unnecessary Docky patch
- Add patch to get rid of linebreak in desktop file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.8.3.1-4
- updated the supported arch list

* Fri Oct 29 2010 Christian Krause <chkr@fedoraproject.org> - 0.8.3.1-3
- Rebuilt against Mono 2.8
- Add patch for compiling against Mono 2.8
- Add patch to not set DGDK_DISABLE_DEPRECATED

* Fri Jun 04 2010 Christian Krause <chkr@fedoraproject.org> - 0.8.3.1-2
- Rebuilt against new mono-addins

* Wed Nov 18 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.8.2-5
- Restored "Docky", but removed Icon Zoom due to potential violation of patents.

* Tue Nov 10 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.2-4
- Remove "Docky" due to patent issues

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.8.2-3
- Exclude sparc64  no mono available

* Mon Aug 24 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.8.2-2
- Fixes gnome-do plugin permissions.

* Thu Aug 20 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2

* Thu Aug 20 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.1.3-7
- Rebuild for ppc64 as the previous build was obsoleted.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.8.1.3-6
- Build arch ppc64.

* Fri Apr 10 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.1.3-5
- Fix .desktop issue, install in both autostart and applications
- Rebuild for new gnome-desktop-sharp
- Add missing gnome-desktop-sharp requires
- Fix Ndesk-dbus Requires

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.1.3-3
- Add patch to fix issue where applications wasn't being indexed

* Tue Mar 17 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.1.3-2
- New upstream release

* Tue Mar 3 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.0-4
- Own _datadir/gnome-do
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Michel Salim <salimma@fedoraproject.org> - 0.8.0-2
- Rebuild against new mono-addins

* Fri Jan 30 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.0-1
- New upstream release

* Thu Jan 29 2009 Michel Salim <salimma@fedoraproject.org> - 0.6.1.0-3
- Remove Tomboy dependency (bz #481183)
- Updated description, from Do

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.1.0-2
- rebuild against new gnome-sharp

* Wed Oct 08 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.1.0-1
- New Upstream Release

* Fri Oct 03 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.0.1-1
- New upstream release

* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.0.0-1
- New upstream release

* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.5.0.1-4
- New upstream release
- Add gnome-desktop-sharp dependency

* Wed Jun 04 2008 Caolán McNamara <caolanm@redhat.com> - 0.4.2.0-2
- rebuild for dependancies

* Tue Apr 22 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.4.2.0-1
- New upstream release

* Tue Apr 01 2008 David Nielsen <gnomeuser@gmail.com> - 0.4.0.1-2
- #439793 - correct URL

* Sat Mar 29 2008 David Nielsen <gnomeuser@gmail.com> - 0.4.0.1-1
- Bump to 0.4.0.1
- Hopefully bring an end to the endless dups of 432201

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.3.1-2
- Fix 432201

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.3.1-1
- Bump to 0.3.1

* Wed Feb 06 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-5
- #431589 - Force runtime dependency on ndesk-dbus(-glib)

* Mon Feb 04 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-4
- #431462 - Correctly pull in Tomboy runtime dependency

* Fri Jan 25 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-3
- autostart gnome-do in quiet mode with the user session
- to invoke gnome-do use super+space

* Tue Jan 22 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-2
- Fix BuildRequires

* Tue Jan 22 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-1
- bump to 0.3.0.1
- update patches

* Sat Nov 17 2007 David Nielsen <david@lovesunix.net> - 0.0.2-2
- updated libdir patch
- cleaned up desktop-file-install invocation
- correct BuildRequires

* Mon Nov 12 2007 David Nielsen <david@lovesunix.net> - 0.0.2-1
- Initial package
