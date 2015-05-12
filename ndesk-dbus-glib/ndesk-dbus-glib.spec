%define			debug_package %{nil}

Name:			ndesk-dbus-glib
URL:			http://www.ndesk.org/DBusSharp
License:		MIT
Group:			Development/Libraries
Version:		0.4.1
Release:		17%{?dist}
Summary:		Provides glib mainloop integration for ndesk-dbus
Source0:		http://www.ndesk.org/archive/dbus-sharp/ndesk-dbus-glib-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:	mono-devel
## This EVR is necessary due to the WaitForIOCompletion API added in the Sugar
## datastore patch.
BuildRequires:	ndesk-dbus-devel >= 0.6.1a-7

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc %{power64} ia64 %{arm} sparcv9 alpha s390x

%description
ndesk-dbus-glib provides glib mainloop integration for ndesk-dbus

%package devel
Summary:		Development files for ndesk-dbus-glib
Group:			Development/Libraries
Requires:		ndesk-dbus-glib = %{version}
Requires:		ndesk-dbus-devel
Requires:		pkgconfig

%description devel
Development files for ndesk-dbus-glib

%prep
%setup -q

%build
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{_prefix}/lib/mono/gac/NDesk.DBus.GLib/
%{_prefix}/lib/mono/ndesk-dbus-glib-1.0/

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/pkgconfig/ndesk-dbus-glib-1.0.pc

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 0.4.1-16
- Changed ppc64 arch to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Christian Krause <chkr@fedoraproject.org> - 0.4.1-12
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Dan Horák <dan[at]danny.cz> - 0.4.1-10
- updated the supported arch list

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.4.1-8
- ExcludeArch sparc64

* Wed Jul 29 2009 Peter Gordon <peter@thecodergeek.com> - 0.4.1-7
- Apply patch from Torello Querci to fix reading from the socket with the
  Sugar datastore (#503151):
  + sugar-datastore.patch
- Bump minimum required ndesk-dbus version (for the WaitForIOCompletion API 
  added in the Sugar datastore patch).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.4.1-5
- Build arch ppc64.

* Thu Feb 26 2009 David Nielsen <dnielsen@fedoraproject.org> - 0.4.1-4
- Rebuild for stack update (#487155)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.1-3
- Autorebuild for GCC 4.3

* Sat Dec 29 2007 David Nielsen <david@lovesunix.net> - 0.4.1-2
- -devel now requires ndesk-dbus-devel

* Thu Nov  8 2007 David Nielsen <david@lovesunix.net> - 0.4.1-1
- bump to 0.4.1
- clean up spec
- remove review blockers

* Sun Oct 21 2007 David Nielsen <david@lovesunix.net> - 0.3-7
- revert noarch change accord to the guidelines to accommodate
- post packaging AOT.

* Tue Oct 16 2007 David Nielsen <david@lovesunix.net> - 0.3-6
- Make noarch

* Thu Jul  5 2007 David Nielsen <david@lovesunix.net> - 0.3-5
- Don't build on ppc64 due to mising deps, see bug 241850

* Wed Jul  4 2007 David Nielsen <david@lovesunix.net> - 0.3-4
- fix spaces vs. tabs
- fix %%defattr
- No longer build as noarch
- make setup quiet

* Mon Jun 25 2007 David Nielsen <david@lovesunix.net> - 0.3-3
- reduced amount of ugly hacks in the spec

* Mon Jun 25 2007 David Nielsen <david@lovesunix.net> - 0.3-2
- Let's not be stupid .mdb files don't go in -devel

* Sat Jun 23 2007 David Nielsen <david@lovesunix.net> - 0.3-1
- Initial package
