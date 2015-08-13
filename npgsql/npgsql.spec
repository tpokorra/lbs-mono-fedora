%global debug_package %{nil}
%if 0%{?el6}
%global mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
%if 0%{?rhel}%{?el6}%{?el7}
# see https://fedorahosted.org/fpc/ticket/395
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

Name:       npgsql
Version:    3.0.0
Release:    1%{?dist}
Summary:    A .Net Data Provider for PostgreSQL

Group:      Development/Languages
License:    MIT
URL:        http://npgsql.projects.pgfoundry.org/
Source0:    https://github.com/%{name}/%{name}/archive/v3.0.0.tar.gz#/%{name}-%{version}.tar.gz
Source1:    npgsql.pc

BuildRequires:  mono-devel
BuildRequires:  nuget

ExclusiveArch: %{mono_arches}

%description
Npgsql is a .Net Data Provider for PostgreSQL.
It allows you to connect and interact with PostgreSQL server using .NET

%package        devel
Summary:        Development files for %{name}
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%prep
%setup -qn %{name}-%{version}
nuget restore Npgsql2015.sln

%build
xbuild /tv:4.0 src/Npgsql/Npgsql.csproj

%install
%{__mkdir_p} %{buildroot}/%{_monogacdir}/
%{__mkdir_p} %{buildroot}/%{_monodir}/npgsql/
%{__mkdir_p} %{buildroot}/%{_libdir}/pkgconfig

install -p -m0644 %SOURCE1 %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 src/Npgsql/bin/Debug/Npgsql.dll %{buildroot}%{_monodir}/npgsql/

gacutil -i %{buildroot}%{_monodir}/npgsql/Npgsql.dll -f -package npgsql -root %{buildroot}/%{_prefix}/lib

%files
%doc README.md
%license LICENSE.txt
%{_monogacdir}/*
%dir %{_monodir}/npgsql
%{_monodir}/npgsql/Npgsql.dll

%files devel
%{_libdir}/pkgconfig/npgsql.pc

%changelog
* Thu Aug 13 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Wed May 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.2.3-2
- Use global insted define
- Use tv xbuild parameter insted sed to build with mono 4

* Thu Nov 21 2013 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.2.3-1
- Initial packaging
