%global debug_package %{nil}
Summary: gtk sharp for Mono
Name: gtk-sharp3
Version: 2.99.3
Release: 2%{?dist}
License: GPL
Group: Development/Languages
Requires: mono-core
Requires: glib2
Requires: gtk3
Requires: libglade2
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: gettext
BuildRequires: make
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: mono-core
BuildRequires: mono-devel
BuildRequires: glib2-devel
BuildRequires: gtk3-devel
BuildRequires: libglade2-devel
BuildRequires: dos2unix
Source: gtk-sharp-%{version}.tar.xz

Provides: libmono-profiler-gui-thread-check

%description
GTK 3 sharp for Mono

%package devel
License:      GPL
Group:        Development/Libraries
Summary:      development files for GTK Sharp for Mono
Requires:     %{name} = %{version}
%description devel
Development files for GTK 3 Sharp for Mono

%prep
%setup -q -n gtk-sharp-%{version}

%build
%configure
make

%install
make install DESTDIR=%{buildroot}
#for f in %{buildroot}%{MonoPath}/bin/gapi*
#do
#  dos2unix $f
#done
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
find %{buildroot} -iname "*.exe.so" -exec rm '{}' ';'

%files
%exclude %{_libdir}/pkgconfig/
%exclude %{_libdir}/*.so
%exclude %{_libdir}/*.a
%{_bindir}/gapi3-codegen
%{_bindir}/gapi3-fixup
%{_bindir}/gapi3-parser
%{_libdir}/*.so*
%{_libdir}/*.a*
%{_libdir}/*.la*
%{_prefix}/lib/*
%{_datadir}/

%files devel
%{_libdir}/pkgconfig/
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Fri Feb 13 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-2
- Remove version requiered of mono-core 

* Fri Oct 17 2014 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-1
- initial version
