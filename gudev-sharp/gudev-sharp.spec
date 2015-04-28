%define tagname GUDEV_SHARP_0_1
%define relvers 0
%define tsuffix g2c53e2f
%define dsuffix cd3e7df

%global debug_package %{nil}

Name:           gudev-sharp
Version:        0.1
Release:        15%{?dist}
Summary:        C# bindings for gudev

Group:          Development/Libraries
License:        LGPLv2
URL:            http://github.com/mono/%{name}
# Releases are tarballs downloaded from a tag at github.
# They are releases, but the file is generated on the fly.
# The actual URL is: http://github.com/mono/$name/tarball/$tagname
Source0:        mono-%{name}-%{tagname}-%{relvers}-%{tsuffix}.tar.gz

BuildRequires:  mono-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libgudev1-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk-sharp2-devel
BuildRequires:  gtk-sharp2-gapi

# Mono only available on these:
ExclusiveArch: %mono_arches

%package devel
Summary:        Development files for gudev-sharp
Requires:	pkgconfig
Requires:       %{name} = %{version}-%{release}

%description
C# bindings for gudev

%description devel
Development files for gudev-sharp

%prep
%setup -q -n mono-%{name}-%{dsuffix}

%build
sed -i 's|^\./configure.*||' autogen.sh # Remove the configure step, we'll do it manually
./autogen.sh
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod 644 `find $RPM_BUILD_ROOT%{_prefix}/lib/mono -name '*.dll.config'`
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/mono/%{name}-1.0/%{name}.dll.config

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE.LGPL NEWS
%{_prefix}/lib/mono/gac/%{name}
%{_prefix}/lib/mono/%{name}-1.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}-1.0.pc

%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.1-15
- use %%mono_arches 

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 0.1-12
- Changing ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 01 2012 Christian Krause <chkr@fedoraproject.org> - 0.1-7
- Add mandatory BR mono-devel

* Mon Oct 31 2011 Christian Krause <chkr@fedoraproject.org> - 0.1-6
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.1-4
- updated the supported arch list

* Mon Oct 04 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-3
- Fix directory ownership

* Sun Oct 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-2
- Fix -devel requires (pkgconfig, base package)
- Disable debuginfo

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-1
- Initial version

