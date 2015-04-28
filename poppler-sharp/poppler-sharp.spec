%global debug_package %{nil} 
Name:		poppler-sharp
Version:	0.0.3
Release:	6%{?dist}
Summary:	C sharp Bindings for Poppler
Summary(es):	Enlaces C# para Poppler
Group:		Development/Libraries
License:	GPLv2+
URL:		http://www.github.com/jacintos/poppler-sharp
Source0:	http://github.com/downloads/jacintos/%{name}/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	mono-devel
BuildRequires:	gtk-sharp2-gapi
BuildRequires:	gtk-sharp2-devel
BuildRequires:	poppler-glib-devel

Requires:	poppler

%description
Generates managed bindings for Poppler using the GAPI tools

%description -l es
Genera los vínculos administrados usando las herramientas GAPI

%package devel
Summary:	Development files for %{name}
Summary(es):	Archivos de desarrollo para %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development package for %{name}

%description devel -l es
Paquete de desarrollo para %{name}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/%{name}.dll*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 8 2012 Ismael Olea <ismael@olea.org> 0.0.3-2
- spec tuning

* Thu Jun 21 2012 Ismael Olea <ismael@olea.org> 0.0.3-1
- update to 0.0.3

* Mon Aug 29 2011 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.0.2-2
- Fix libpoppler-glib missing

* Fri Aug 26 2011 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.0.2-1
- Update to upstream version

* Thu Mar 22 2011 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.0.1-3
- Translate spec summary and description to spanish
- Add poppler-glib-devel dependency

* Wed Oct 04 2010 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.0.1-2
- Patch .pc package for work correctly on x86_64
- Correct license according to http://github.com/jacintos/poppler-sharp

* Wed Jul 07 2010 Claudio Rodrigo Pereyra Diaz <claudiorodrigo@pereyradiaz.com.ar> 0.0.1-1
- Initial packaging
