%if 0%{?rhel}%{?el6}%{?el7}
%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif
# see https://fedorahosted.org/fpc/ticket/395
%define _monodir %{_prefix}/lib/mono
%define _monogacdir %{_monodir}/gac
%endif

Name:           OpenTK
%global         lowercase opentk
Version:        1.1
%global         snapshot 4c
Release:        3.%{snapshot}%{?dist}
Summary:        C# library that wraps OpenGL, OpenCL and OpenAL
# See License.txt for more information
License:        MIT and BSD
URL:            http://www.%{lowercase}.com/
Source0:        https://github.com/%{lowercase}/%{lowercase}/archive/%{version}-%{snapshot}.tar.gz
# JIT only available on these:
ExclusiveArch:  %mono_arches
%global         cecilver 0.9.6.0
BuildRequires:  mono(xbuild)
BuildRequires:  mono(gacutil)
BuildRequires:  mono(Mono.Cecil) = %{cecilver}
BuildRequires:  mono(Mono.Cecil.Mdb) = %{cecilver}
BuildRequires:  mono(Mono.Cecil.Pdb) = %{cecilver}
BuildRequires:  mono(Mono.Cecil.Rocks) = %{cecilver}
BuildRequires:  libgdiplus-devel

BuildRequires:  dos2unix
# https://bugzilla.redhat.com/show_bug.cgi?id=1032883
Provides:       %{lowercase} = %{version}-%{release}

%description
The Open Toolkit is an advanced, low-level C# library that wraps OpenGL, OpenCL
and OpenAL. It is suitable for games, scientific applications and any other
project that requires 3d graphics, audio or compute functionality.

%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       %{lowercase}-doc = %{version}-%{release}

%description    doc
The Open Toolkit is an advanced, low-level C# library that wraps OpenGL, OpenCL
and OpenAL. It is suitable for games, scientific applications and any other
project that requires 3d graphics, audio or compute functionality.

This package contains the manual and several examples.

%prep
%setup -q -n %{lowercase}-%{version}-%{snapshot}
rm -rf Dependencies

for FILE in Documentation/License.txt Source/Examples/Data/Shaders/Parallax_FS.glsl; do
  iconv -f iso8859-1 -t utf-8 $FILE > $FILE.conv && mv -f $FILE.conv $FILE
done

# Shouldn't harm the correct ones
find Source/Examples -type f -exec dos2unix {} \;
echo '/* Nothing here */' >> Source/Examples/OpenGLES/SimpleWindow20.cs

# Use Mono.Cecil %%{cecilver}
cd Source/Generator.Rewrite
sed -i 's/Include="Mono.Cecil"/Include="Mono.Cecil, version=%{cecilver}"/' Generator.Rewrite.csproj
sed -i 's/Include="Mono.Cecil.Mdb"/Include="Mono.Cecil.Mdb, version=%{cecilver}"/' Generator.Rewrite.csproj
cd -

#Fixes for Mono 4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;


%build
export LANG=en_US.utf8 # Otherwise there are errors
xbuild %{name}.sln /p:Configuration=Release
chmod -x Source/Examples/obj/Release/Examples.exe

%install
mkdir -p %{buildroot}/%{_monogacdir}
gacutil -i Binaries/OpenTK/Release/%{name}.dll -f -package %{name} -root %{buildroot}/usr/lib
gacutil -i Binaries/OpenTK/Release/%{name}.Compatibility.dll -f -package %{name} -root %{buildroot}/usr/lib
gacutil -i Binaries/OpenTK/Release/%{name}.GLControl.dll -f -package %{name} -root %{buildroot}/usr/lib

%files
%doc Documentation/*.txt
%{_monogacdir}/%{name}*
%{_monodir}/%{name}

%files doc
%doc Source/Examples

%changelog
* Mon May 11 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 1.1-3.4c
- Add libgdiplus-devel as buildrequires

* Mon May 11 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 1.1-2.4c
- Build for Mono 4
- Use mono macros

* Sat Oct 25 2014 Miro Hrončok <mhroncok@redhat.com> - 1.1-1.4c
- New post release 1.1-4c
- Remove no longer existing PDF form the doc

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Miro Hrončok <mhroncok@redhat.com> - 1.1-0.1.b1
- Version 1.1 beta1
- Provide opentk

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-7.20130108svn3126
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-6.20130108svn3126
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Miro Hrončok <mhroncok@redhat.com> - 0.0-5.20130108svn3126
- Split the doc package
- Add examples to the docs

* Thu Jan 10 2013 Miro Hrončok <mhroncok@redhat.com> - 0.0-4.20130108svn3126
- New revision

* Mon Dec 31 2012 Miro Hrončok <miro@hroncok.cz> - 0.0-3.20120523svn3125
- Renamed from %{lowercase} to OpenTK

* Mon Dec 31 2012 Miro Hrončok <miro@hroncok.cz> - 0.0-2.20120523svn3125
- The package now owns /usr/lib/mono/OpenTK directory

* Sun Dec 30 2012 Miro Hrončok <miro@hroncok.cz> - 0.0-1.20120523svn3125
- First try
