Name:		mono-immutablecollections
Version:	4.2
Release:	1%{?dist}
License:	MIT-X11
URL:		https://github.com/mono/ImmutableCollections
Summary:	An implementation of System.Collections.Immutable
Group: 		Development/Libraries

%define gitrevision 4f149018cfba40c89c5b5cd62ccb8efc7c39c759
Source0:	https://github.com/mono/ImmutableCollections/archive/%{gitrevision}.tar.gz
Source1:        %{name}.pc
BuildRequires:	mono-devel
BuildRequires:	autoconf automake libtool
Requires:	mono-core

# Mono only available on these:
ExclusiveArch: %mono_arches

%define debug_package %{nil}
%define configuration Release

%description

This is a MIT-X11 implementation which tries to implement the interfaces from the nuget package: https://nuget.org/packages/Microsoft.Bcl.Immutable

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%prep
%setup -q -n ImmutableCollections-%{gitrevision}

# drop the unit tests, still depending on NUnit2
sed -i 's#.*E7523A9A-BF2B-420D-B67F-B73AA98C6061.*##g' System.Collections.Immutable.sln # UnitTests

%build
xbuild System.Collections.Immutable.sln /p:Configuration=%{configuration}

%install
cd bin/%{configuration}
%{__mkdir_p} %{buildroot}%{_monodir}/System.Collections.Immutable
%{__install} -m0755 System.Collections.Immutable.dll %{buildroot}%{_monodir}/System.Collections.Immutable
# no strong name for the assembly, cannot install to gac
#gacutil -i %{buildroot}%{_monodir}/System.Collections.Immutable/System.Collections.Immutable.dll -package System.Collections.Immutable -root %{buildroot}%{_monodir}/../
mkdir -p %{buildroot}/%{_libdir}/pkgconfig/
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/

%files
#%{_monogacdir}/System.Collections.Immutable*
%{_monodir}/System.Collections.Immutable/*.dll

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Aug 10 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.2-1
- initial version
