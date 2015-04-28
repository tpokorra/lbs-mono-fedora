%define tagname GKEYFILE_SHARP_0_1
%define relvers 0
%define tsuffix g07a401a
%define dsuffix 662c5c1

%global debug_package %{nil}

Name:           gkeyfile-sharp
Version:        0.1
Release:        16%{?dist}
Summary:        C# bindings for glib2's keyfile implementation

Group:          Development/Libraries
License:        LGPLv2
URL:            http://github.com/mono/%{name}
# Releases are tarballs downloaded from a tag at github.
# They are releases, but the file is generated on the fly.
# The actual URL is: http://github.com/mono/$name/tarball/$tagname
Source0:        mono-%{name}-%{tagname}-%{relvers}-%{tsuffix}.tar.gz
# Upstream patch to fix DllImport name of libglib (BZ 692784)
# https://github.com/mono/gkeyfile-sharp/commit/1a1adb8ec4149b4a0a8e55db0e3baa172cbd2c3f
Patch1:         0001-Change-glib-DllImports-to-libglib-2.0-0.dll.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glib2-devel
BuildRequires:  gtk-sharp2-devel
BuildRequires:  gtk-sharp2-gapi
BuildRequires:  mono-devel

# Mono only available on these:
ExclusiveArch: %mono_arches

%package devel
Summary:        Development files for gkeyfile-sharp
Requires:	pkgconfig
Requires:       %{name} = %{version}-%{release}

%description
C# bindings for glib2's keyfile implementation

%description devel
Development files for gkeyfile-sharp

%prep
%setup -q -n mono-%{name}-%{dsuffix}
%patch1 -p1 -b dllimport-fix

%build
./autogen.sh
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod 644 `find $RPM_BUILD_ROOT%{_prefix}/lib/mono -name '*.dll.config'`
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/mono/%{name}/%{name}.dll.config

mkdir -p %{buildroot}%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv %{buildroot}%{_prefix}/lib/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE.LGPL NEWS
%{_prefix}/lib/mono/gac/%{name}
%{_prefix}/lib/mono/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.1-16
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 0.1-13
- Changing ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Christian Krause <chkr@fedoraproject.org> - 0.1-8
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Sun May 08 2011 Christian Krause <chkr@fedoraproject.org> - 0.1-7
- Add mono-devel as BR for correct generation of the Requires/Provides

* Sun May 08 2011 Christian Krause <chkr@fedoraproject.org> - 0.1-6
- Fix DllNotFoundException by adding upstream patch (BZ 692784)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Dan Horák <dan[at]danny.cz> - 0.1-4
- updated the supported arch list

* Mon Oct 04 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-3
- Fix directory ownership

* Sun Oct 03 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-2
- Fix -devel requires (pkgconfig, base package)
- Disable debuginfo

* Wed Sep 29 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 0.1-1
- Initial version

