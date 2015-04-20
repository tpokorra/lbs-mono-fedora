%define debug_package %{nil}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Summary: C# bindings for D-Bus glib main loop integration
Name: dbus-sharp-glib
Version: 0.5.0
Release: 12%{?dist}
URL: http://mono.github.com/dbus-sharp/
Source0: https://github.com/downloads/mono/dbus-sharp/%{name}-%{version}.tar.gz
License: MIT
Group: System Environment/Libraries
BuildRequires: mono-devel
BuildRequires: dbus-sharp-devel >= 1:0.7.0
# Mono only available on these:
ExclusiveArch: %mono_arches

%description
C# bindings for D-Bus glib main loop integration

%package devel
Summary: Development files for D-Bus Sharp
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for D-Bus Sharp development.

%prep
%setup -q

%build
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure --libdir=%{_prefix}/lib
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%files
%doc COPYING README
%{_prefix}/lib/mono/dbus-sharp-glib-1.0
%{_prefix}/lib/mono/gac/dbus-sharp-glib

%files devel
%{_libdir}/pkgconfig/dbus-sharp-glib-1.0.pc

%changelog
* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.5.0-12
- Define mono_arches for epel6

* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 0.5.0-11
- Build for mono 4

* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.5.0-10
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Brent Baude <baude@us.ibm.com> - 0.5.0-7
- Changed ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Christian Krause <chkr@fedoraproject.org> - 0.5.0-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Christian Krause <chkr@fedoraproject.org> - 0.5.0-1
- Initial spec file

