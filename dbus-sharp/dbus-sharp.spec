%define debug_package %{nil}

Summary: C# bindings for D-Bus
Name: dbus-sharp
Version: 0.7.0
Release: 13%{?dist}
Epoch: 1
URL: http://mono.github.com/dbus-sharp/
Source0: https://github.com/downloads/mono/dbus-sharp/%{name}-%{version}.tar.gz
License: MIT
Group: System Environment/Libraries
BuildRequires: mono-devel
BuildRequires: autoconf
BuildRequires: automake, libtool
# Mono only available on these:
ExclusiveArch: %mono_arches

%description
D-Bus mono bindings for use with mono programs.

%package devel
Summary: Development files for D-Bus Sharp
Group: Development/Libraries
Requires: %name = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description devel
Development files for D-Bus Sharp development.

%prep
%setup -q

%build
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
autoreconf --force --install
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure --libdir=%{_prefix}/lib
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%files
%doc COPYING README
%{_prefix}/lib/mono/dbus-sharp-1.0
%{_prefix}/lib/mono/gac/dbus-sharp

%files devel
%{_libdir}/pkgconfig/dbus-sharp-1.0.pc

%changelog
* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 1:0.7.0-13
- Build for mono 4

* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 1:0.7.0-12
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 1:0.7.0-9
- Change ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Christian Krause <chkr@fedoraproject.org> - 1:0.7.0-5
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 19 2011 Christian Krause <chkr@fedoraproject.org> - 1:0.7.0-3
- Fix path in pkgconfig file for x86_64

* Tue Oct 18 2011 Christian Krause <chkr@fedoraproject.org> - 1:0.7.0-2
- Minor spec file cleanup (remove unnecessary %%defattr)

* Mon Oct 17 2011 Christian Krause <chkr@fedoraproject.org> - 1:0.7.0-1
- Migrating to new uptream source
- Initial spec file changes by Denis Washington <denisw@online.de>

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Dan Horák <dan[at]danny.cz> - 0.63-16
- updated the supported arch list

* Tue Oct 26 2010 Christian Krause <chkr@fedoraproject.org> - 0.63-15
- Rebuilt against Mono 2.8

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.63-14
- ExcludeArch sparc64

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-13.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Karsten Hopp <karsten@redhat.com> 0.63-12.1
- mono is now available on s390x

* Mon May 25 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.63-12
- build arch ppc64.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-10
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.63-9
- Autorebuild for GCC 4.3

* Tue Oct  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.63-8
- Add alpha to ExlusiveArch

* Tue Oct  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.63-7
- Fix license field
- Add pkgconfig dependency to the -devel package

* Wed Aug 30 2006 Alexander Larsson <alexl@redhat.com> - 0.63-6
- Fix connection and message gc problem (#187452)
- Patch from Christian Krause

* Fri Aug 18 2006 Alexander Larsson <alexl@redhat.com> - 0.63-5
- Update for new mono multilib setup
- Don't buildrequire old gtk-sharp

* Thu Jul 20 2006 John (J5) Palmieri <johnp@redhat.com> - 0.63-4
- Remove from the s390 builds

* Thu Jul 20 2006 Warren Togami <wtogami@redhat.com> - 0.63-3
- remove unnecessary obsolete

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.63-2
- Spec file cleanups

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.63-1
- Initial dbus-glib package
