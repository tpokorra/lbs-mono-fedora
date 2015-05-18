%if 0%{?rhel}%{?el7}
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_prefix}/lib/mono/gac
%endif

%global debug_package %{nil}
%global _docdir_fmt %{name}

Name:           notify-sharp3
Version:        3.0.3
Release:        1%{?dist}
Summary:        A C# implementation for Desktop Notifications

Group:          System Environment/Libraries
License:        MIT
URL:            https://www.meebey.net/projects/notify-sharp
Source0:        https://www.meebey.net/projects/notify-sharp/downloads/notify-sharp-%{version}.tar.gz

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
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for notify-sharp

%package doc
Summary:        Documentation files for notify-sharp
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       monodoc
BuildArch:      noarch

%description doc
Documentation files for notify-sharp

%prep
%setup -qn notify-sharp-%{version}

%build
sed -i "s#gmcs#mcs#g" configure.ac
autoreconf --install
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}

%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

%files
%doc NEWS README AUTHORS
%license COPYING
%{_monogacdir}/notify-sharp/
%{_monodir}/notify-sharp*/

%files devel
%{_libdir}/pkgconfig/notify-sharp*.pc

%files doc
%{_prefix}/lib/monodoc/sources/*

%changelog
* Mon Apr 20 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.0.3-1
- Packaging version 3
