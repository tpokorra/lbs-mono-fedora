%define tagname 0.3
%define relvers 0
%define tsuffix g8ed9274
%define dsuffix 31b4926

%global debug_package %{nil}

Name:           gio-sharp
Version:        %{tagname}
Release:        11%{?dist}
Summary:        C# bindings for gio

Group:          Development/Libraries
License:        MIT
URL:            http://github.com/mono/%{name}
# Releases are tarballs downloaded from a tag at github.
# They are releases, but the file is generated on the fly.
# The actual URL is: http://github.com/mono/$name/tarball/$tagname
Source0:        mono-%{name}-%{tagname}-%{relvers}-%{tsuffix}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glib2-devel
BuildRequires:  gtk-sharp2-devel
BuildRequires:  gtk-sharp2-gapi
BuildRequires:  mono-devel

# Mono only available on these:
ExclusiveArch: %mono_arches

%package devel
Summary:        Development files for gio-sharp
Requires:       gtk-sharp2-gapi
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description
C# bindings for gio

%description devel
Development files for gio-sharp

%prep
%setup -q -n mono-%{name}-%{dsuffix}

%build
NOCONFIGURE=true ./autogen-2.22.sh
%configure
make # Parallel builds don't work

%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod 644 `find $RPM_BUILD_ROOT%{_prefix}/lib -name '*.dll.config'`

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_prefix}/lib/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_datadir}/gapi-2.0/gio-api.xml

%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.3-11
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 0.3-8
- Change ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Christian Krause <chkr@fedoraproject.org> - 0.3-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sun May 08 2011 Christian Krause <chkr@fedoraproject.org> - 0.3-2
- Add mono-devel as BR for correct generation of the Requires/Provides

* Wed Apr 06 2011 Christian Krause <chkr@fedoraproject.org> - 0.3-1
- Update to release 0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.2-3
- updated the supported arch list

* Sun Oct 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.2-2
- Fix -devel requires (pkgconfig, base package)
- Disable debuginfo

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.2-1
- Initial version

