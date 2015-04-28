%define tagname 2.14.0
%define relvers 0
%define tsuffix ga2ff3c5
%define dsuffix 19023b6

%global debug_package %{nil}

Name:           gtk-sharp-beans
Version:        %{tagname}
Release:        14%{?dist}
Summary:        C# bindings for GTK+ API not included in GTK#

Group:          Development/Libraries
License:        LGPLv2
URL:            http://github.com/mono/%{name}
# Releases are tarballs downloaded from a tag at github.
# They are releases, but the file is generated on the fly.
# The actual URL is: http://github.com/mono/$name/tarball/$tagname
Source0:        mono-%{name}-%{tagname}-%{relvers}-%{tsuffix}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  mono-devel
BuildRequires:  gio-sharp-devel
BuildRequires:  gtk-sharp2-devel
BuildRequires:  gtk-sharp2-gapi

# Mono only available on these:
ExclusiveArch: %mono_arches

%package devel
Summary:        Development files for gtk-sharp-beans
Requires:	pkgconfig
Requires:       %{name} = %{version}-%{release}

%description
C# bindings for GTK+ API not included in GTK#

%description devel
Development files for gtk-sharp-beans

%prep
%setup -q -n mono-%{name}-%{dsuffix}

%build
NOCONFIGURE=true ./autogen.sh
%configure
make #%{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_prefix}/lib/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}-2.0.pc

%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 2.14.0-14
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 2.14.0-11
- Changing ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 01 2012 Christian Krause <chkr@fedoraproject.org> - 2.14.0-6
- Add mandatory BR mono-devel

* Wed Oct 26 2011 Christian Krause <chkr@fedoraproject.org> - 2.14.0-5
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Dan Horák <dan[at]danny.cz> - 2.14.0-3
- updated the supported arch list

* Sun Oct 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.14.0-2
- Fix -devel requires (pkgconfig, base package)
- Disable debuginfo

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.14.0-1
- Initial version

