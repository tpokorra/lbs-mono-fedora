%global debug_package %{nil}
Summary:        GTK+ 3 and GNOME 3 bindings for Mono
Name:           gtk-sharp3
Version:        2.99.3
Release:        6%{?dist}
License:        LGPLv2
Group:          System Environment/Libraries

BuildRequires:  mono-devel gtk3-devel libglade2-devel monodoc
BuildRequires:  automake, libtool
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: glib2-devel
BuildRequires: libglade2-devel

URL:            http://www.mono-project.com/GtkSharp
Source:         http://ftp.acc.umu.se/pub/gnome/sources/gtk-sharp/2.99/gtk-sharp-%{version}.tar.xz

Provides:       libmono-profiler-gui-thread-check

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
Summary:        Glib and GObject C source parser and C generator for the creation and maintenance of managed bindings for Mono and .NET
Requires:       perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX

%description gapi
This package provides developer tools for the creation and
maintenance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk.

%package devel
Summary:        Files needed for developing with gtk-sharp3
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package provides the necessary development libraries and headers
for writing gtk-sharp3 applications.

%package doc
Group:          Documentation
Summary:        Gtk# 3 documentation
Requires:       %{name} = %{version}-%{release}
Requires:       monodoc

%description doc
This package provides the Gtk# 3 documentation for monodoc.

%prep
%setup -q -n gtk-sharp-%{version}

%build
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.ac
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
%configure
make %{?_smp_flags}

%install
%make_install DESTDIR=%{buildroot}

find %{buildroot} -iname "*.dll.so" -delete
find %{buildroot} -iname "*.exe.so" -delete
#Remove libtool archive
find %{buildroot} -name \*.*a -delete

%files
%defattr(-,root,root,-)
%doc README AUTHORS
%license COPYING
%exclude %{_libdir}/*.so
%{_libdir}/*.so*
%{_monogacdir}/*
%{_monodir}/gtk-sharp-3.0

%files gapi
%defattr(-,root,root,-)
%{_bindir}/gapi3-codegen
%{_bindir}/gapi3-fixup
%{_bindir}/gapi3-parser
%{_prefix}/lib/gapi-3.0/gapi_codegen.exe
%{_prefix}/lib/gapi-3.0/gapi-fixup.exe
%{_prefix}/lib/gapi-3.0/gapi-parser.exe
%{_prefix}/lib/gapi-3.0/gapi_pp.pl
%{_prefix}/lib/gapi-3.0/gapi2xml.pl
%{_datadir}/gapi-3.0
%{_libdir}/pkgconfig/gapi-3.0.pc

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*-sharp-3.0.pc
%{_libdir}/pkgconfig/gtk-dotnet-3.0.pc
%{_libdir}/*.so

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/*

%changelog
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
