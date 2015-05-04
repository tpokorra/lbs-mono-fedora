%global debug_package %{nil}
%define snapshot 20150421
Name:           monodevelop-git-latest
Version:        6.0
Release:        1.%{snapshot}%{?dist}
Summary:        A full-featured IDE for Mono and Gtk#

Group:          Development/Tools
License:        GPLv2+
URL:            http://monodevelop.com/
Source0:        https://jenkins.mono-project.com/view/Packaging-MonoDevelop/job/build-source-tarball-monodevelop/lastSuccessfulBuild/artifact/%{name}.tar.bz2
Patch0:         monodevelop-nunit-unbundle.patch
Patch1:         monodevelop-avoidgiterrors.patch
BuildRequires:  mono-devel >= 3.0.4
BuildRequires:  mono-addins-devel >= 0.6
BuildRequires:  nunit-devel
BuildRequires:  monodoc-devel
BuildRequires:  gnome-desktop-sharp-devel
BuildRequires:  desktop-file-utils intltool
BuildRequires:  nuget dos2unix
Requires:       mono-core >= 3.0.4
Requires:       mono-addins >= 0.6
# Using system nunit, but dependency not automatically picked up by RPM
#Requires:       mono(nunit.core)
#Requires:       mono(nunit.framework)
Requires:       nunit
Requires:       gnome-desktop-sharp
Requires:       subversion monodoc
Requires:       hicolor-icon-theme shared-mime-info
Requires:       gtk-sharp2-devel
Conflicts:      monodevelop < %{version}

# Mono only available on these:
ExclusiveArch: %{mono_arches}

%description
This package provides MonoDevelop, a full-featured IDE for Mono with
syntax coloring, code completion, debugging, project management and
support for C sharp, Visual Basic.NET, Java, Boo, Nemerle and MSIL.


%package        devel
Summary:        Development files for monodevelop
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
 
%description devel
Development files for %{name}.


%prep
%setup -qn %{name}
%patch0 -p1 -b .unbundle
%patch1 -p1

#mozroots --import --sync

#%patch0 -p0
#nuget restore
# Delete shipped *.dll files
#find -name '*.dll' -exec rm -f {} \;

%build
sed -i "s#gmcs#mcs#g" configure
sed -i "s#gmcs#mcs#g" configure.in
sed -i "s#dmcs#mcs#g" configure
sed -i "s#dmcs#mcs#g" configure.in
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
%configure --enable-git --disable-update-mimedb --disable-update-desktopdb

make

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
                     --dir $RPM_BUILD_ROOT%{_datadir}/applications \
                     --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/monodevelop.desktop

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig/* $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/m*
%{_prefix}/lib/monodevelop
%{_mandir}/man1/m*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mime/packages/monodevelop.xml

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/monodevelop*.pc

%changelog
* Fri Apr 17 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 6.0-1
- Packaging from jenkins build.

* Fri Jan 09 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.8-2
- Packaging from jenkins build.
