# lbs-mono-fedora
Mono 4 packages for Fedora

SeeBuild in [koji f23-mono4](https://copr.fedoraproject.org/coprs/tpokorra/mono

# New packages
Package                        |Notes
-------------------------------|-----
gtk-sharp3                     |Epel6 missing gtk3. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637565)
monodevelop-database           |Epel6 need fix mysql-connection-net first
mysql-connector-net            |Epel6 fail build when try apply patch0
notify-sharp3                  |Epel6 missing gtk3
npgsql                         |
nuget                          |
nunit                          |
nunit25                        |

# Dependecy list
Package                        |Run with Mono 4
-------------------------------|---------------
OpenTK                         |Work from Copr, EPEL6 need fix
RepetierHost                   |Need move to 4.5 profile
avahi                          |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637529)
avahi-sharp                    |Need fix requires avahi-libs
banshee                        |Work from Copr, EPEL6/7 need fix libgpod first
banshee-community-extensions   |Fedora package work without changes if Copr is configured
bareftp                        |Work from Copr, EPEL6 need fix gnome-keyring-sharp. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637654)
bless                          |Need move to 4.5 profile
boo                            |Need move to 4.5 profile
cdcollect                      |Work from Copr, only need rebuild
dbus-sharp                     |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637535)
dbus-sharp-glib                |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637598)
docky                          |Work from Copr, EPEL6 need fix gnome-keyring-sharp. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637641)
gbrainy                        |Fedora package work without changes if Copr is configured
gdata-sharp                    |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637551)
gecko-sharp2                   |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637633)
gio-sharp                      |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637541)
giver                          |Nedd fix avahi-sharp
gkeyfile-sharp                 |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637609)
gmime                          |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637667)
gnome-desktop-sharp            |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637547)
gnome-do                       |Need move to 4.5 profile
gnome-guitar                   |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637679)
gnome-keyring-sharp            |Work from Copr, Epel6 missing libgnome-keyring-devel. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637615)
gnome-rdp                      |Need move to 4.5 profile
gnome-sharp                    |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637538)
gnome-subtitles                |Fedora package work without changes if Copr is configured
gsf-sharp                      |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637661)
gtk-sharp-beans                |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637622)
gtk-sharp2                     |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637531)
gtksourceview-sharp            |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637666)
graphviz                       |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637540)
gudev-sharp                    |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637553)
hyena                          |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637653)
keepass                        |Work from Copr for Fedora, EPEL need fixes
kimono                         |Need fix version requires of libmono-2.0.so.1
libappindicator                |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637662)
libgdiplus                     |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637589)
libgpod                        |Work from Copr, EPEL6 need fix missing libusbx. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637552)
log4net                        |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637559)
mono4                          |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637599)
mono-addins                    |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637575)
mono-basic                     |Work from Copr. Updated to 4.0.1
mono-bouncycastle              |Need move to 4.5 profile
mono-cecil                     |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637639)
mono-cecil-flowanalysis        |Need move to 4.5 profile
mono-debugger                  |Need move to 4.5 profile
mono-reflection                |Need move to 4.5 profile
mono-tools                     |Work from Copr
mono-zeroconf                  |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637550)
monobristol                    |Fedora package install without changes if Copr is configured
monodevelop                    |Work from Copr
monodevelop-debugger-gdb       |Fedora package install without changes if Copr is configured
monosim                        |Fedora package install without changes if Copr is configured
nant                           |Need mono(log4net) = 1.2.13.0. bootstrap works on Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637570)
ndesk-dbus                     |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637549)
ndesk-dbus-glib                |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637632)
nini                           |Work from Copr
notify-sharp                   |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637624)
pdfmod                         |Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637668)
pinta                          |Fedora package work without changes if Copr is configured. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637640)
poppler-sharp                  |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637545)
qyoto                          |Need move to 4.5 profile
rescene                        |
shogun                         |
sparkleshare                   |Fedora package work without changes if Copr is configured
syntastic                      |
taglib-sharp                   |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637613)
themonospot-base               |Need move to 4.5 profile
themonospot-console            |Need move to 4.5 profile
themonospot-gui-gtk            |Need move to 4.5 profile
themonospot-gui-qt             |Need move to 4.5 profile
themonospot-plugin-avi         |Need move to 4.5 profile
themonospot-plugin-mkv         |Need move to 4.5 profile
tomboy                         |Work from Copr
uwsgi                          |
webkit-sharp                   |Work from Copr. Build in [koji f23-mono4](http://koji.fedoraproject.org/koji/buildinfo?buildID=637607)
xsp                            |Work from Copr, EPEL6 need fix
