%define debug_package %{nil}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
%if 0%{?rhel}%{?el6}%{?el7}
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_prefix}/lib/mono/gac
%endif

Name:           notify-sharp
Version:        3.0.3
Release:        1%{?dist}
Summary:        A C# implementation for Desktop Notifications

Group:          System Environment/Libraries
License:        MIT
URL:            https://www.meebey.net/projects/notify-sharp
Source0:        https://www.meebey.net/projects/notify-sharp/downloads/%{name}-%{version}.tar.gz

BuildRequires:  mono-devel, gtk-sharp3-devel, gnome-sharp-devel, dbus-sharp-glib-devel
BuildRequires:  autoconf, automake, libtool

BuildRequires:  monodoc-devel
# Mono only available on these:
ExclusiveArch: %{mono_arches}

%description
notify-sharp is a C# client implementation for Desktop Notifications,
i.e. notification-daemon. It is inspired by the libnotify API.

Desktop Notifications provide a standard way of doing passive pop-up
notifications on the Linux desktop. These are designed to notify the
user of something without interrupting their work with a dialog box
that they must close. Passive popups can automatically disappear after
a short period of time.

%package devel
Summary:        Development files for notify-sharp
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for notify-sharp

%package doc
Summary:        Documentation files for notify-sharp
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       monodoc

%description doc
Documentation files for notify-sharp

%prep
%setup -qn %{name}-%{version}

%build
sed -i "s#gmcs#mcs#g" configure.ac
autoreconf --install
%configure --libdir=%{_prefix}/lib
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README AUTHORS
%{_monogacdir}/notify-sharp/
%{_monodir}/notify-sharp*/

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/notify-sharp*.pc

%files doc
%defattr(-,root,root,-)
%{_prefix}/lib/monodoc/sources/*

%changelog
* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.0.3-1
- Packaging version 3
