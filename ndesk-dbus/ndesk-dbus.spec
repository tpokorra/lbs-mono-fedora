%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

%define			debug_package %{nil}

Name:			ndesk-dbus
Version:		0.6.1a
Release:		17%{?dist}
Summary:		Managed C# implementation of DBus

License:		MIT
Group:			System Environment/Libraries
URL:			http://www.ndesk.org/DBusSharp
Source0:		http://www.ndesk.org/archive/dbus-sharp/ndesk-dbus-%{version}.tar.gz

Patch0:			%{name}-sugar-datastore.patch

BuildRequires:	mono-devel

Requires:		mono-core

ExclusiveArch:	%{mono_arches}

%description
Managed C# implementation of DBus

%package devel
Summary:		Develpment files for the managed C# implementation of DBus
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		pkgconfig

%description devel
Development files for ndesk-dbus

%prep
%setup -q
%patch0 -p1 -b .sugar-datastore
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac

%build
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}


%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/


%files
%{_monodir}/ndesk-dbus-1.0/
%{_monogacdir}/NDesk.DBus/

%files devel
%{_libdir}/pkgconfig/ndesk-dbus-1.0.pc

%changelog
* Tue May 12 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 0.6.1a-17
- Build for Mono 4
- Use mono macros

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Dan Horák <dan[at]danny.cz> - 0.6.1a-14
- set proper ExclusiveArch
- spec cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Christian Krause <chkr@fedoraproject.org> - 0.6.1a-11
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.6.1a-8
- ExcludeArch sparc64

* Wed Jul 29 2009 Peter Gordon <peter@thecodergeek.com> - 0.6.1a-7
- Correct version number in previous %%changelog entry.
- Apply patch from Torello Querci to fix byte-alignment when reading from the
  Sugar datastore (#503151):
  + sugar-datastore.patch
- Make the pkconfig lib/lib64 munging a little bit less ugly by using the
  %%_libdir macro instead of hardcoding it per-arch.
- Move %%configure to the %%build step, not %%prep (for consistency with the
  ndesk-dbus-glib package).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.6-1a-5
- Build arch ppc64.

* Thu Feb 26 2009 David Nielsen <dnielsen@fedoraproject.org> - 0.6.1a-4
- Rebuild for stack update (#487155)

* Tue Dec 30 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.1a-3
- rebuild to get provides pkgconfig(ndesk-dbus-1.0)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.1a-2
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 David Nielsen <david@lovesunix.net> - 0.6.1a-1
- Bump to 0.6.1a

* Thu Nov  8 2007 David Nielsen <david@lovesunix.net> - 0.6.0-1
- bump to 0.6.0 
- clean up spec
- upstream is now officially renamed to ndesk-dbus as promised

* Sun Oct 21 2007 David Nielsen <david@lovesunix.net> - 0-5.2-12
- revert noarch change accord to the guidelines to accommodate
- post packaging AOT.

* Tue Oct 16 2007 David Nielsen <david@lovesunix.net> - 0.5.2-11
- Make noarch
- Don't obsolete dbus-sharp - they can coexist peacefully

* Sat Jul  7 2007 David Nielsen <david@lovesunix.net> - 0.5.2-10
- Obsolete dbus-sharp-devel as well, thanks Michael Schwendt

* Fri Jul  6 2007 David Nielsen <david@lovesunix.net> - 0.5.2-9
- And let's not be stupid and add the EVR for that provides

* Fri Jul  6 2007 David Nielsen <david@lovesunix.net> - 0.5.2-8
- Provide mono(dbus-sharp)

* Thu Jul  5 2007 David Nielsen <david@lovesunix.net> - 0.5.2-7
- Don't build on ppc64 due to mising deps, see bug 241850

* Wed Jul  4 2007 David Nielsen <david@lovesunix.net> - 0.5.2-6
- more provides, obsoletes adjustments
- %%defattr corrections
- Happy 4th of July America

* Sun Jul  1 2007 David Nielsen <david@lovesunix.net> - 0.5.2-5
- Remove mono-core from BR as it was not the cause of the mock breakage
- fix tab vs spaces
- Fix summeries
- don't use macros in changelog anymore.. upsie

* Fri Jun 29 2007 David Nielsen <david@lovesunix.net> - 0.5.2-4
- Add BuildRequires for mono-core to fix building in mock
- Fix Requires for the -devel package
- Make %%setup a bit quieter
- Made package no longer be noarch
- Added COPYING as documentation for the -devel package

* Fri Jun 26 2007 David Nielsen <david@lovesunix.net> - 0.5.2-3
- Make this significantly less hacky

* Mon Jun 25 2007 David Nielsen <david@lovesunix.net> - 0.5.2-2
- Don't be stupid .mdb files don't go in -devel

* Sat Jun 23 2007 David Nielsen <david@lovesunix.net> - 0.5.2-1
- Initial package
