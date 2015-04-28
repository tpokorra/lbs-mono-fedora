Name:		webkit-sharp
Version:	0.3
Release:	14%{?dist}
Summary:	.NET bindings for WebKit

License:	MIT
URL:		http://www.mono-project.com/Main_Page
Source0:	http://origin-download.mono-project.com/sources/webkit-sharp/%{name}-%{version}.tar.bz2
# https://bugzilla.redhat.com/show_bug.cgi?id=658502
Patch1:		webkit-sharp-0.3-dllmap.patch

Requires:	webkitgtk
BuildRequires:	webkitgtk-devel
BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2-devel
BuildRequires:	gtk-sharp2-gapi
BuildRequires:	monodoc-devel

ExclusiveArch: %mono_arches

#https://fedoraproject.org/wiki/Packaging:Mono#Empty_debuginfo
%global debug_package %{nil}


%description
WebKit-sharp is .NET bindings for the WebKit rendering engine.


%package devel
Summary:	Development files for WebKit-sharp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig


%description devel
Development files for WebKit-sharp


%prep
%setup -q
# update for new webkit library name
%patch1 -p1 -b .dllmap
sed -i -e 's!@libdir@!${exec_prefix}/lib!g' sources/webkit-sharp.pc.in


%build
%configure
make


%install
make DESTDIR=%{buildroot} install


%files
%doc COPYING README
%{_prefix}/lib/mono/


%files devel
%{_libdir}/pkgconfig/webkit-sharp-1.0.pc
%{_prefix}/lib/monodoc/sources/webkit-sharp*


%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.3-14
- use %%mono_arches

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 27 2013 Nikos Roussos <comzeradd@fedoraproject.org> 0.3-10
- Clean up package for F19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 0.3-8
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jun 03 2011 Paul Whalen <paul.whalen@senecac.on.ca> - 0.3-7
- Added arm macro to ExclusiveArch

* Mon Mar 28 2011 Christian Krause <chkr@fedoraproject.org> - 0.3-6
- Rebuilt against mono 2.10
- Minor spec file cleanup

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 27 2010 Dan Horák <dan[at]danny.cz> - 0.3-4
- update dll mapping for new webkitgtk (#658502)
- sync ExclusiveArch list with mono

* Sun Oct 31 2010 Christian Krause <chkr@fedoraproject.org> - 0.3-3
- Rebuild again to create correct requires/provides capabilities

* Sat Oct 09 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 0.3-2
- Rebuild for mono-2.8

* Thu Dec 17 2009 Paul Lange <palango@gmx.de> - 0.3-1
- Update to version 0.3

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 0.2-6
- build for sparcv9 s390 s390x

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Paul Lange <palango@gmx.de> - 0.2-4
- Fix supported archs

* Sun Jun 14 2009 Paul Lange <palango@gmx.de> - 0.2-3
- Fix wrong webkitgtk link and missing dependency (#500654)

* Mon May 25 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.2-2
- Build arch ppc64.

* Sat Feb 21 2009 David Nielsen <gnomeuser@gmail.com> - 0.2-1
- Initial package
