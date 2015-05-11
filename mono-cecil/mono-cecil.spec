%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

Name:           mono-cecil
Version:        0.9.6
Release:        1%{?dist}
Summary:        Library to generate and inspect programs and libraries in the ECMA CIL form
License:        MIT
URL:            http://www.mono-project.com/Cecil
Source0:        https://github.com/jbevain/cecil/archive/%{version}/cecil-%{version}.tar.gz
Patch0:         %{name}-nobuild-tests.patch
# JIT only available on these:
ExclusiveArch:  %mono_arches
BuildRequires:  mono(xbuild)
Requires:       mono-core

%global configuration net_4_5_Release

%description
Cecil is a library written by Jb Evain to generate and inspect programs and
libraries in the ECMA CIL format. It has full support for generics, and support
some debugging symbol format.

In simple English, with Cecil, you can load existing managed assemblies, browse
all the contained types, modify them on the fly and save back to the disk the
modified assembly.

Today it is used by the Mono Debugger, the bug-finding and compliance checking
tool Gendarme, MoMA, DB4O, as well as many other tools.

%prep
%setup -qn cecil-%{version}

# bundles nunit and we don't use them anyway
%patch0 -p1

%build
xbuild Mono.Cecil.sln /p:Configuration=%{configuration}

%install
mkdir -p %{buildroot}%{monogacdir}/
cd bin/%{configuration}/
gacutil -i Mono.Cecil.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Mdb.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Pdb.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
gacutil -i Mono.Cecil.Rocks.dll -f -package Mono.Cecil -root %{buildroot}/usr/lib
cd -

%files
%doc
%{_monogacdir}/Mono.Cecil*
%{_monodir}/Mono.Cecil*

%changelog
* Mon May 11 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 0.9.6-1
- Build for Mono 4
- Use mono macros
- Update to 0.9.6

* Sat Oct 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-3.20140924git6d1b7d0
- Updated
- Remove bundled nunit
- Patch Mono.Cecil.sln not to build tests

* Thu Feb 27 2014 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-2.20131105git8425de4
- Define %%monodir
- Require mono-core for monodir/gac dependency
- Define %%configuration

* Mon Jan 27 2014 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-1
- New package
