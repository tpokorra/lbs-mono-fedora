%global         majorver 2.2
%global         minorver 0
%global         debug_package %{nil}

Name:           docky
Version:        %{majorver}.%{minorver}
Release:        4%{?dist}
Summary:        Advanced dock application written in Mono
License:        GPLv3+
URL:            http://wiki.go-docky.com
Source0:        https://launchpad.net/docky/%{majorver}/%{version}/+download/%{name}-%{version}.tar.xz
# The "Icon Magnification" was removed from "Docky" due 
# to a potential violation of US Patent 7434177
Patch0:         docky-nozoom.patch
Patch1:         docky-startscript-path.patch
# Logind support checked out from upstream bzr repository
Patch3:         1841_1840.patch
BuildRequires:  gnome-sharp-devel gtk-sharp2-devel gnome-desktop-sharp-devel
BuildRequires:  gnome-keyring-sharp-devel gtk-sharp2-gapi mono-addins-devel
BuildRequires:  mono-devel ndesk-dbus-devel ndesk-dbus-glib-devel
BuildRequires:  notify-sharp-devel GConf2-devel
# Docky does not use gio-sharp library yet (it has its own for now)
BuildRequires:  gio-sharp-devel dbus-sharp-devel dbus-sharp-glib-devel
# native deps
BuildRequires:  python2-devel
BuildRequires:  glib2-devel gtk2-devel
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Requires:       gnome-sharp gtk-sharp2 gnome-desktop gnome-desktop-sharp
Requires:       gnome-keyring-sharp gtk-sharp2-gapi mono-addins
Requires:       mono-core ndesk-dbus notify-sharp gtk2 GConf2
Requires:       hicolor-icon-theme
# Docky does not use gio-sharp library yet (it has its own for now)
Requires:       gio-sharp dbus-sharp dbus-sharp-glib
Requires:       ndesk-dbus-glib
# Mono only available on these:
ExclusiveArch:  %{ix86} x86_64 ppc %{power64} ia64 %{arm} sparcv9 alpha s390x

%description
Docky is an advanced shortcut bar that sits at the bottom, top, and/or sides 
of your screen. It provides easy access to some of the files, folders, 
and applications on your computer, displays which applications are 
currently running, holds windows in their minimized state, and more.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files
for developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3

%build
%configure --disable-schemas-install \
           --with-gconf-schema-file-dir=%{_sysconfdir}/gconf/schemas
# do not use %{?_smp_mflags} here - LP:983001
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

#gapi_codegen.exe is not distributed (licence is GNU GPL v2)
rm -f %{buildroot}%{_libdir}/%{name}/gapi_codegen*

desktop-file-install    \
        --dir %{buildroot}%{_sysconfdir}/xdg/autostart       \
        --add-only-show-in=GNOME                                \
        %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --delete-original  \
        --dir %{buildroot}%{_datadir}/applications   \
        --remove-category Application \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

# autostart is disabled by default
echo "X-GNOME-Autostart-enabled=false" >> \
    %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}.desktop

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING COPYRIGHT NEWS
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/apps/gmail.png
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/gconf/schemas/docky.schemas
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_mandir}/man1/%{name}.1*

%files devel
%{_libdir}/pkgconfig/docky.*.pc

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 2.2.0-2
- Replace ppc64 with power64 macro

* Thu Sep 19 2013 Christopher Meng <rpm@cicku.me> - 2.2.0-1
- Update to 2.2.0(BZ#958779)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 2.1.4-1
- version bump - new 2.1 stable branch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0.12-3
- Bump build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 10 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.12-1
- version bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.11-1
- version bump

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 2.0.10-2
- updated the supported arch list

* Mon Jan 10 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.10-1
- Version bump
- Man page added
- Patch for shebang not needed anymore (fixed in mainstream)

* Mon Oct 25 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-3
- Fixing many things reported in the bug 635450
- Licence change
- Zooming code completly removed

* Mon Oct 25 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-2
- Fixed requirement on mono-core

* Mon Oct 18 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-1
- Version bump

* Mon Sep 06 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.6-1
- Initial package
- Many fixes in spec (thank to Christian Krause)

* Mon Sep 06 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.6-1
- Initial package
