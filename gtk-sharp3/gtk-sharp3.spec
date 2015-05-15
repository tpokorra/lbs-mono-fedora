%if 0%{?rhel}%{?el7}
# see https://fedorahosted.org/fpc/ticket/395
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

%global debug_package %{nil}
%global _docdir_fmt %{name}

Summary:        GTK+ 3 and GNOME 3 bindings for Mono
Name:           gtk-sharp3
Version:        2.99.3
Release:        10%{?dist}
License:        LGPLv2
Group:          System Environment/Libraries

BuildRequires:  mono-devel gtk3-devel libglade2-devel monodoc
BuildRequires:  automake, libtool
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel

URL:            http://www.mono-project.com/docs/gui/gtksharp/
Source:         http://ftp.acc.umu.se/pub/gnome/sources/gtk-sharp/2.99/gtk-sharp-%{version}.tar.xz

# Mono only available on these:
ExclusiveArch:  %{mono_arches}

%description
This package provides a library that allows you to build
fully native graphical GNOME applications using Mono. Gtk#
is a binding to version 3 of GTK+, the cross platform user interface
toolkit used in GNOME. It includes bindings for Gtk, Atk,
Pango, Gdk.

%package gapi
Group:          Development/Languages
Summary:        Tools for creation and maintenance managed bindings for Mono and .NET

%description gapi
This package provides developer tools for the creation and
maintenance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk.

%package devel
Summary:        Files needed for developing with gtk-sharp3
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package provides the necessary development libraries and headers
for writing gtk-sharp3 applications.

%package doc
Group:          Documentation
Summary:        Gtk# 3 documentation
Requires:       monodoc
BuildArch:      noarch

%description doc
This package provides the Gtk# 3 documentation for monodoc.

%prep
%setup -q -n gtk-sharp-%{version}

# https://fedorahosted.org/FedoraReview/wiki/AutoTools
sed -i "s#AM_PROG_LIBTOOL#LT_INIT#g" configure.ac

# Fixes for build with Mono 4
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
%configure
make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -iname "*.dll.so" -delete
find %{buildroot} -iname "*.exe.so" -delete
#Remove libtool archive
find %{buildroot} -name \*.a -delete
find %{buildroot} -name \*.la -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%license COPYING
%exclude %{_libdir}/*.so
%{_libdir}/*.so*
%{_monogacdir}/*
%{_monodir}/gtk-sharp-3.0

%files gapi
%{_bindir}/gapi3-codegen
%{_bindir}/gapi3-fixup
%{_bindir}/gapi3-parser
%dir %{_prefix}/lib/gapi-3.0
%{_prefix}/lib/gapi-3.0/gapi_codegen.exe
%{_prefix}/lib/gapi-3.0/gapi-fixup.exe
%{_prefix}/lib/gapi-3.0/gapi-parser.exe
%{_prefix}/lib/gapi-3.0/gapi_pp.pl
%{_prefix}/lib/gapi-3.0/gapi2xml.pl
%{_datadir}/gapi-3.0
%{_libdir}/pkgconfig/gapi-3.0.pc

%files devel
%{_libdir}/pkgconfig/*-sharp-3.0.pc
%{_libdir}/pkgconfig/gtk-dotnet-3.0.pc
%{_libdir}/*.so

%files doc
%{_prefix}/lib/monodoc/sources/*

%changelog
* Fri May 15 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-10
- Fix url
- Use global insted define for rhel and epel7
- Replace old autotool macros in configure.ac

* Mon May 11 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-9
- Remove virtual provides

* Tue May 05 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-8
- Add /sbin/ldconfig in post and postun
- Remove requiere in gapi

* Tue May 05 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-7
- gtk-sharp-3-doc not requiered gtk-sharp-3 and move to noarch
- gapi summary less than 70 characters
- Fixed for mono 4 moved to prep
- Define _monodir and _monogacdir for rhel and epel7
- Spec clean up

* Mon May 04 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-6
- Use same subpackage criteria as gtk-sharp2
- Spec clean up
- Use license macro

* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-5
- Add mono_arches

* Thu Apr 16 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-4
- Use mcs insted gmcs

* Thu Apr 16 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-3
- Build for Mono 4

* Fri Feb 13 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-2
- Remove version requiered of mono-core

* Fri Oct 17 2014 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.99.3-1
- initial version
