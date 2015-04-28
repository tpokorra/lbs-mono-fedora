%global debug_package %{nil}
Name:		hyena
Version:	0.5
Release:	9%{?dist}
Summary:	A library of GUI and non-GUI C sharp code
Summary(es):	Una librería para aplicaciones escritas en C#
Group:		Development/Libraries
License:	MIT
URL:		http://live.gnome.org/Hyena
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.gz
#fixed in git upstream:
Patch0:		%{name}-fix-makefile.diff
ExclusiveArch:  %{mono_arches}

BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2-devel
BuildRequires:	mono-data
BuildRequires:	mono-nunit-devel >= 2.4.7

Requires:	gtk-sharp2
Requires:	mono-nunit

%description
This is a library of useful GUI and non-GUI C sharp code, originally used in 
Banshee.

%description -l es
Esta es una librería útil para escribir aplicaciones en C# usada
originalmente en Banshee.

%package devel
Summary:	Development files for %{name}
Summary(es):	Archivos de desarrollo de %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development package for %{name}

%description devel -l es
Paquete de desarrollo para %{name}

%prep
%setup -q 
%patch0 -p1

%build
%configure 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

chmod a-x %{buildroot}%{_libdir}/hyena/*.config

%files
%doc NEWS README COPYING
%{_libdir}/%{name}

%files devel
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 07 2012 Dan Horák <dan[at]danny.cz> - 0.5-5
- set ExclusiveArch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 <ismael@olea.org> 0.5-3
- applying recomendations from https://bugzilla.redhat.com/show_bug.cgi?id=834548#c2 

* Thu Jun 21 2012 <ismael@olea.org> 0.5-2
- minor spec cleaning

* Mon Mar 21 2011 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.5-1
- Update to version 0.5
- Spec summary and description translation to spanish

* Wed Jul 07 2010 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.3-1
- Update to version 0.3
- Add development package

* Fri Oct 23 2009 Ryan Lerch <rlerch@redhat.com> 0.2-1
- Initial RPM
