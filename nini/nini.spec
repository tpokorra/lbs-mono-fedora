%global debug_package %{nil}
%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://lists.fedoraproject.org/pipermail/packaging/2011-May/007762.html
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

Name:           nini
Version:        1.1.0
Release:        7%{?dist}
Summary:        .NET configuration library
License:        MIT
URL:            http://nini.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/%{name}/Nini/%{version}/Nini-%{version}.zip
Source1:        nini.pc
BuildRequires:  mono-devel

ExclusiveArch: %{mono_arches}

%description
Nini is an .NET configuration library which designed to help build highly
configurable applications quickly. Nini provides a solution that attempts to
eliminate the above problems. It provides a large feature set that gives you
functionality that you will use in every phase of your project, from concept
to mature product. This is accomplished through a simple, yet flexible, API
that provides an abstraction over the underlying configuration sources.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains a pkgconfig file for developing 
applications that use %{name}.

%prep
%setup -qn Nini

%build
cd Source
# Generated and sorted from nant build-mono.
# Native failed with: 'mcs.bat' failed to start.
# So we need mcs to build it manually.
# Also we should use system pki snk key.
ln -s %{_sysconfdir}/pki/mono/mono.snk %{name}.snk
mcs -t:library -keyfile:%{name}.snk -r:System,System.Data,System.Xml -out:%{name}.dll {AssemblyInfo,Ini/*,Config/*,Util/*}.cs

%install
mkdir -p %{buildroot}%{_monogacdir}/
mkdir -p %{buildroot}%{_datadir}/pkgconfig
gacutil -i Source/%{name}.dll -f -package %{name} -root %{buildroot}%{_prefix}/lib
install -pm644 %{S:1} %{buildroot}%{_datadir}/pkgconfig/

%files
%doc {CHANGELOG,LICENSE,README}.txt
%doc Docs/*
%{_monogacdir}/%{name}/
%{_monodir}/%{name}/

%files devel
%{_datadir}/pkgconfig/nini.pc

%changelog
* Thu May 14 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 1.1.0-7
- Build for Mono 4
- Use mono macros

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Dan Horák <dan[at]danny.cz> - 1.1.0-4
- set ExclusiveArch

* Fri Dec 13 2013 Christopher Meng <rpm@cicku.me> - 1.1.0-3
- No noarch.

* Thu Nov 21 2013 Christopher Meng <rpm@cicku.me> - 1.1.0-2
- Conform to Fedora Mono Packaging Guideline by using system shipped pki.

* Thu Apr 04 2013 Christopher Meng <rpm@cicku.me> - 1.1.0-1
- Initial Package.
